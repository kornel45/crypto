import OpenSSL
import jks

# generate key
key = OpenSSL.crypto.PKey()
key.generate_key(OpenSSL.crypto.TYPE_RSA, 2048)

# generate a self signed certificate
cert = OpenSSL.crypto.X509()
cert.get_subject().CN = 'my.server.example.com'
cert.set_serial_number(473289472)
cert.gmtime_adj_notBefore(0)
cert.gmtime_adj_notAfter(365 * 24 * 60 * 60)
cert.set_issuer(cert.get_subject())
cert.set_pubkey(key)
cert.sign(key, 'sha256')

# dumping the key and cert to ASN1
dumped_cert = OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_ASN1, cert)
dumped_key = OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_ASN1, key)

# creating a private key entry
pke = jks.PrivateKeyEntry.new('self signed cert', [dumped_cert], dumped_key, 'rsa_raw')

# if we want the private key entry to have a unique password, we can encrypt it beforehand
# if it is not ecrypted when saved, it will be encrypted with the same password as the keystore
# pke.encrypt('my_private_key_password')

# creating a jks keystore with the private key, and saving it
keystore = jks.KeyStore.new('jks', [pke])
keystore.save('./keystore.jks', 'my_password')
