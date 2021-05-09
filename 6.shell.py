import subprocess

while True:
    cmd = input('shell> ')
    if cmd == 'exit':
        break
    print(subprocess.getoutput(cmd))
