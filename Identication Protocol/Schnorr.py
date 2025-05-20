import random

def schnorr_protocol():
    # Public parameters
    p = 23
    q = 11  # q divides p - 1
    g = 2   # g^q mod p = 1

    # Key generation
    x = random.randint(1, q-1)        # secret key
    y = pow(g, x, p)                  # public key

    # --- Identification protocol ---
    r = random.randint(1, q-1)
    t = pow(g, r, p)                  # commitment

    c = random.randint(1, q-1)        # challenge (normally sent by verifier)

    s = (r + c * x) % q               # response

    # Verifier checks:
    lhs = pow(g, s, p)
    rhs = (t * pow(y, c, p)) % p

    print("Verification:", lhs == rhs)

schnorr_protocol()
