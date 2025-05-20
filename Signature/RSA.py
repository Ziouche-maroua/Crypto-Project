import hashlib

def hacher(message):
    """
    Hash d’un message texte avec SHA-256.
    Retourne un entier.
    """
    h = hashlib.sha256(message.encode()).hexdigest()
    return int(h, 16)

def signer_message(message, d, n):
    """
    Signature RSA du hash d’un message avec clé privée (d, n).
    Retourne la signature.
    """
    h = hacher(message)
    return pow(h, d, n)

def verifier_signature(message, signature, e, n):
    """
    Vérifie la signature RSA avec la clé publique (e, n).
    Retourne True si valide, sinon False.
    """
    h = hacher(message)
    h_verif = pow(signature, e, n)
    return h == h_verif

message = "Bonjour"
d=851
n=1643
e=11
signature = signer_message(message, d, n)
print(f"Signature : {signature}")

valide = verifier_signature(message, signature, e, n)
print("✔️ Signature valide" if valide else "❌ Signature invalide")
