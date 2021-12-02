import os
# module imports
if os.name == 'nt':
    from msvcrt import getch
else:
    from getch import getch

# function definitions
def quit():
    os._exit(0)

def run_environment(function_mapping):
    while True:
        key = ord(getch())
        if key in function_mapping:
            function_mapping[key]()
        else:
            print(key)

# key mappings and running environment

key_mapping = {
    106: lambda: print('down'),
    107: lambda: print('up'),
    113: quit,
    53: lambda: print('page up'),
    54: lambda: print('page down'),
}


run_environment(key_mapping)

