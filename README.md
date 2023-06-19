# Hop!

Hop is a terminal based file explorer designed to be fast, simple and user friendly. Hop runs on any operating system.

![demo](docs/demo.gif)

## Use
Once Hop installed, it can be ran at any point in the terminal by typing ```hop```. This will bring you into the file explorer.

Anything you type will filter the files, and pressing enter will navigate into a selected folder.

Typing ```+``` at the end of your input, and pressing enter will add a selected item into your "inventory".

You can delete, copy or move the files into your current folder by typing ```!delete```, ```!copy``` or ```!move``` and pressing enter. Deleting will move to the recycle bin.

Empty your inventory (i.e. clear your selection) with ```!empty``` or ```!e```, and quit with ```!q``` or ```!quit```.

Otherwise, run any normal shell commands (i.e. vim, mkdir, rm etc) by using the ! prefix, such as ```!mkdir cool-files```

## Installation
The only requirement for running Hop is python. It can be installed with pip, with optional dependencies for unix (apple/linux):
```
pip install hop-file-browser
pip install 'hop-file-browser[unix]'
```
Consider using pipx to install into an isolated environment.
