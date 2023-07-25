repeat = 'y'
while repeat == 'y':
    with open("main.py") as f:
        exec(f.read())
    repeat = input("Would you like to run again? (y/n) ")