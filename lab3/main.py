# keytool -genkey -alias mydomain -keyalg RSA -keystore KeyStore.jks -keysize 2048
import base64
import sys
import textwrap
from random import randint

import jks

from command_line_parser import CommandLineParser
from openssl import OpenSSL


def print_pem(der_bytes, typ):
    print("-----BEGIN %s-----" % typ)
    print("\r\n".join(textwrap.wrap(base64.b64encode(der_bytes).decode('ascii'), 64)))
    print("-----END %s-----" % typ)


def encrypt_msgs(encryptor, msg_list, key, iv):
    result = []
    for msg in msg_list:
        enc = encryptor.encrypt_msg(msg, key, iv)
        iv = increment_iv(iv)
        result.append(enc)
    return result


def xor_strings(str1, str2):
    xored = "".join([chr(ord(a) ^ ord(b)) for a, b in zip(str1, str2)])
    return xored


def increment_iv(iv):
    iv = bin(int(iv, 2) + 1)[2:]
    return '0' * (16 - len(iv)) + iv


def which_msg(enc_type, key, iv, msg_list, enc_msg):
    iv2 = increment_iv(iv)
    encryptor = OpenSSL(enc_type)
    for i, m in enumerate(msg_list):
        xored = xor_strings(xor_strings(iv, iv2), m)
        enc_m = encryptor.encrypt_msg(xored, key, iv2)
        if enc_m == enc_msg:
            return i, enc_m


if __name__ == '__main__':
    command_line_parser = CommandLineParser()
    parsed_args = command_line_parser.parse_arguments(sys.argv[1:])

    enc_type = 'cbc'
    openssl = OpenSSL(enc_type)
    iv = '0' * 16
    iv2 = increment_iv(iv)
    ks = jks.KeyStore.load(parsed_args['keystore_path'], parsed_args['password'])
    key = ks.private_keys['mydomain'].pkey[:32]

    msg_list = ['lubie placki bar', 'pala lufa jedyna']
    msg_list = [x[:16] for x in msg_list]
    rand = randint(0, 1)
    random_msg = msg_list[rand]

    enc_m1 = openssl.encrypt_msg(random_msg, key, iv)
    print('Encrypting "{}" to "{}"'.format(random_msg, enc_m1))

    ind, cipher = which_msg(enc_type, key, iv, msg_list, enc_m1)
    print('"{}" was encrypted to: {}'.format(msg_list[ind], cipher))

