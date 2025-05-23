def KSA(key):
    key_length = len(key)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]
    return S

def PRGA(S):
    i = j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        yield K

def RC4(key, data):
    # Convertir la clé en liste d'entiers
    key = [ord(c) for c in key]
    S = KSA(key)
    keystream = PRGA(S)
    return bytes([c ^ next(keystream) for c in data])

# Exemple
key = "ceryne2"
plaintext = b"HELLO CRYPTO"
ciphertext = RC4(key, plaintext)
print("Chiffré :", ciphertext)

# Pour déchiffrer, on applique RC4 à nouveau avec la même clé
decrypted = RC4(key, ciphertext)
print("Déchiffré :", decrypted)
