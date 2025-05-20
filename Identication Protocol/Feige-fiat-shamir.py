import random
from Crypto.Util import number

def feige_fiat_shamir():
    # Key generation
    p = number.getPrime(8)
    q = number.getPrime(8)
    n = p * q

    s = random.randint(2, n-1)
    v = pow(s, -2, n)  # public key

    # --- Authentication ---
    r = random.randint(2, n-1)
    x = pow(r, 2, n)

    # Verifier sends challenge
    e = random.randint(0, 1)

    # Prover computes response
    if e == 0:
        y = r
    else:
        y = (r * s) % n

    # Verifier checks
    if e == 0:
        valid = pow(y, 2, n) == x
    else:
        valid = pow(y, 2, n) == (x * v) % n

    print("Verification:", valid)

feige_fiat_shamir()
