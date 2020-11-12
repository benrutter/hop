from setuptools import setup

setup(
    name='hop',
    version='1.0.0',
    author='House of Left',
    description='Python-written terminal based file explorer with support for windows/unix',
    url='https://github.com/houseofleft/hop',
    packages=['hop'],
    install_requires=['getch'],
    entry_points={
        'console_scripts':[
            'hop = hop.hop:main',
        ],
    },
)