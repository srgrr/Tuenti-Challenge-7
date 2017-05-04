import sys
import os



def main():
  for i in range(1000):
    print 'Attempt %d'%i
    os.system('python main2.py > attempts/%d'%(i))

if __name__ == '__main__':
  main()