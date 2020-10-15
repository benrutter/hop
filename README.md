# pacer
installation free, python-written terminal based file explorer with support for windows/unix

## setting up
the only requirement for running pacer is python 3 (although if you're on a linux system, you'll also need to pip install getch)

if you want to run from the terminal anywhere, you may want to add either the "unix" or "windows" folder to path, which will allow you to run by typing "pacer" in the terminal

## Unix
add to path using the following command:
    export PATH=/home/you/wherever/you/saved/this/pacer/unix:$PATH

(you may also need to allow the file to execute with "chmod +x pacer")

## Windows
adding to path in windows is a little bit (but not too much) more complicated.

firstly, you'll need to edit the pacer.bat file inside the 'pacer/widows' folder to reference your python source location and the location you cloned this repo to,

After that you can add the path by modifying your 'environment variables' (search for this term in the start menu)

