import sys

if len(sys.argv) != 4:
    print("usage")
width = int(sys.argv[2])
height = int(sys.argv[1])

blank = []
for i in range(width):
    l = str()
    for j in range(height):
        l += '.'
        print('.', end='')
    print()
    if i != width - 1:
        l += '\n'
    blank.append(l)

with open(sys.argv[3], 'w') as f:
    f.writelines(blank)
    f.close()
