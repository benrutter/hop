# Hop!
Hop is a python-written terminal based file explorer with support for windows/unix.


## Use
Once Hop installed, it can be ran at any point in the terminal by typing 'hop' - this will bring you into the file explorer.

## Installation
The only requirement for running Hop is python. It can be installed with pip, if you're installing through windows run:
```
python -m pip install hop-file-browser
```
Unix systems have an additional requirement (the getch module) so can be installed for with:
```
python -m pip install hop-file-browser[unix]
```
or if required (for some setups, this might be needed to allow a runnable command line script)
```
sudo python -m pip install hop-file-browser[unix]
```

