with open("game1.txt") as f:
    file = [l.split(",") for l in f.read().splitlines()]

for i in range(1, len(file), 2):
    for j in range(0, len(file[i]), 2):
        if file[i][j] == "<":
            file[i][j] = "^"
        if file[i][j] == ">":
            file[i][j] = "v"

print(file)
# for l in file:
#     print(" ".join(l))
