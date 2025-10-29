print("----------------")
for i in range(150):
    if i % 3:
        print("carlos")
    else:
        print("wiener")

print("----------------")
with open("passwd.txt", "r") as f:
    lines = f.readlines()

i = 0
for pwd in lines:
    if i % 3:
        print(pwd.strip())
    else:
        print("peter")
        print(pwd.strip('\n'))
        i += 1
    i += 1