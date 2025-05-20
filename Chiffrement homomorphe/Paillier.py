from phe import paillier

def generate_keys():
    public_key, private_key = paillier.generate_paillier_keypair()
    return public_key, private_key

def encrypt(public_key, plaintext):
    return public_key.encrypt(plaintext)

def decrypt(private_key, ciphertext):
    return private_key.decrypt(ciphertext)

def homomorphic_add(c1, c2):
    return c1 + c2

def homomorphic_mult(ciphertext, constant):
    return ciphertext * constant

# Exemple d'utilisation
if __name__ == "__main__":
    # Génération des clés
    pub_key, priv_key = generate_keys()

    # Messages à chiffrer
    m1 = 10
    m2 = 20
    k = 5

    # Chiffrement
    c1 = encrypt(pub_key, m1)
    c2 = encrypt(pub_key, m2)

    # Opérations homomorphes
    c_sum = homomorphic_add(c1, c2)
    c_mult = homomorphic_mult(c1, k)

    # Déchiffrement des résultats
    decrypted_sum = decrypt(priv_key, c_sum)
    decrypted_mult = decrypt(priv_key, c_mult)

    # Affichage
    print("Message 1:", m1)
    print("Message 2:", m2)
    print("Somme chiffrée (déchiffrée):", decrypted_sum)
    print("Multiplication homomorphe (déchiffrée):", decrypted_mult)
