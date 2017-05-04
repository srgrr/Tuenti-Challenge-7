import subprocess
import glob
import os
import sys

import zlib
import hashlib

def compute(secret1, secret2, iterations, user_id, old_hash):
    bignum = pow(secret1, 10000000, secret2)
    for i in range(iterations):
        if old_hash is None:
            secret3 = zlib.crc32(user_id) % 2**32
        else:
            secret3 = zlib.crc32(old_hash) % 2**32
        
        counter = (secret3 * bignum) % secret2

        password = ''

        for _ in range(10):
            counter = (counter * secret1) % secret2
            password += chr(counter % 94 + 33)

        old_hash = hashlib.md5(password).hexdigest()

    return password, old_hash


def main():
    secret_keys = {}
    '''
        Precompute all secret number pairs in order to avoid repeated disk read
    '''
    for commit in glob.iglob('201*'):
        script_name = os.path.join(commit, 'script.php')
        script_lines = open(script_name).readlines()
        magic1 = script_lines[6].split("= ")[1].split(";")[0]
        magic2 = script_lines[7].split("= ")[1].split(";")[0]
        secret_keys[os.path.split(commit)[-1]] = (int(magic1), int(magic2))
    T = int(raw_input())

    for tc in range(1, T+1):
        userid, n = raw_input().split(' ')
        n = int(n)
        last_password = ''
        old_hash = None
        for i in range(n):
            change_date, times = raw_input().split(' ')
            times = int(times)
            magic1, magic2 = secret_keys[change_date]
            last_password, old_hash = compute(magic1, magic2, times, userid, old_hash)
            old_hash.strip()
        print('Case #%d: %s'%(tc, last_password))


if __name__ == '__main__':
    main()
