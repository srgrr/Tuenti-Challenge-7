import socket
import sys
import os
import Image
import numpy as np
import glob
from scipy import signal, misc
from scipy.ndimage.morphology import binary_closing, binary_opening, binary_dilation, binary_erosion
from scipy.ndimage import sobel
from skimage.measure import label
from copy import deepcopy as dc
try:
    from skimage import filters
except ImportError:
    from skimage import filter as filters


IP_ADDRESS = '52.49.91.111'
PORT = 3456
BYTE_REQ = 10000000
PIXEL_REVERT = 40
'''
image_database = {}
for image in glob.glob('image_database/*'):
    amount = int(os.path.split(image)[-1].split('.')[0])
    image_content = misc.imread(image)
    image_database[amount] = image_content

'''

image_database = {}
image_database[1] = (53, 53)
image_database[2] = (60, 60)
image_database[10] = (64, 64)
image_database[5] = (68, 68)
image_database[20] = (70, 70)
image_database[100] = (73, 73)
image_database[50] = (77, 77)
image_database[200] = (80, 80)


'''
def get_money_amount(image_matrix):
    ret = 0
    row, col, _ = image_matrix.shape
    for (amount, pattern) in image_database.items():
        prow, pcol, _ = pattern.shape
        print row, col, prow, pcol
        for i in range(row - prow + 1):
            for j in range(col - pcol + 1):
                delta = 0.0
                for k in range(prow):
                    for l in range(pcol):
                        delta += np.linalg.norm(image_matrix[i, j, :]/255.0 - pattern[k, l, :]/255.0)
                if delta < float(prow*pcol):
                    ret += 1
            print ret
    return ret
'''

def qmain():
    image_content = misc.imread('imatge_3.jpeg')
    print get_money_amount(image_content)

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(100)
    s.connect((IP_ADDRESS, PORT))
    current_level = 0
    while True:
        image_path = 'imatge_%d.jpeg'%current_level
        f = open(image_path, 'wb')
        current_level += 1
        last_message = s.recv(BYTE_REQ)
        while not 'money' in last_message:
            print len(last_message)
            f.write(last_message)
            last_message = s.recv(BYTE_REQ)
        # append the question, it wont hurt
        f.write(last_message)
        f.close()
        preimg = misc.imread(image_path)

        img = preimg[:, :, 0]
        #img = signal.medfilt(img)
        image_content = np.array(img, dtype = np.float) / 255.0
        row, col = image_content.shape
        # revert the image
        for i in range(row):
            for j in range(40, col, 80):
                l = j
                r = min(col-1, l+39)
                env = r-l+1
                for k in range(env//2):
                    tmp = image_content[i, l+k]
                    image_content[i, l+k] = image_content[i, l+env-k-1]
                    image_content[i, l+env-k-1] = tmp

        print 'Money?'
        thresh = filters.threshold_otsu(image_content)
        to_erase = image_content < thresh
        to_preserve = image_content >= thresh
        image_content[to_erase] = 1.0
        image_content[to_preserve] = 0.0
        #image_content = binary_closing(image_content)
        image_content = np.array(image_content, dtype=np.uint8)
        labels = label(image_content)
        label_count = np.max(labels)
        answer = 0
        # (h, w, id)
        regions = []
        total_coins = 0
        for i in range(1, label_count+1):
            xwhere, ywhere = np.where(labels == i)
            height = max(xwhere) - min(xwhere) + 1
            width  = max(ywhere) - min(ywhere) + 1
            if height < 50 or width < 50: continue
            if height > 90 or width > 90: continue
            regions.append((height, width, i, xwhere, ywhere))
        regions = sorted(regions, key=lambda x: -x[0]*x[1])
        for (height, width, regionid, xwhere, ywhere) in regions:
            if np.sum(labels[min(xwhere):max(xwhere)+1, min(ywhere):max(ywhere)+1])  == 0:
                print 'Discarded region'
                continue
            pixel_count = height * width
            print 'Found a %d x %d region'%(height, width)
            smallest_diff = 10**50
            for (amount, (pwidth, pheight)) in image_database.items():
                if amount == 50 or amount  == 200:
                    half_x = (min(xwhere) + max(xwhere))//2
                    half_y = (min(ywhere) + max(ywhere))//2
                    quarter_amount = (width*height) / 4.0
                    white_ratio = np.sum(image_content[half_x:max(xwhere)+1, half_y:max(ywhere)+1]) / quarter_amount
                    print 'special coin %d found, white ratio is %f'%(amount, white_ratio)
                    thresh = 0.65
                    if amount == 50 and white_ratio > thresh:
                        continue
                    if (amount == 100 or amount == 200) and white_ratio < thresh:
                        continue
                    print 'coin is NOT rejected'
                diff_x = abs(height - pheight) / float(height)
                diff_y = abs(width - pwidth) / float(width)
                diff = np.linalg.norm(np.array([diff_x, diff_y]))
                #diff = abs((pixel_count - pheight*pwidth) / float(pheight*pwidth))
                #diff = np.linalg.norm(np.array([height - pheight, width - pwidth]))
                print 'Diff with %d coin: %f'%(amount, diff)
                if diff < smallest_diff:
                    smallest_diff = diff
                    amount_to_add = amount

            print '[IMPORTANT] Found a %d coin'%amount_to_add
            answer += amount_to_add
            total_coins += 1
            labels[min(xwhere):max(xwhere)+1, min(ywhere):max(ywhere)+1] = 0

        to_save = np.array(image_content*255.0, dtype = np.uint8)
        misc.imsave(image_path.replace('jpeg', 'png'), to_save)
        print str(answer)
        s.send(str(answer)+'\n')
        antwoord = s.recv(BYTE_REQ)
        print 'Total coins: %d'%total_coins
        print antwoord
        if 'wrong' in antwoord:
            exit(0)


if __name__ == '__main__':
    main()
