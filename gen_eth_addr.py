'''Special thanks to: https://kobl.one/blog/create-full-ethereum-keypair-and-address/
Using python2.7
requirements:
ecdsa (should be included in 2.7)
pysha3
'''

from ecdsa import SigningKey
from ecdsa.curves import SECP256k1
import sha3

print "\n"

cont = raw_input("This script generates a public and private ECDSA key pair for use with the Ethereum blockchain. "
                 "Your Keys will be displayed on this screen once generation is complete.  Be sure to backup "
                 "your private key.  If you fail to do this, you will lose all your Ether. Are you sure you want "
                 "to continue? (Y/N) ")

if cont.upper() != "Y":
    exit(1)

tryagain = True
while (tryagain):
    sk = SigningKey.generate(curve=SECP256k1)
    vk = sk.get_verifying_key()

    # The x() and y() methods return the coordinates in the form of "0x<point>L", so we trim off the
    # first 2 and last character.
    x = hex(vk.pubkey.point.x())
    y = hex(vk.pubkey.point.y())
    public_key = x[2:-1] + y[2:-1]
    private_key = hex(sk.privkey.secret_multiplier)[2:-1]

    # Sometimes public_key.decode("hex") throws a TypeError for Odd-length string.
    # Not sure why, need to look into that.
    try:
        addr = sha3.keccak_256(public_key.decode("hex")).hexdigest()[-40:]
    except TypeError:
        continue

    tryagain = False

    print "\n1) Your Ethereum Address is: 0x{}\n".format(addr)
    print "2) Your Public Key is: \n"
    print "\t{}".format(public_key[0:32])
    print "\t{}".format(public_key[32:64])
    print "\t{}".format(public_key[64:96])
    print "\t{}\n".format(public_key[96:128])

    print "3) Your Private Key is: \n\n{}\n\tBACK THIS UP NOW!!!\n".format(private_key)

    print "To import your new Ethereum account into geth, copy your private key to a file then run:\n\t" \
          "geth account import <filename>\n"

    print "Be sure to delete <filename>.\nTo prevent loss of funds, be sure that the address returned from the geth " \
          "command matches #1 above."
