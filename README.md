# Hop!
Hop is a python-written terminal based file explorer with support for windows/unix

![screenshot](https://github.com/houseofleft/hop/blob/master/readme_files/hop_scrot.png)

## Use
Once Hop installed, it can be ran at any point in the terminal by typing 'hop' - this will bring you into the file explorer.

Press "#" if you need help with the controls, but the controls are:

**h, j, k, l (vim keys)** to move around folders

**f** will add the current file/folder to your selection

**d** will clear your selection

**s** will run a Hop command (move, copy, delete) on your selection

**a** to enter shell prompt *(this will let you run any commands normally allowed in your shell such as "vim new_file.txt" or "grep something")*

**.** will toggle whether hidden (dot files) are shown

**q** will exit hop and bring you back to the terminal


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

