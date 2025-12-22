import os
import sys
import json



def create_autorun(
            target_file_path: str,
            drive_path: str,
            ) -> None:

    path = drive_path + r"autorun.cc"
    
    with open(path, 'w') as file:
        data = {'target_file_path': target_file_path,
                }

        json.dump(data, file)



def parse_flags(argv: list) -> tuple:
    flags = {}
    args = []
    i = 1  # bỏ argv[0] vì nó là tên file

    while i < len(argv):
        if argv[i].startswith('--'):
            key = argv[i]

            if i + 1 < len(argv) and not argv[i+1].startswith('--'):
                flags[key] = argv[i+1]
                i += 2
            else:
                flags[key] = True
                i += 1
        else:
            args.append(argv[i])
            i += 1

    return args, flags

if __name__ == '__main__':
    data = sys.argv
    if len(data) < 2:
        file_name = data[0] # file name
        print(f'''
Ussage:
    {file_name} <target file path> <create in>

Options:
    <target file path>              path to the target file.
    <create in>                     Directory where autorun.cc will be created.


Examples:
    {file_name} D:\payload.exe D:\
    {file_name} G:\hot_anime_girl.png  X:\

''')
        exit()



    try:
        
        args, flags = parse_flags(data)
        create_autorun(*args)

    except KeyError as e:
        print(f'Key ERROR: {e}')


