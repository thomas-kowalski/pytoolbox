#%% Generate UVIP presets from sample folder input 

import os
import re
from uvipy.sf import browse
from uvipy.midi import *
from copy import deepcopy
import xml.etree.ElementTree as ET

template = """
<UVI4>
    <Program Name="Program" Bypass="0" BypassInsertFX="0" Gain="1" Pan="0" DisplayName="New Program" TransposeOctaves="0" TransposeSemiTones="0" OutputName="" Polyphony="16" NotePolyphony="0" ProgramPath="" LoopProgram="0" Streaming="1">
        <ControlSignalSources/>
        <Layers>
            <Layer Name="Layer 0" Bypass="0" BypassInsertFX="0" Gain="1" Pan="0" Mute="0" MidiMute="0" Solo="0" DisplayName="Layer 1" OutputName="" LowKey="0" HighKey="127" CustomPolyphony="0" PlayMode="0" PortamentoTime="0.029999999" PortamentoCurve="0" PortamentoMode="0" NumVoicesPerNote="1" VelocityCurve="0">
                <Properties Color="ff02b0ff"/>
                <ControlSignalSources/>
                <BusRouters/>
                <Keygroups>
                    <Keygroup Name="Keygroup 0" Bypass="0" BypassInsertFX="0" Gain="1" Pan="0" DisplayName="Keygroup 1" OutputName="" ExclusiveGroup="0" LowKey="127" HighKey="127" LowVelocity="1" HighVelocity="127" LowKeyFade="0" HighKeyFade="0" LowVelocityFade="0" HighVelocityFade="0" FadeCurve="2" TriggerMode="0" TriggerSync="0" TriggerRule="0" LatchTrigger="0" FXPostGain="0">
                        <Connections>
                            <SignalConnection Name="AmpEnvMod" Ratio="1" Source="Amp. Env" Destination="Gain" Mapper="" ConnectionMode="0" Bypass="0" Inverted="0"/>
                        </Connections>
                        <ControlSignalSources>
                            <AnalogADSR Name="Amp. Env" DisplayName="Amp. Env" Bypass="0" AttackTime="0.001" DecayTime="0.050000001" KeyToDecay="0" KeyToAttack="0" VelToDecay="0" Punch="0" VelToAttack="0" DynamicRange="20" SustainLevel="1" ReleaseTime="0.0099999998" TriggerMode="0" InvertVelocity="0" AttackDecayMode="0"/>
                        </ControlSignalSources>
                        <BusRouters/>
                        <Oscillators>
                            <SamplePlayer Name="Oscillator" Bypass="0" CoarseTune="0" FineTune="0" Gain="1" Pitch="0" NoteTracking="1" BaseNote="60" DisplayName="Oscillator 1" SamplePath="" SampleStart="0" InterpolationMode="1" AllowStreaming="1" Reverse="0" SamplePurged="0">
                                <Connections>
                                    <SignalConnection Name="PitchBendMod" Ratio="2" Source="@PitchBend" Destination="Pitch" Mapper="" ConnectionMode="0" Bypass="0" Inverted="0"/>
                                </Connections>
                            </SamplePlayer>
                        </Oscillators>
                    </Keygroup>
                </Keygroups>
            </Layer>
        </Layers>
    </Program>
</UVI4>
"""

def main(root_samples):
    folders = []
    for root, dirs, files in os.walk(root_samples):
        if len(dirs) == 0: continue
        for dir in dirs:
            folders.append(os.path.join(root, dir))

    template_tree = ET.ElementTree(ET.fromstring(template))
    template_root = template_tree.getroot()
    basepath = os.path.join(os.path.split(root_samples)[0], "_Generated")

    try:
        os.mkdir(basepath)
    except:
        pass

    for folder in folders:
        foldername = os.path.split(folder)[1]
        presetpath = f'{os.path.join(basepath, foldername)}.uvip'

        newtree = deepcopy(template_tree)
        newroot = newtree.getroot()

        keygroup_template = deepcopy(newroot.find(".//Keygroup"))
        keygroups_node = newroot.find(".//Keygroups")

        try:
            keygroup_to_remove = keygroups_node.find(".//Keygroup")
            keygroups_node.remove(keygroup_to_remove)
        except:
            pass

        samples = browse(folder)
        for i in range(len(samples)):
            sample = samples[i]

            note = get_note_name(sample)
            midinote = note_from_name(note)

            new_keygroup = deepcopy(keygroup_template)
            new_keygroup.attrib["Name"] = "Keygroup "+str(i)
            new_keygroup.attrib["DisplayName"] = note
            new_keygroup.attrib["LowKey"] = str(midinote)
            new_keygroup.attrib["HighKey"] = str(midinote)

            splayer = new_keygroup.find(".//SamplePlayer")
            splayer.attrib["BaseNote"] = str(midinote)
            splayer.attrib["SamplePath"] = sample

            keygroups_node.append(new_keygroup)

        newtree.write(presetpath)

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("usage: python <script> <samples folder containing multiple subfolders>")
# %%
