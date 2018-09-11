from subprocess import Popen, PIPE
import os
import time


process = Popen(['/usr/local/bin/python3', '/Users/bermudez/Documents/personal/gitprojects/ise/main.py'], stdout=PIPE, stderr=PIPE, env=os.environ)
while True:
    stdout, stderr = process.communicate()
    print(stdout)
    print(stderr)
    time.sleep(5)
