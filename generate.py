import sys
import picobot

if len(sys.argv not in {2,3}):
    print("usage")
    sys.exit()
width = picobot.WIDTH
height = picobot.HEIGHT

blank = []
for i in range(height):
    l = str()
    for j in range(width):
        if i in {0, (height - 1)} or j in {0, (width - 1)}:
            l += '#'
            print('#', end='')
        else:
            l += '.'
            print('.', end='')
    print()

    if i != height - 1:
        l += '\n'
    blank.append(l)
'''
l = str()
for item in range(width):
    l += '#'

blank[0] = l
blank[0] += '\n'
blank[height - 1] = l
'''


with open(sys.argv[1], 'w') as f:
    f.writelines(blank)
    f.close()
