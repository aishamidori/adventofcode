import re
import sys

REQ_FIELDS = [
    ['byr', lambda val: (len(val) == 4 and int(val) >= 1920 and int(val) <= 2002)],
    ['iyr', lambda val: (len(val) == 4 and int(val) >= 2010 and int(val) <= 2020)],
    ['eyr', lambda val: (len(val) == 4 and int(val) >= 2020 and int(val) <= 2030)],
    ['hgt', lambda val: ((val[-2:] == 'cm' and int(val[:-2]) in range(150,194)) or (val[-2:] == 'in' and int(val[:-2]) in range(59, 77)))],
    ['hcl', lambda val: re.match(r'^#(\d|[a-f]){6}$', val)],
    ['ecl', lambda val: (val in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'])],
    ['pid', lambda val: re.match(r'^[\d]{9}$', val)],
]

def isValid(passport):
    for field_tuple in REQ_FIELDS:
        field = field_tuple[0]
        validation = field_tuple[1]
        if not field in passport.keys() or not validation(passport[field]):
            print '\nINVALID (' + field + ': ' + (passport[field] if field in passport else "EMPTY") + ')'
            return False

    print '\nVALID'
    print passport
    return True

def process(inputFile):
    passports = []
    validPassports = 0
    currPassport = {}
    for line in inputFile:
        print line
        if line == '\n':
            if isValid(currPassport):
                validPassports = validPassports + 1
            passports.append(currPassport)
            currPassport = {}
        else:
            fields = line.split(' ')
            for field in fields:
                splitField = field.strip().split(':')
                currPassport[splitField[0]] = splitField[1]

    if isValid(currPassport):
        validPassports = validPassports + 1
    passports.append(currPassport)
    currPassport = {}

    print "Total Count: " + str(len(passports))
    print "Total Valid: " + str(validPassports)

if __name__ == "__main__":
    if not len(sys.argv) > 1:
        print "Please provide a file argument"
    else:
        inputFile = open(sys.argv[1])
        process(inputFile)
