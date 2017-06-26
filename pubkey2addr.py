# A python example of how a bitcoin address is derived from the public key
# using the steps described in:
# https://en.bitcoin.it/wiki/Technical_background_of_version_1_Bitcoin_addresses
#
# This could be written more elegantly but the goal here is to understand the
# steps.

import hashlib
import base58
import sys


if len(sys.argv) is not 2:
    print "\tUsage: " + sys.argv[0] + " <public key>"
    exit(1)

# Step 1: Have the public key.  Commented below is they key from the example.
# pubkey="0450863AD64A87AE8A2FE83C1AF1A8403CB53F53E486D8511DAD8A04887E5B23522CD470243453A299FA9E77237716103ABC11A1DF38855ED6F2EE187E9C582BA6"
pubkey = sys.argv[1] 

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

print "\n" + "addr: " + step9
