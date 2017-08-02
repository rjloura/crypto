# A python example of how a bitcoin address is derived from the public key
# using the steps described in:
# https://en.bitcoin.it/wiki/Technical_background_of_version_1_Bitcoin_addresses
#
# This could be written more elegantly but the goal here is to understand the
# steps.

import hashlib
import base58
import sys
import qrcode
from ecdsa_key_pair import ECDSAKeyPair

wallet = False

#should be a class method btcwallet to extend ecdsakeypair
def privatekey2wif(sk):
    '''convernt private key in hex string format to BTC WIF'''
    sk = '80' + sk
    h = hashlib.sha256(hashlib.sha256(sk.decode('hex')).digest()).hexdigest()
    sk = sk + h[:8]

    return base58.b58encode(sk.decode('hex'))

again = True
while (again):
    if len(sys.argv) == 2:
        pubkey = sys.argv[1] 
    elif len(sys.argv) == 1:
        e = ECDSAKeyPair()
        pubkey = e.public_key
        wallet = True
    else:
        print "Usage"
        
    pubkey = '04' + pubkey

    if len(pubkey) % 2 != 0:
        if wallet == True:
            continue
        print "Error: Odd length public key"
        exit()
    again = False

    # Step 2: Perform sha256 hash on public key
    step2 = hashlib.sha256(pubkey.decode("hex")).hexdigest()

    # Step 3: Perform Ripemd-160 hash on result of step 2
    h = hashlib.new('ripemd160')
    h.update(step2.decode('hex'))
    step3 = h.hexdigest()

    # Step 4: Add version byte
    step4 = '00' + step3

    # Step 5: Perform SHA256 on Step 4
    step5 = hashlib.sha256(step4.decode("hex")).hexdigest()

    # Step 6: Perform SHA256 on Step 5
    step6 = hashlib.sha256(step5.decode("hex")).hexdigest()

    # Step 7: The last 4 bytes are the checksum
    step7 = step6[0:8]

    # Step 8: Append checksum from step 7 to ripemd-160 hash from step 4
    step8 = step4 + step7

    # Step9: base58 encode step8, this is your address
    step9 = base58.b58encode(step8.decode('hex'))

    print "\n"
    if wallet:
        print "Private Key: {}".format(e.private_key)
        private_wif = privatekey2wif(e.private_key) 
        print "Private Key in WIF: {}\n".format(private_wif)
        img = qrcode.make(private_wif)
        img.save('wallet.png')
        print "Private Key QR code saved at wallet.png, scan this to import wallet."


    print "\nPublic Key: {}".format(pubkey)
    print "Bitcoin Address: " + step9
