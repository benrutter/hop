# HOP
Hop is an installation free, python-written terminal based file explorer with support for windows/unix

![readme_files/screenshot](https://github.com/houseofleft/pacer/blob/master/hop_scrot.png)

## Setting up
The central requirement for running Hop is python 3 (if you're on a linux system, you'll also need to pip install getch)

If you want to run from the terminal anywhere, you may want to add either the "unix" or "windows" folder to path, which will allow you to run by typing "hop" in the terminal

## Unix
Add to path using the following command:
    export PATH=/home/you/wherever/you/saved/this/hop/unix:$PATH

(You may also need to allow the file to execute with "chmod +x hop")

## Windows
Adding to path in windows is a little bit (but not too much) more complicated.

Firstly, you'll need to edit the hop.bat file inside the 'hop/windows' folder to reference your python source location and the location you cloned this repo to,

After that you can add the path by modifying your 'environment variables' (search for this term in the start menu)
