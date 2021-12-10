from setuptools import setup

setup(
    name='hop-file-browser',
    version='1.1.3',
    author='hop by benrruter + pip installation script by Elsoleiro',
    description='Python-written terminal based file explorer with support for windows/unix',
    url='https://github.com/benrrutter/hop',
    packages=['hop'],
    extras_require={'unix': ['getch']},
    entry_points={
        'console_scripts': [
            'hop = hop.hop:run_session',
        ],
    },
) 
