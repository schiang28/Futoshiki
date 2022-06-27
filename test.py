with open("game1.txt") as f:
    file = [l.split(",") for l in f.read().splitlines()]

for i in range(1, len(file), 2):
    for j in range(0, len(file[i]), 2):
        if file[i][j] == "<":
            file[i][j] = "^"
        if file[i][j] == ">":
            file[i][j] = "v"

with open("game1.txt") as f:
    f = [l.split(",") for l in f.read().splitlines()]
print(f)
print(file)


def check():
    for i in range(len(f)):
        for j in range(len(f[i])):
            if f[i][j] != file[i][j] and (
                f[i][j] not in [">", "<", "^", "v"]
                or file[i][j] not in [">", "<", "^", "v"]
            ):
                return False
    return True


print(check())
