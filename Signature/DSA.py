from hashlib import sha1

def modinv(a, m):
    # Inverse modulaire a⁻¹ mod m
    # Utilise l'algorithme d'Euclide étendu
    t, newt = 0, 1
    r, newr = m, a
    while newr != 0:
        quotient = r // newr
        t, newt = newt, t - quotient * newt
        r, newr = newr, r - quotient * newr
    return t % m if r == 1 else None

def hash_msg(message):
    # Hachage SHA-1 du message en entier
    return int(sha1(message.encode()).hexdigest(), 16)

# Paramètres publics (petits pour l'exemple)
p = 23
q = 11
g = 4

# Clé privée
x = 3  # x ∈ [1, q-1]

# Clé publique
y = pow(g, x, p)

# Message
message = "hello"
h = hash_msg(message) % q

# Signature
k = 6  # Choisir aléatoirement k ∈ [1, q-1] avec pgcd(k, q) = 1
r = pow(g, k, p) % q
k_inv = modinv(k, q)
s = (k_inv * (h + x * r)) % q
signature = (r, s)

# Vérification
w = modinv(s, q)
u1 = (h * w) % q
u2 = (r * w) % q
v = ((pow(g, u1, p) * pow(y, u2, p)) % p) % q
valid = (v == r)

# Affichage
print("Message :", message)
print("Hash (mod q):", h)
print("Signature (r, s):", signature)
print("Validité :", valid)
