from distutils.core import setup

setup(
    name='psmodulecheck',
    version='0.1dev',
    author='Tod Gentille',
    author_email="info@syncorsystems.com",
    packages=['psmodulecheck'],
    #data_files=[('settings.json', '.\psmodulecheck')]
    package_data={'psmodulecheck': ['./settings.json']},
    license='The MIT License (MIT)',
    description='Validate a PluralSight module folder. '
                'Check that all needed files are present and more.',
    long_description=open('ReadMe.md').read(),
    keywords=['PluralSight', 'module checker', 'module validator'],
    requires=['termcolor', 'colorama'],
)
