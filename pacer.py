#!/usr/bin/python

import os
import sys
import shutil
if os.name == 'nt':
    from msvcrt import getch
else:
    from getch import getch

banner1 = r"    ____"
banner2 = r"   / __ \____ _________  _____"
banner3 = r"  / /_/ / __ '/ __/ _  \/  __/"
banner4 = r" / ____/ /_/ / /__   __/ /"
banner5 = r"/_/    \__~_/\___/\___/_/"
banner = [banner1,banner2,banner3,banner4,banner5]

hidden = True
selected = 0
selection = []
files = os.listdir()
message = ''
move_file = ''
if os.name == 'nt':
    splitter = '\\'
else:
    splitter = '/'

def run_environment(function_mapping, exit_feature=True):
    while True:
        key = ord(getch())
        if key == 27 and exit_feature:
            break
        elif key in function_mapping:
            function_mapping[key]()

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def show_menu():

    global selected
    global files
    term_columns = shutil.get_terminal_size().columns
    big = term_columns >170
    col_size = 40
    dynamic_size = max(10, shutil.get_terminal_size().lines - 20)

    if big:
        margin = ' ' * int(term_columns/10)
    else:
        margin = ' '
    if big:
        line = '-' * term_columns
    else:
        line = ''

    col_size = max(37, int((term_columns/3)-len(margin)-3))

    clear()

    for b in banner:
        print(margin + b)
    print('{}Pacer is a console based file browser.\n{}Vim keys: move, a: console command, s: pacer command\n{}f: select, d: clear, .: hidden, q: quit'.format(margin,margin,margin))
    print(line)

    ### directory_list

    files = os.listdir()
    if hidden:
        files = [f for f in files if f[0] != '.']
    files.sort()

    selected_files = [s['file'] for s in selection if s['path'] == os.getcwd()]
    curr_f = [f + ' ' * int(col_size-len(f)) if len(f) < col_size else f[:col_size-3] + '...' for f in files]
    curr_f.sort()

    prev_sel = [s['file'] for s in selection if s['path'] == os.path.abspath(os.path.join(os.getcwd(), os.pardir))]
    prev_f = os.listdir(os.pardir)
    prev_f = [f + ' ' * int(col_size-len(f)) if len(f) < col_size else f[:col_size-3] + '...' for f in prev_f]
    prev_f.sort()

    try:
        next_sel = [s['file'] for s in selection if s['path'] == os.getcwd() + splitter + files[min(max(0,selected),len(files)-1)]]
        next_f = os.listdir(files[min(max(0,selected),len(files)-1)])
        next_f = [f + ' ' * int(col_size-len(f)) if len(f) < col_size else f[:col_size-3] + '...' for f in next_f]
    except:
        next_f = []
    next_f.sort()

    if hidden:
        curr_f = [f for f in curr_f if f[0] != '.']
        prev_f = [f for f in prev_f if f[0] != '.']
        next_f = [f for f in next_f if f[0] != '.']

    selected = min(max(selected, 0),len(files)-1)
    file_range_trans = curr_f[max(0,selected-(dynamic_size-1)):]
    files_trans = files[max(0,selected-(dynamic_size-1)):]
    file_range = range(0,dynamic_size)

    for i in file_range:

        # previour directory
        if i >= 0 and i < len(prev_f):
            prev = prev_f[i]
            if prev.strip() in prev_sel:
                prev = '*' + prev
            else:
                prev = ' ' + prev
        else:
            prev = ' ' * (col_size+1)

        # current directory
        if selected == i or (selected > dynamic_size-1 and i == dynamic_size-1):
            cursor = ' >> '
        else:
            cursor = '    '

        if i < len(files) and files_trans[i] in selected_files:
            cursor = cursor + '*'
        else:
            cursor = cursor + ' '

        try:
            if i >= 0:
                curr = cursor + curr_f[i]
                curr = cursor + file_range_trans[i]
            else:
                curr = cursor + (' ' * col_size)
        except:
            curr = cursor + (' ' * col_size)

        # next directory
        try:
            nxt = next_f[i]
            if nxt.strip() in next_sel:
                nxt = '*' + nxt
            else:
                nxt = ' ' + nxt
        except:
            nxt = (' ' * (col_size+1))

        if big:
            print(margin + prev + margin + curr + margin + nxt)
        else:
            print(curr)

    print('\n{}'.format(line))
    print('{}DIR: {}'.format(margin, os.getcwd()))
    try:
        if selected >= 0:
            print('{}FILE: {}'.format(margin, files[selected]))
        else:
            print('{}FILE: <NA>'.format(margin))
    except:
        print('{}FILE: <NA>'.format(margin))

    print('{}SELECTION: {}'.format(margin, [s['file'] for s in selection]))
    print(line)

def move(num):
    global selected
    global message
    message = ''
    selected += num
    show_menu()

def left():
    global selected
    try:
        os.chdir('..')
        selected = 0
    except:
        pass
    show_menu()

def right():
    global selected
    try:
        os.chdir(files[selected])
        selected = 0
    except:
        pass
    show_menu()

def exec_int():
    show_menu()
    cmd = input(' Console Execute: ')
    os.system(cmd)

def quit():
    clear()
    os._exit(0)

def del_f():
    cmd = input(' Delete ' + str([s['path'] + splitter + s['file'] for s in selection]) + '? (Y/N) ')
    if cmd.lower().strip() == 'y':
        for s in selection:
            try:
                os.remove(s['path'] + splitter + s['file'])
            except:
                try:
                    shutil.rmtree(s['path'] + splitter + s['file'])
                except Exception as e:
                    print(' Deletion error ({})'.format(str(e)))
        clear_selection()
    else:
        print(' Not deleted.')
    show_menu()

def select():
    global selection
    f_dict = {'path':os.getcwd(),'file':files[selected]}
    if f_dict in selection:
        selection.remove(f_dict)
    else:
        selection.append(f_dict)
    show_menu()

def clear_selection():
    global selection
    selection = []
    show_menu()

def move_file(action='Move'):
    cmd = input(' {} {} into current directory? (Y/N)'.format(action, [s['path'] + splitter + s['file'] for s in selection]))
    if cmd.lower().strip() == 'y':
        try:
            for s in selection:
                if action == 'Move':
                    shutil.move(s['path'] + splitter + s['file'], str(os.getcwd()) + splitter)
                elif action == 'Copy':
                    shutil.copy(s['path'] + splitter + s['file'], str(os.getcwd()) + splitter)
            clear_selection()
            print(' Complete.')
        except Exception as E:
            print(' Error: ' + str(E))
    else:
        print(' Not complete.')
    show_menu()


def exec_pacer():
    show_menu()
    cmd = input(' Command for current selections? (move, copy, delete): ')
    if cmd.lower().strip() == 'move':
        move_file('Move')
    elif cmd.lower().strip() == 'copy':
        move_file('Copy')
    elif cmd.lower().strip() == 'delete':
        del_f()
    else:
        print(' No action taken')
    show_menu()

def switch_hidden():
    global hidden
    hidden = not hidden
    show_menu()

key_mapping = {
    106: lambda: move(1),
    107: lambda: move(-1),
    108: right,
    104: left,
    97: exec_int,
    115: exec_pacer,
    102: select,
    100: clear_selection,
    113: quit,
    46: switch_hidden
}

show_menu()
run_environment(key_mapping, exit_feature=False)
