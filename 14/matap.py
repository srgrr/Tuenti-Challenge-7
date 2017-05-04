import os
import subprocess

x = subprocess.check_output(['ps -ef | grep main.py'], shell=True)

for line in x.split('\n'):
  if 'main.py' in line:
    for x in line.split(' '):
      try:
        os.system('kill -9 %s'%x)
      except:
        pass
