"""
Usefull websites
Modular equation solver: https://www.dcode.fr/modular-equation-solver
Blog with order explaination: https://andrea.corbellini.name/2015/05/23/elliptic-curve-cryptography-finite-fields-and-discrete-logarithms/
Adding points on edwards curve: https://hyperelliptic.org/EFD/g1p/auto-edwards.html
"""
import random

from edvard_curves import EdwardsCurves
from el_gamal import ElGamal

if __name__ == '__main__':
    d = 5
    p = 17
    ec = EdwardsCurves(d, p)
    g = ec.create_point(7, 12)  # must be on edwards curve
    message = ec.create_point(12, 7)  # must be on edwards curve
    eg = ElGamal(ec, g)
    priv_key = random.randint(1, eg.n - 1)  # smaller than order of point because we don't want pub_key to be base_point
    rand_int = random.randint(1, eg.n - 1)  # does not have to be smaller than order of g
    pub_key = ec.scalar_mul(priv_key, g)  # must be on edwards curve
    encoded = eg.encrypt_point(message, pub_key, rand_int)
    decrypted = eg.decrypt_cipher(encoded, priv_key)
    assert message == decrypted
