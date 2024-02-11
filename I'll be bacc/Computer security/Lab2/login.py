import random
import string
import sys
from getpass import getpass
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

ph = PasswordHasher()
argon_info = '$argon2id$v=19$m=65536,t=3,p='


def replace_for_user(user, file_name, password):
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
                lines[line_no] = user + ' ' + password + ' ' + 'False' + '\n'
        file.writelines(lines)


def check_if_reset_forced(user, file_name):
    with open(file_name, 'r') as file:
        for line in file:
            if line.split(" ")[0] == user:
                return line.split(" ")[2].strip() == 'True'


def check_if_user_exist(user, file_name):
    with open(file_name, 'r') as file:
        for line in file:
            if line.split(" ")[0] == user:
                return True


def check_if_passwords_match(user, file_name, password):
    with open(file_name, 'r') as file:
        for line in file:
            if line.split(" ")[0] == user:
                original_password_hash = line.split(" ")[1]
                try:
                    if ph.verify(argon_info + original_password_hash, password):
                        return True
                except VerifyMismatchError:
                    return False


def mock_login():
    random_password = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))
    random_password_to_hash = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16))

    try:
        ph.verify(ph.hash(random_password_to_hash), random_password)
    except VerifyMismatchError:
        pass


def login(user, file_name):
    password_input = getpass()
    if check_if_user_exist(user, file_name):
        if not check_if_passwords_match(user, 'pass.txt', password_input):
            print('Wrong username or password!')
            exit(1)

        if check_if_reset_forced(user, file_name):
            new_password_input = getpass('New password: ')
            repeat_new_password_input = getpass('Repeat new password: ')

            if new_password_input != repeat_new_password_input:
                print('Password mismatch!')
                exit(1)

            new_password_hash_verbose = ph.hash(new_password_input)
            new_password_hash = new_password_hash_verbose.split('p=')[1]

            replace_for_user(user, file_name, new_password_hash)

        print('Login successful!')
    else:
        mock_login()
        print('Wrong username or password!')
        exit(1)


def main():
    args_len = len(sys.argv)
    user = ''
    if args_len == 2:
        user = sys.argv[1]
    else:
        print('Wrong usage of arguments. Read README.md for more info!')
        exit(1)

    login(user, 'pass.txt')


if __name__ == '__main__':
    main()
