#!/usr/bin/env python3

import os
import sys
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt

masterPassword = ""


def findAddressLineNumber(address):
    try:
        with open('address') as file:
            for num, line in enumerate(file):
                if address.decode() in line:
                    return num
    except FileNotFoundError:
        print('No passwords yet!')
        exit(1)


def normalize(str):
    return str.replace('\\n'.encode(), '\n'.encode()) \
        .replace('\\t'.encode(), '\t'.encode()) \
        .replace('\\r'.encode(), '\r'.encode())


def deWindowsize(str):
    return str.replace('\n'.encode(), '\\n'.encode()) \
        .replace('\t'.encode(), '\\t'.encode()) \
        .replace('\r'.encode(), '\\r'.encode())


def decrypt():
    if SHA256.new(sys.argv[2].encode()).hexdigest() != masterPassword:
        print("Wrong master password!")
        exit(1)
    address = SHA256.new(sys.argv[3].encode()).hexdigest().encode()  # hash the address

    lineNumber = findAddressLineNumber(address)
    with open('extras', 'rb') as file:
        for i, line in enumerate(file):
            if i == lineNumber:
                salt = line
                salt = normalize(salt)

    # derive
    kdf = Scrypt(
        salt=salt[0:16],
        length=16,
        n=2 ** 14,
        r=4,
        p=1,
    )
    key = kdf.derive(sys.argv[2].encode())

    with open('pass', 'rb') as file:
        for i, line in enumerate(file):
            if i == lineNumber:
                cipher_password = line
                cipher_password = normalize(cipher_password)

    cipher = AES.new(key, AES.MODE_CBC, iv=address[0:16])
    numba = len(cipher_password) - 1

    try:
        plain_password = unpad(cipher.decrypt(cipher_password[0:numba]), AES.block_size)
        print(f'Password for {sys.argv[3]} is: {plain_password.decode()}')
    except ValueError:
        print(f"***WARNING***"
              f"Someone tried to mess with your password database"
              f"Immediately reset your Master Password and clear the database!"
              f"Run main.py clear <masterPassword>!")


def encrypt():
    if SHA256.new(sys.argv[2].encode()).hexdigest() != masterPassword:
        print("Wrong master password!")
        exit(1)

    address = SHA256.new(sys.argv[3].encode()).hexdigest().encode()
    password = sys.argv[4].encode()

    salt = os.urandom(16)
    # with open('extras', 'ab') as file:
    #     file.write(deWindowsize(salt))
    #     file.write('\n'.encode())
    # derive
    kdf = Scrypt(
        salt=salt,
        length=16,
        n=2 ** 14,
        r=4,
        p=1,
    )
    key = kdf.derive(sys.argv[2].encode())

    cipher = AES.new(key, AES.MODE_CBC, iv=address[0:16])

    cipher_password = cipher.encrypt(pad(password, AES.block_size))

    lineNumber = None
    try:
        with open('address', 'r') as file:
            if address.decode() in file.read():
                lineNumber = findAddressLineNumber(address)
    except FileNotFoundError:
        pass

    # check if address already exists in database
    if lineNumber is None:
        with open('address', 'a+') as file:
            file.write(address.decode())
            file.write('\n')

        with open('pass', 'ab+') as file:
            file.write(deWindowsize(cipher_password))
            file.write('\n'.encode())

        with open('extras', 'ab+') as file:
            file.write(deWindowsize(salt))
            file.write('\n'.encode())
    else:
        with open('pass', 'rb') as file:
            data = file.readlines()
        with open('pass', 'wb+') as file:
            data[lineNumber] = deWindowsize(cipher_password)
            data[lineNumber] += '\n'.encode()
            file.writelines(data)

        with open('extras', 'rb') as file:
            data2 = file.readlines()
        with open('extras', 'wb+') as file:
            data2[lineNumber] = deWindowsize(salt)
            data2[lineNumber] += '\n'.encode()
            file.writelines(data2)
    print('Password set!')


def init():
    with open('master', 'w+') as file:
        file.write(SHA256.new(str(sys.argv[2]).encode()).hexdigest())


def clear():
    if SHA256.new(sys.argv[2].encode()).hexdigest() != masterPassword:
        print("Wrong master password!")
        exit(1)

    os.remove('pass')
    os.remove('address')
    os.remove('master')
    os.remove('extras')
    print("Database and Master Password are now reset!")
    print("Run main.py init <masterPassword> to set your new Master Password!")


def main():
    global masterPassword
    try:
        with open('master', 'rb') as file:
            masterPassword = file.read().decode()
            if masterPassword == '' and sys.argv[1] != 'init':
                print('Master password not set. Use init command for setting it!')
                exit(1)
    except FileNotFoundError:
        init()

    cmdargs = len(sys.argv)

    if cmdargs == 3 and sys.argv[1] == 'clear':
        clear()
    elif cmdargs == 3 and sys.argv[1] == 'init':
        init()
    elif cmdargs == 5 and sys.argv[1] == 'put':
        encrypt()
    elif cmdargs == 4 and sys.argv[1] == 'get':
        decrypt()
    else:
        print('Wrong usage of arguments. Read README.md for more info!')
        exit(1)


if __name__ == '__main__':
    main()
