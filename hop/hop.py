import os
import shutil
if os.name == 'nt':
    from msvcrt import getch
else:
    from getch import getch


class HopEnvironment():
    def __init__(self):
        self.show_help = False
        self.hidden = True
        self.selected = 0
        self.selection = []
        self.file_icons = ['∙', '∗', '∘']
        self.message = ''
        if os.name == 'nt':
            self.splitter = '\\'
        else:
            self.splitter = '/'
        self.banner_segments = [
            '┬ ┬┌─┐┌─┐',
            '├─┤│ │├─┘',
            '┴ ┴└─┘┴  ',
        ]
        self.set_dynamic_variables()

    def set_dynamic_variables(self):
        self.files = os.listdir()
        self.files.sort()
        if self.hidden:
            self.files = [i for i in self.files if i[0] != '.']
        terminal_columns, terminal_lines = shutil.get_terminal_size()
        self.dynamic_height = max(10, terminal_lines - 20)
        self.wide_mode = terminal_columns > 100

        if self.wide_mode:
            self.margin = ' ' * int(terminal_columns/20)
            self.line = '-' * terminal_columns
            self.column_size = int((terminal_columns - (len(self.margin)*3))/3)-5
        else:
            self.margin = ' '
            self.line = ''
            self.column_size = 30

    def highlight(self, string):
        return f"\033[7m{string}\033[00m"

    def file_icon(self, file_string):
        file_ending = file_string.split('.')[-1]
        if file_string == file_ending:
            return '  '
        else:
            icon = self.file_icons[ord(file_ending[0]) % len(self.file_icons)]
            return ' ' + icon

    def quit(self):
        self.clear()
        os._exit(0)

    def clear(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def toggle_hidden(self):
        self.hidden = not self.hidden

    def toggle_show_help(self):
        self.show_help = not self.show_help

    def filename_for_display(self, filename):
        if len(filename) < self.column_size:
            buffer = ' ' * int(self.column_size-len(filename))
            return filename + self.file_icon(filename) + buffer
        else:
            return filename[:self.column_size-1] + '...'

    def display_banner(self):
        for banner_segment in self.banner_segments:
            print(f'{self.margin}{banner_segment}')
        if self.show_help:
            print(
                f'{self.margin}h, j, k & l, or arrow keys to move'
                f'\n{self.margin}console commands with a, hop commands with si'
                f'\n{self.margin}select files with f and clear with di'
                f'\n{self.margin}show hidden files with . and hide help with #'
                f'\n{self.margin}quit with q'
            )
        else:
            print(f'{self.margin}# for help')
        print(self.line)

    def read_directories(self):
        cwd_files = os.listdir()
        if self.hidden:
            cwd_files = [i for i in cwd_files if i[0] != '.']
        cwd_files.sort()

        self.cwd_selection = [
            i['file'] for i in self.selection if i['path'] == os.getcwd()
        ]

        self.cwd_files = [self.filename_for_display(i) for i in cwd_files]

        self.pwd_selection = [
            i['file'] for i in self.selection
            if i['path'] == os.path.abspath(
                os.path.join(os.getcwd(), os.pardir)
            )
        ]

        self.pwd_files = [self.filename_for_display(
            i) for i in os.listdir(os.pardir)]
        self.pwd_files.sort()

        try:
            self.nwd_selection = [
                i['file'] for i in self.selection
                if i['path'] == os.getcwd() + self.splitter +
                cwd_files[min(max(0, self.selected), len(cwd_files)-1)]
            ]
            self.nwd_files = [
                self.filename_for_display(i) for i in os.listdir(
                    cwd_files[min(max(0, self.selected), len(cwd_files)-1)])
            ]
            self.nwd_files.sort()
        except (NotADirectoryError, PermissionError, IndexError):
            self.nwd_files = []

        # removing hidden files
        if self.hidden:
            self.pwd_files = [i for i in self.pwd_files if i[0] != '.']
            self.nwd_files = [i for i in self.nwd_files if i[0] != '.']

    def in_selection(self, filename, selection):
        for icon in self.file_icons:
            filename = filename.replace(icon, ' ')
        filename = filename.strip()
        return filename in selection

    def display_directories(self):
        self.selected = min(max(self.selected, 0), len(self.cwd_files)-1)
        for i in range(0, self.dynamic_height):

            # previous directory
            # let's not display anything if we're at the absolute parent
            if (i < len(self.pwd_files)) and (self.pwd_files != self.cwd_files):
                pwd_line = self.pwd_files[i]
                if self.in_selection(pwd_line, self.pwd_selection):
                    pwd_line = self.highlight(pwd_line)
            else:
                pwd_line = ' ' * self.column_size + '  '

            # cursor
            if self.selected == i or (
                    self.selected > self.dynamic_height-1 and
                    i == self.dynamic_height-1
            ):
                cursor = ' >> '
            else:
                cursor = '    '

            # current directory
            # we need slightly different logic to move around in this one
            overshoot = max(0, self.selected - self.dynamic_height + 1)
            i_adjusted = overshoot + i
            if i_adjusted < len(self.cwd_files):
                cwd_line = self.cwd_files[i_adjusted]
                if self.in_selection(cwd_line, self.cwd_selection):
                    cwd_line = self.highlight(cwd_line)
            else:
                cwd_line = ' ' * self.column_size + '  '

            # next directory
            if i < len(self.nwd_files):
                nwd_line = self.nwd_files[i]
                if self.in_selection(nwd_line, self.nwd_selection):
                    nwd_line = self.highlight(nwd_line)
            else:
                nwd_line = ' ' * self.column_size + '  '

            if self.wide_mode:
                print(self.margin + pwd_line + self.margin +
                      cursor + cwd_line + self.margin + nwd_line)
            else:
                print(cursor + cwd_line)

    def display_cmd(self):
        print(self.line)
        if self.selected >= 0:
            print(f'{self.margin}FILE: {self.files[self.selected]}')
        else:
            print(f'{self.margin}FILE: <NA>')
        print(f'{self.margin}SELECTION: {[i["file"] for i in self.selection]}')

    def move(self, num):
        self.message = ''
        self.selected += num

    def up_dir(self):
        os.chdir('..')
        self.selected = 0

    def down_dir(self):
        try:
            os.chdir(self.files[self.selected])
            self.selected = 0
        except (NotADirectoryError, PermissionError, IndexError):
            pass

    def select(self):
        file_dict = {'path': os.getcwd(), 'file': self.files[self.selected]}
        if file_dict in self.selection:
            self.selection.remove(file_dict)
        else:
            self.selection.append(file_dict)

    def clear_selection(self):
        self.selection = []

    def shell_execute(self):
        cmd = input(f'{self.margin}Console Execute: ')
        os.system(cmd)
        print(f"\n\n{self.margin}Press any key to continue.")
        _ = getch()

    def delete_file(self):
        cmd = input(f"{self.margin}Delete all files in selection? (Y/N) ")
        replace_selection = self.selection.copy()
        if cmd.lower().strip() != 'y':
            return False
        for i in self.selection:
            try:
                os.remove(i['path'] + self.splitter + i['file'])
                replace_selection.remove(i)
            except IsADirectoryError:
                shutil.rmtree(i['path'] + self.splitter + i['file'])
                replace_selection.remove(i)
            except PermissionError:
                print(
                    f"{self.margin}Permission Error.\n{self.margin}Press any key to continue")
                _ = getch()
                return False
        self.selection = replace_selection

    def move_file(self):
        cmd = input(f"{self.margin}Move files into directory? (Y/N) ")
        replace_selection = self.selection.copy()
        if cmd.lower().strip() != 'y':
            return False
        try:
            for i in self.selection:
                shutil.move(i['path'] + self.splitter +
                            i['file'], str(os.getcwd()) + self.splitter)
                replace_selection.remove(i)
        except Exception as e:
            print(
                f"{self.margin}Unexpected error: {e}\n{self.margin}Press any key to continue.")
            _ = getch()
        self.selection = replace_selection

    def copy_file(self):
        cmd = input(f"{self.margin}Copy files into directory? (Y/N) ")
        replace_selection = self.selection.copy()
        if cmd.lower().strip() != 'y':
            return False
        try:
            for i in self.selection:
                try:
                    shutil.copy(i['path'] + self.splitter +
                                i['file'], str(os.getcwd()) + self.splitter)
                    replace_selection.remove(i)
                except IsADirectoryError:
                    shutil.copytree(
                        i['path'] + self.splitter + i['file'],
                        str(os.getcwd()) + self.splitter + i['file'])
                    replace_selection.remove(i)
        except Exception as e:
            print(
                f"{self.margin}Unexpected error: {e}\n{self.margin}Press any key to continue.")
            _ = getch()
        self.selection = replace_selection

    def pacer_execute(self):
        cmd = input(
            f'{self.margin}Command for current selections? (move, copy, delete): ').lower().strip()
        if cmd == 'move':
            self.move_file()
        elif cmd == 'copy':
            self.copy_file()
        elif cmd == 'delete':
            self.delete_file()
        else:
            print('No action taken')

    def callback(self):
        self.set_dynamic_variables()
        self.read_directories()
        self.clear()
        self.display_banner()
        self.display_directories()
        self.display_cmd()

    def run(self):
        function_mapping = {
            106: lambda: self.move(1),
            66: lambda: self.move(1),
            107: lambda: self.move(-1),
            65: lambda: self.move(-1),
            53: lambda: self.move(-50),
            54: lambda: self.move(50),
            108: self.down_dir,
            67: self.down_dir,
            104: self.up_dir,
            68: self.up_dir,
            46: self.toggle_hidden,
            35: self.toggle_show_help,
            113: self.quit,
            97: self.shell_execute,
            102: self.select,
            100: self.clear_selection,
            115: self.pacer_execute,
        }

        self.callback()

        while True:
            try:
                key = ord(getch())
            except OverflowError:
                key = ''
            if key in function_mapping:
                function_mapping[key]()
                self.callback()


def run_session():
    session = HopEnvironment()
    session.run()


if __name__ == "__main__":
    run_session()
