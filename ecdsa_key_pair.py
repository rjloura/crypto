'''Special thanks to: https://kobl.one/blog/create-full-ethereum-keypair-and-address/
Using python2.7
requirements:
ecdsa (should be included in 2.7)
'''

from ecdsa import SigningKey
from ecdsa.curves import SECP256k1

class ECDSAKeyPair():
    def __init__(self):
        sk = SigningKey.generate(curve=SECP256k1)
        vk = sk.get_verifying_key()

        '''The x() and y() methods return the coordinates in the form of
        "0x<point>L", so we trim off the first 2 and last character.'''
        x = hex(vk.pubkey.point.x())
        y = hex(vk.pubkey.point.y())
        self.public_key = x[2:-1] + y[2:-1]
        self.private_key = hex(sk.privkey.secret_multiplier)[2:-1]

