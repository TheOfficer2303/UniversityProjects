import sys
from getpass import getpass
from argon2 import PasswordHasher

ph = PasswordHasher()


def replace_for_user(user, file_name, for_replacing, password, force_password):
    user_line = None
    lines = []
    with open(file_name, 'r') as file:
        lines = file.readlines()
        for number, line in enumerate(lines):
            if line.split(" ")[0] == user:
                user_line = number

    with open(file_name, 'w') as file:
        for line_no, line in enumerate(lines):
            if line_no == user_line:
                if for_replacing == 'password':
                    force_password = str(lines[line_no].split(" ")[2]).strip()
                elif for_replacing == 'force_password':
                    password = str(lines[line_no].split(" ")[1]).strip()

                lines[line_no] = user + ' ' + password + ' ' + force_password + '\n'
        file.writelines(lines)


def check_if_user_exist(user, file_name):
    with open(file_name, 'r') as file:
        for line in file:
            if line.split(" ")[0] == user:
                return True


def force_password(user, file_name):
    if not check_if_user_exist(user, file_name):
        print('No user with that username!')
        exit(1)

    force_password = 'True'
    replace_for_user(user, file_name, 'force_password', force_password=force_password, password=None)
    print('User will be requested to change password on next login.')


def change_password(user, file_name):
    if not check_if_user_exist(user, file_name):
        print('No user with that username!')
        exit(1)

    new_password = getpass()
    repeat_new_password = getpass('Repeat password: ')

    if new_password != repeat_new_password:
        print('Password mismatch!')
        exit(1)

    new_password_hash_verbose = ph.hash(new_password)
    new_password_hash = new_password_hash_verbose.split('p=')[1]

    replace_for_user(user, file_name, 'password', password=new_password_hash, force_password=None)
    print('Password changed!')


def delete_user(user, file_name):
    if not check_if_user_exist(user, file_name):
        print('No user with that username!')
        exit(1)

    with open(file_name, 'r') as file_read:
        lines = file_read.readlines()
        with open(file_name, 'w') as file_write:
            for line in lines:
                if line.split(" ")[0] != user:
                    file_write.write(line)
    print('User successfully removed!')


def add_user(user, file_name):
    global argon_info

    if check_if_user_exist(user, file_name):
        print('User exists')
        exit(1)

    password = getpass()
    repeat_password = getpass('Repeat password: ')

    if password != repeat_password:
        print('Password mismatch!')
        exit(1)

    password_hash_verbose = ph.hash(password)
    password_hash = password_hash_verbose.split('p=')[1]
    force_password = False

    with open(file_name, 'a') as file:
        user_info = user + ' ' + password_hash + ' ' + str(force_password) + '\n'
        file.writelines(user_info)
        print('User successfully added!')


def main():
    # change_password('blaz', file_name='pass.txt')
    args_len = len(sys.argv)
    user = ''
    command = ''
    if args_len == 3:
        command = sys.argv[1]
        user = sys.argv[2]
    else:
        print('Wrong usage of arguments. Read README.md for more info!')
        exit(1)

    if command == 'add':
        add_user(user, file_name='pass.txt')
    elif command == 'del':
        delete_user(user, file_name='pass.txt')
    elif command == 'password':
        change_password(user, file_name='pass.txt')
    elif command == 'forcepass':
        force_password(user, file_name='pass.txt')


if __name__ == '__main__':
    main()
