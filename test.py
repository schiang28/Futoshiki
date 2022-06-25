with open("game1.txt") as f:
    file = f.read().splitlines()
    file = [l.split(",") for l in file]

for l in file:
    print(l)

for i in range(1, len(file), 2):
    for j in range(0, len(file[i]), 2):
        if file[i][j] == "<":
            file[i][j] = "^"
        if file[i][j] == ">":
            file[i][j] = "v"

print()

for l in file:
    print(l)
