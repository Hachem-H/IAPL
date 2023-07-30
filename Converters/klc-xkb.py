import re

ConversionTable = '''
# First Row
TLDE OEM_3
AE01 1
AE02 2
AE03 3
AE04 4
AE05 5
AE06 6
AE07 7
AE08 8
AE09 9
AE10 0
AE11 OEM_MINUS
AE12 OEM_PLUS

# Second row
AD01 Q
AD02 W
AD03 E
AD04 R
AD05 T
AD06 Y
AD07 U
AD08 I
AD09 O
AD10 P
AD11 OEM_4
AD12 OEM_6

# Third row
AC01 A
AC02 S
AC03 D
AC04 F
AC05 G
AC06 H
AC07 J
AC08 K
AC09 L
AC10 OEM_1
AC11 OEM_7
BKSL OEM_5

# Fourth row
LSGT OEM_102
AB01 Z
AB02 X
AB03 C
AB04 V
AB05 B
AB06 N
AB07 M
AB08 OEM_COMMA
AB09 OEM_PERIOD
AB10 OEM_2
SPCE SPACE
KPDL DECIMAL
'''

output = open(r'src/IAPL.xkb', 'w')
input = open(r'src/IAPL.klc', encoding='utf-16')

klcKeyCodes = []
xkbKeyCodes = []

for line in ConversionTable.splitlines():
    line = line.strip()
    if '#' in line or len(line) == 0:
        continue

    xkbKeyCodes.append(line.split()[0])
    klcKeyCodes.append(line.split()[1])
    
for line in input:
    newline = line.rstrip()
    newlineRef = newline
    newline = re.sub(r'\w\w\t+(\w*)\t+\w*\t+([\w@]+)\t+([-\w@]+)\t+[-\w@]+\t+([-\w@]+)\t+([-\w@]+)\t+(\/\/ .*)',
                     r'\tkey <winkeycode\1> { [ \2, \3, \4, \5 ] }; \6', newline)
    newline = re.sub(r'([A-Fa-f0-9]{4}(,|\s\]))', r'U\1', newline)
    newline = re.sub(r'-1', r'NoSymbol', newline)
    
    for kl, kw in zip(xkbKeyCodes, klcKeyCodes):
        newline = newline.replace('<winkeycode%s>' %kw, '<%s>' % kl)
    if newlineRef != newline: 
        output.write('%s\n' % newline)

input.close()
output.close()
