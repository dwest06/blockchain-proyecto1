#!/usr/bin/python

#posiblement
from subprocess import *

# Opcion 1

# call(['gnome-terminal', '-e', "python3 ./Main.py 1"])
# call(['gnome-terminal', '-e', "python3 ./Main.py 2"])
# call(['gnome-terminal', '-e', "python3 ./Main.py 3"])

# Opcion 2

# Popen(['gnome-terminal', '-e', "python3 ./Main.py 1"])
# Popen(['gnome-terminal', '-e', "python3 ./Main.py 2"])
# Popen(['gnome-terminal', '-e', "python3 ./Main.py 3"])


# Opcion 3

cmd =['gnome-terminal',
      '--tab', '-e', 'python  ./Main.py 1',
      '--tab', '-e', 'python  ./Main.py 2',
      '--tab', '-e', 'python  ./Main.py 3']
call(cmd)
