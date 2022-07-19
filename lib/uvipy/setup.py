# initial test to include custom dependency from private git
# import os
# gitcmd = 'pysoundfile @ git+ssh://<thomas-kowalski>:<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>@github.com/thomas-kowalski/python-soundfile.git'
# os.system(f'pip install {gitcmd}')

from setuptools import setup

setup(name='uvipy',
      version='1.0',
      description='',
      url='',
      author='UVI',
      author_email='t.kowalski@uvi.net',
      license='MIT',
      packages=['uvipy'],
      install_requires=[
            'soundfile @ git+https://<thomas-kowalski>:<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>@github.com/thomas-kowalski/python-soundfile.git',
            'numpy',
            'scipy'
      ],
      zip_safe=False
)
