import binascii
import hashlib

def compute(secret1, secret2, iterations, user_id, old_hash):
    bignum = pow(secret1, secret2, 10000000)
    for i in range(iterations):
        if old_hash is None:
            secret3 = binascii.crc32(user_id)
        else:
            secret3 = binascii.crc32(old_hash)

        counter = (secret3 * bignum) % secret2

        password = ''

        for i in range(10):
            counter = (counter * secret1) % secret2
            password += chr(counter % 94 + 33)

        old_hash = hashlib.md5(password).hexdigest()

    return password, old_hash
