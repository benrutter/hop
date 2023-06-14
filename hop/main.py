import os
import sys

from rich import print

if os.name == "nt":
    from msvcrt import getch
else:
    from getch import getch

def run():
    input_str = ""
    message = ""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')

        print(os.getcwd())
        print()
        print(input_str)
        print()
        files = [".."] + os.listdir()
        files = [i for i in files if input_str.lower() in i.lower()]
        files = files[:min(10, len(files))]
        for i, file in enumerate(files):
            if i == 0:
                print(f"[blue]{file}[/blue]")
            else:
                print(file)
        print(message)
        key = getch()
        key_code = ord(key)
        # if key.lower() in "qwertyuiopasdfghjklzxcvbnm" or key_code == 32:
        #     input_str += key
        if key_code == 127:
            if len(input_str) != 0:
                input_str = input_str[:-1]
                message = ""
        elif key_code == 10:
            try:
                os.chdir(files[0])
                input_str = ""
                message = ""
            except:
                message = f"[red]Can\'t navigate into item[/red]"
        else:
            input_str += key

if __name__ == "__main__":
    run()