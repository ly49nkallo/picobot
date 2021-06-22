import sys

if len(sys.argv) != 4:
    print("usage")
width = int(sys.argv[2])
height = int(sys.argv[1])

blank = []
for i in range(width):
    l = str()
    for j in range(height):
        if j in {0, (height - 1)}:
            l += '#'
            print('#', end='')
        else:
            l += '.'
            print('.', end='')
    print()
    if i != width - 1:
        l += '\n'
    blank.append(l)
l = str()
for item in range(height):
    l += '#'
l += '\n'
blank[0] = l
blank[width - 1] = l



with open(sys.argv[3], 'w') as f:
    f.writelines(blank)
    f.close()
