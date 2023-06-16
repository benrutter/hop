from typing import List
import os
from pathlib import Path
import shutil

from send2trash import send2trash
from rich import print

if os.name == "nt":
    from msvcrt import getch
else:
    from getch import getch



class HopApp:

    def __init__(self):
        self.input_str: str = ""
        self.message: str = ""
        self.inventory: List[str] = []
        self.list_length = 20
        self.files: List[str] = []
        self.input_length = 30
        self.max_file_width = 30
        self.running = True

    def display_header(self) -> None:
        print(f"{os.getcwd()}\n")
        trimmed_input_str: str = self.input_str
        if len(trimmed_input_str) > self.input_length:
            trimmed_input_str = trimmed_input_str[len(trimmed_input_str) - self.input_length:]
        elif len(trimmed_input_str) < self.input_length:
            trimmed_input_str += ' '*(self.input_length-len(trimmed_input_str))
        print(f"[bold reverse]>> {trimmed_input_str}[/bold reverse]\n")

    def levenshtein_distance(self, a, b) -> int:
        char_diff = len(set(a) - set(b))
        len_diff = abs(len(b) - len(a))
        return len_diff + char_diff

    def update_files(self) -> None:
        self.files = [Path("..")] + [i.resolve() for i in Path(".").iterdir()]
        if self.input_str.startswith("!"):
            return None
        search_str = self.input_str.lower().strip()
        if search_str.endswith("+"):
            search_str = search_str[:-1]
        files = [i for i in self.files if search_str in str(i).lower()]
        files.sort(key=lambda x: self.levenshtein_distance(search_str, str(x)))
        self.files = files


    def get_icon(self, path: Path) -> str:
        if path.is_dir():
            return ":file_folder:"
        if path.suffix != "":
            file_icons = [":koala:", ":honeybee:", ":kiwi_fruit:", ":herb:", ":wave:"]
            return file_icons[ord(path.suffix[-1]) % len(file_icons)]
        return ":alien_monster:"

    def display_files(self) -> None:
        cut_files = self.files[:min(self.list_length, len(self.files))]
        blanks: List[str] = ['' for i in range(self.list_length - len(self.files))]
        files_to_display: List[str] = [str(i.stem) + str(i.suffix) for i in cut_files] + blanks
        icons: List[str] = [self.get_icon(i) for i in cut_files] + blanks
        selected: List[bool] = [i in self.inventory for i in cut_files] + blanks
        for i, (file, icon, is_selected) in enumerate(zip(files_to_display, icons, selected)):
            if file == "..":
                file = ".. (parent dir)"
            if i == 0:
                file = f"[blue u]{file}[/blue u]"
            if is_selected:
                file += "*"
            print(f"{icon} {file}")

    def display_footer(self) -> None:
        print(f"[u]{' ' * self.max_file_width}[/u]")
        formatted_inventory: str = ', '.join([str(i.stem) for i in self.inventory]) or "empty"
        print(f"\nInventory: {formatted_inventory}")
        print(self.message)

    def add_to_inventory(self) -> None:
        if len(self.files) > 0 and self.files[0] not in self.inventory:
            self.inventory += [self.files[0]]

    def empty_inventory(self) -> None:
        self.inventory = []

    def delete_files_in_inventory(self) -> None:
        not_deleted: List[str] = []
        for i in self.inventory:
            try:
                send2trash(i.resolve())
            except:
                not_deleted.append(str(i))
        self.inventory = []
        if len(not_deleted) > 0:
            self.message = "[red bold]Could not delete:\n" + "\n".join(not_deleted) + "[/red bold]"
        else:
            self.message = "[green]Files in inventory deleted[/green]"
        self.input_str = ""

    def move_files_in_inventory(self) -> None:
        not_moved: List[str] = []
        for i in self.inventory:
            try:
                shutil.move(i.resolve(), i.stem)
            except:
                not_moved.append(str(i))
        self.inventory = []
        if len(not_moved) > 0:
            self.message = "[red bold]Could not move:\n" + "\n".join(not_moved) + "[/red bold]"
        else:
            self.message = "[green]Files in inventory moved[/green]"
        self.input_str = ""


    def copy_files_in_inventory(self) -> None:
        not_copied: List[str] = []
        for i in self.inventory:
            try:
                shutil.copy(str(i.resolve()), i.stem)
            except:
                not_copied.append(str(i))
        self.inventory = []
        if len(not_copied) > 0:
            self.message = "[red bold]Could not copy:\n" + "\n".join(not_copied) +"[/red bold]"
        else:
            self.message = "[green]Files in inventory copied[/green]"
        self.input_str = ""


    def exit(self) -> None:
        self.running = False

    def shell_exec(self) -> None:
        os.system(self.input_str[1:])
        print("[blue]Press any key to continue[/blue]")
        _ = getch()
        self.input_str = ""

    def run_command(self) -> None:
        mapping = {
            "!e": self.empty_inventory,
            "!empty": self.empty_inventory,
            "!exit": self.exit,
            "!quit": self.exit,
            "!q": self.exit,
            "!delete": self.delete_files_in_inventory,
            "!copy": self.copy_files_in_inventory,
            "!move": self.move_files_in_inventory,
        }
        run = mapping.get(self.input_str) or self.shell_exec
        run()

    def chdir(self) -> None:
        if len(self.files) == 0:
            return None
        try:
            os.chdir(self.files[0])
            self.input_str = ""
        except:
            self.message = "[red]Can\'t navigate into item[/red]"

    def backspace(self) -> None:
        if len(self.input_str) != 0:
            self.input_str = self.input_str[:-1]

    def process_keys(self) -> None:
        key = getch()
        key_code = ord(key)
        if key_code == 10 and self.input_str.startswith('!'):
            self.run_command()
        elif key_code == 10 and self.input_str.endswith('+'):
            self.add_to_inventory()
        elif key_code == 10:
            self.chdir()
        elif key_code == 127:
            self.backspace()
            self.message = ""
        else:
            self.input_str += key
            self.message = ""

    def clear(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')    

    def run(self) -> None:
        self.clear()
        while self.running:
            self.update_files()
            self.display_header()
            self.display_files()
            self.display_footer()
            self.process_keys()
            self.clear()


if __name__ == "__main__":
    app = HopApp()
    app.run()