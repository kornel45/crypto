from edvard_curves import EdwardsCurves


class ElGamal:
    def __init__(self, curve: EdwardsCurves, g):
        assert curve.is_on_curve(g)
        self.curve = curve
        self.g = g
        self.n = curve.order(g)

    def generate_public_key(self, private_key):
        """ Generates public key by scalar multiplication of private key and generator g """
        return self.curve.scalar_mul(private_key, self.g)

    def encrypt_point(self, p, public_key, rand):
        """
        Encrypts point. Point must be on curve
        :param p: point
        :param public_key: public key as point on curve
        :param rand: random int
        """
        assert self.curve.is_on_curve(p)
        assert self.curve.is_on_curve(public_key)
        cipher = self.curve.scalar_mul(rand, self.g), self.curve.add_points(p, self.curve.scalar_mul(rand, public_key))
        print(f'Encrypting point {p} with public key {public_key}.\nEncrypted to {cipher}')
        return cipher

    def decrypt_cipher(self, cipher, private_key):
        c1, c2 = cipher
        assert self.curve.is_on_curve(c1)
        assert self.curve.is_on_curve(c2)
        decoded = self.curve.add_points(c2, self.curve.neg(self.curve.scalar_mul(private_key, c1)))
        print(f'Decoding {cipher} with private key {private_key}.\nDecoded message {decoded}')
        return decoded
