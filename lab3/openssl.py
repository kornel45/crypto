import hashlib
import os
import struct
from Crypto.Cipher import AES


class OpenSSL:
    def __init__(self, mode):
        self.iv = 16 * '\x00'
        self.mode = {'cbc': AES.MODE_CBC, 'ofb': AES.MODE_OFB, 'ctr': AES.MODE_CTR}[mode]

    def encrypt_msg(self, msg, key, iv):
        iv = bytes(iv.encode())
        msg = bytes(msg.encode())
        if len(key) % 16:
            key = hashlib.sha256(key).digest()
        while len(msg) % 16 != 0:
            msg += b'\x00'
        encryptor = AES.new(key, self.mode, iv)

        return encryptor.encrypt(msg)

    def decrypt_msg(self, msg, key, iv):
        iv = bytes(iv.encode())
        if len(key) % 16 != 0:
            key = hashlib.sha256(key).digest()
        decryptor = AES.new(key, self.mode, iv)
        return decryptor.decrypt(msg)

    def encrypt_file(self, key, iv, in_filename, out_filename=None, chunksize=64 * 1024):
        if len(key) % 16:
            key = hashlib.sha256(key).digest()
        if not out_filename:
            out_filename = in_filename + '.enc'

        # iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
        encryptor = AES.new(key, AES.MODE_CBC, iv)
        filesize = os.path.getsize(in_filename)

        with open(in_filename, 'rb') as infile:
            with open(out_filename, 'wb') as outfile:
                outfile.write(struct.pack('<Q', filesize))
                outfile.write(iv)
                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += b' ' * (16 - len(chunk) % 16)

                    outfile.write(encryptor.encrypt(chunk))

    def decrypt_file(self, key, iv, in_filename, out_filename=None, chunksize=24 * 1024):
        """ Decrypts a file using AES (CBC mode) with the
            given key. Parameters are similar to encrypt_file,
            with one difference: out_filename, if not supplied
            will be in_filename without its last extension
            (i.e. if in_filename is 'aaa.zip.enc' then
            out_filename will be 'aaa.zip')
        """
        if not out_filename:
            out_filename = os.path.splitext(in_filename)[0]

        with open(in_filename, 'rb') as infile:
            origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
            iv = infile.read(16)
            decryptor = AES.new(key, AES.MODE_CBC, iv)

            with open(out_filename, 'wb') as outfile:
                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    outfile.write(decryptor.decrypt(chunk))

                outfile.truncate(origsize)

