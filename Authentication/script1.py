with open("passwd.txt", "r") as f:
    lines = f.readlines()

for pwd in lines:
    print('"' + pwd.strip("\n") + '",', end='\n')
    