passwordFile = open('input.txt')
numValid = 0
for line in passwordFile:
    tmp = line.split(' ')
    (minCount, maxCount) = tmp[0].split('-')
    reqLetter = tmp[1][:-1]
    pwd = tmp[2]

    print line
    print len(pwd)
    print int(minCount)
    print int(maxCount)
    if (pwd[int(minCount)-1] == reqLetter) is not (pwd[int(maxCount)-1] == reqLetter):
        numValid = numValid + 1
        print 'found a valid password'
        print line

print numValid
