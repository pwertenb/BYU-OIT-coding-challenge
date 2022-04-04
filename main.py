# main source file

import sys

# these two constants are used to throw different errors
# ex: throw NumeralException(num, INVALID_CHARACTER)
INVALID_CHARACTER = "At least one character is not a roman numeral."
INVALID_PRECEDENCE = "A symbol representing 10x precedes a symbol greater than 10x+1."

# custom exception to deal with invalid strings
class NumeralException(Exception):
    err = ""
    num = ""

    def __init__(self, num, err, *args):
        super().__init__(args)
        self.num = num
        self.err = err

    def __str__(self):
        return f'Error converting numeral {self.num}: {self.err}'


# dictionary to give each letter its value
letters = {
    "I": 1,
    "V": 5,
    "X": 10,
    "L": 50,
    "C": 100,
    "D": 500,
    "M": 1000
}

# roman numerals to decimal
def roman_to_decimal(num):
    # capitalize entire string
    num = num.upper()

    # check if entire numeral is valid
    for i in range(len(num)-1):
        # check if letter is a numeral
        if num[i] not in letters.keys():
            raise NumeralException(num, INVALID_CHARACTER)

        # check if letter is in a valid order
        if letters[num[i]] * 10 < letters[num[i+1]]:
            raise NumeralException(num, INVALID_PRECEDENCE)
    # check last character
    if num[-1] not in letters.keys():
        raise NumeralException(num, INVALID_CHARACTER)


    # loop from beginning to second to last symbol
    result = 0
    for i in range(len(num)-1):
        # if value is less than next num, subtract it instead of adding it
        if letters[num[i]] < letters[num[i+1]]:
            result -= letters[num[i]]

        # else add normally
        else:
            result += letters[num[i]]

    # add last symbol
    result += letters[num[-1]]

    return result

def test_roman_to_decimal():
    # testing roman to decimal conversion
    tests = ["III", "VII", "CLXV", "IV", "XL", "XC", "XIV", "XCIV", "MMMCMXCIX"]
    answers = [3, 7, 165, 4, 40, 90, 14, 94, 3999]

    # testing loop
    try:
        for i in range(len(tests)):
            print("testing:", tests[i])
            result = roman_to_decimal(tests[i])
            if result == answers[i]:
                print("     passed!")
            else:
                print("     expected:", answers[i], "got:", result)
    except NumeralException as ex:
        print(ex)

# decimal to roman numerals
def decimal_to_roman(num):
    result = ""

    # iterate through numerals in dictionary backwards until last two
    keys = list(letters.keys())
    keys.reverse()
    for i in range(len(keys)):
        # add value until would be greater than num
        while num - letters[keys[i]] >= 0:
            num -= letters[keys[i]]
            result += keys[i]

        # append closest possible subtraction numeral (except if last symbol)
        j = 0
        if i < len(keys)-1:
            # keep finding next closest numeral
            while num - (letters[keys[i]] - letters[keys[i+j+1]]) >= 0:
                j += 1
                if j >= 2 or i+j+1 >= len(keys):
                    break

        # edge case of equivalent numerals (ex. VX == V)
        if num - (letters[keys[i]] - letters[keys[i+j]]) == num - letters[keys[i+j]]:
            j = 0

        # if j has any effect, append subtraction numeral
        if j > 0:
            num -= (letters[keys[i]] - letters[keys[i+j]])
            result += keys[i+j]
            result += keys[i]

    return result

def test_decimal_to_roman():
    # testing roman to decimal conversion
    tests = [3, 7, 165, 4, 40, 90, 14, 94, 3999]
    answers = ["III", "VII", "CLXV", "IV", "XL", "XC", "XIV", "XCIV", "MMMCMXCIX"]

    # testing loop
    try:
        for i in range(len(tests)):
            print("testing:", tests[i])
            result = decimal_to_roman(tests[i])
            if result == answers[i]:
                print("     passed!")
            else:
                print("     expected:", answers[i], "got:", result)
    except NumeralException as ex:
        print(ex)


# main function
def main():
    #test_roman_to_decimal()
    #test_decimal_to_roman()

    if sys.argv[1] == "rtod":
        print("Roman numeral", sys.argv[2], "to decimal:", roman_to_decimal(sys.argv[2]))
    elif sys.argv[1] == "dtor":
        print("Decimal", sys.argv[2], "to Roman numeral:", decimal_to_roman(int(sys.argv[2])))
    else:
        print(sys.argv[1], "is an invalid command. Options are rtod (Roman numeral to decimal) or dtor (decimal to Roman numeral)")

if __name__ == "__main__":
    main()
