# keytool -genkey -alias mydomain -keyalg RSA -keypass pass -storepass pass -keystore KeyStore.jks -keysize 2048
import base64
import sys
import textwrap
from random import randint
import os
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
    return "".join([chr(ord(a) ^ ord(b)) for a, b in zip(str1, str2)])


def increment_iv(iv):
    return format(int(iv, 2) + 1, '016b')


def which_msg(enc_type, key, iv, msg_list, enc_msg):
    iv2 = increment_iv(iv)
    encryptor = OpenSSL(enc_type)
    for i, m in enumerate(msg_list):
        xored = xor_strings(xor_strings(iv, iv2), m)
        enc_m = encryptor.encrypt_msg(xored, key, iv2)
        if enc_m == enc_msg:
            return i, enc_m


def test_mode(file_to_encrypt, mode):
    open_ssl = OpenSSL(mode)
    encrypted_path = file_to_encrypt.replace('.py', '.enc')
    open_ssl.encrypt_file(key, bytes(iv, 'utf-8'), file_to_encrypt, encrypted_path)
    decrypted_path = file_to_encrypt.replace('.py', '.dec')
    open_ssl.decrypt_file(key, bytes(iv, 'utf-8'), encrypted_path, decrypted_path)
    with open(file_to_encrypt, 'rb') as original:
        with open(decrypted_path, 'rb') as decrypted:
            assert original.read() == decrypted.read()

    os.remove(decrypted_path)
    os.remove(encrypted_path)
    print('Test for {} passed'.format(mode))


if __name__ == '__main__':
    command_line_parser = CommandLineParser()
    parsed_args = command_line_parser.parse_arguments(sys.argv[1:])

    enc_type = 'cbc'
    openssl = OpenSSL(enc_type)
    iv = '0' * 16
    iv2 = increment_iv(iv)
    ks = jks.KeyStore.load(parsed_args['keystore_path'], parsed_args['password'])
    key = ks.private_keys['self signed cert'].pkey[:32]

    msg_list = ['lubie placki bar', 'pala lufa jedyna']
    msg_list = [x[:16] for x in msg_list]
    rand = randint(0, 1)
    random_msg = msg_list[rand]

    enc_m1 = openssl.encrypt_msg(random_msg, key, iv)
    print('Encrypting "{}" to {}'.format(random_msg, enc_m1))

    ind, cipher = which_msg(enc_type, key, iv, msg_list, enc_m1)
    print('"{}" was encrypted to: {}'.format(msg_list[ind], cipher))

    test_mode('command_line_parser.py', 'cbc')
    test_mode('command_line_parser.py', 'ofb')
    test_mode('command_line_parser.py', 'ctr')
