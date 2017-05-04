import glob



def main():
    maxf = 0
    argmax = -1
    for filename in glob.glob("attempts/*"):
        maxv = 0
        for line in open(filename).readlines():
            maxv = 0
            if 'COINS LEFT' in line:
                maxv = max(maxv, int(line.split(" ")[-1].replace('\n', '')))
                if maxv > maxf:
                    maxf = maxv
                    argmax = filename
    print "Max value of %s at file %s"%(maxf, argmax)

if __name__ == '__main__':
    main()
