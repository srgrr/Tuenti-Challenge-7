import os
import sys

def main():
    for i in range(10000000):
        for j in range(6):
            os.system('python main.py %d > attempts/%d_%d.txt &'%(j, i, j))
	os.system('python main.py 6 > attempts/%d_6.txt'%i)

if __name__ == '__main__':
    main()
