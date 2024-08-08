import os

os.chdir(os.path.dirname(__file__))
print(str(os.getcwd()))
os.system('gnome-terminal ./python automation.py')
