# exception thrown if code word isn't binary
import sys


class NotBinaryError(Exception):
    pass


def print_lines():
    print("-------------------------------------------------------------------------")


def list_to_string(s):
    string = ""

    for el in s:
        string += el

    return string


def is_power_of_two(x):
    return x and (not (x & (x - 1)))


def check_if_binary(num):
    for i in str(num):
        if i not in ("0", "1"):
            return False
    return True


# function for taking input
def take_input():
    global n, c, k
    try:
        n = int(input("n = "))
        if n <= 0:
            raise ValueError

        k = int(input("k = "))
        if k <= 0:
            raise ValueError

        c = input("c = ")

        if not check_if_binary(c):
            raise NotBinaryError

        if len(c) != n:
            print("Code word has to be of length n!\n")
            take_input()

    except ValueError:
        print("Wrong input! Please try again.\n")
        take_input()
    except NotBinaryError:
        print("Code word has to be binary!\n")
        take_input()

    return n, k, c


def calculate_no_of_parity_bits(n, k):
    return n - k


def error_detection(x, y):
    syndrome = []

    print_lines()
    print("SYNDROME CALCULATION")

    for i in range(len(x)):
        if is_power_of_two(i):
            if i == 1:
                print(f"Parity bits at position {i}: {x[i - 1]} XOR {y[i - 1]} = {int(x[i - 1]) ^ int(y[i - 1])}   ᐱ")
            else:
                print(f"Parity bits at position {i}: {x[i - 1]} XOR {y[i - 1]} = {int(x[i - 1]) ^ int(y[i - 1])}   ⎹")
            syndrome.append(str(int(x[i - 1]) ^ int(y[i - 1])))

    # return value is decimal form of found syndrome
    return int(list_to_string(syndrome[::-1]), 2)


# printing decoded word
def decoded_word(msg):
    help_list = ['0']
    help_list.extend(msg)

    real_msg = []

    for i in range(1, len(help_list)):

        if not is_power_of_two(i):
            real_msg.append(help_list[i])

    print_lines()
    print("Decoded word is", list_to_string(real_msg))


def error_correction(syndrome, list1):
    try:
        if list1[syndrome - 1] == "0":
            list1[syndrome - 1] = "1"
        else:
            list1[syndrome - 1] = "0"
    except IndexError as err:
        print("\n***** In the code word there are 2 or more errors found that cannot be corrected! *****\n", file=sys.stderr)

    print_lines()
    print("Correct message is:", list_to_string(list1))

    return list_to_string(list1)


# function for re-encoding the received code word
def encode_Hamming(x, m):
    for i in range(0, m):
        count = 0
        real_pos = 2 ** i
        pos = real_pos - 1

        while pos < x.__len__():
            for j in range(pos, real_pos + pos):
                if j >= x.__len__():
                    break
                if x[j] == "1":
                    count += 1

            pos = pos + 2 * real_pos

        if count % 2 == 0:
            x[real_pos - 1] = "0"
        else:
            x[real_pos - 1] = "1"

    print_lines()
    print("Re-encoded message is:", list_to_string(x))

    return x


def decode_Hamming(c, m):
    x = list(c)

    # setting 0s at positions of parity bits (1, 2, 4, 8...)
    for i in range(0, len(c)):
        if not is_power_of_two(i):
            x[i - 1] = c[i - 1]
        else:
            x[i - 1] = "0"

    encode_Hamming(x, m)

    # received code word c and re-encoded word x are being compared
    # in order to find possible errors in the word c
    syndrome = error_detection(list(c), x)

    # if the syndrome is found, it is send to correct itself
    print(f"\nSyndrome is: {bin(syndrome)[2:]} (binary) or {syndrome} (decimal), i.e.")

    if syndrome != 0:
        print(f"the error is located at {syndrome}. bit in the received code word c!")
        real_msg = error_correction(syndrome, list(c))
        decoded_word(real_msg)
    else:
        print("the message is received without errors!")
        decoded_word(list(c))


def main():
    print("*** Application works for Hamming codes with the distance of 3 (even parity) only! ***\n")

    print("Enter the Hamming code parameters n and k and the arbitrary code word c:")
    n, k, c = take_input()
    m = calculate_no_of_parity_bits(n, k)
    decode_Hamming(c, m)


if __name__ == '__main__':
    main()
    input("\nPress any button to exit...")
