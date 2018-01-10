hgt = int(input("Enter desired prymid height: "))

while True:
    if hgt > 0 or hgt <= 23:
        break
for h in range(hgt+1):
    space = hgt - h
    print(" " * space +"#" * h+"  "+"#" * h)
