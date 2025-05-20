# -*- coding: utf-8 -*-
import random
import hashlib
from math import gcd

def is_prime(n):
    """Vérifie si un nombre est premier (méthode simple pour l'exemple)."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def find_generator(p):
    """Trouve un générateur g du groupe multiplicatif Z_p*."""
    if not is_prime(p):
        raise ValueError("p doit être premier")
    
    # Pour un petit p, on peut faire une recherche exhaustive
    phi = p - 1  # Fonction d'Euler pour un nombre premier
    
    # Factorisation de phi (dans une implémentation réelle, utilisez une méthode plus efficace)
    factors = []
    n = phi
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            factors.append(i)
            while n % i == 0:
                n //= i
    if n > 1:
        factors.append(n)
    
    # Chercher un générateur
    for g in range(2, p):
        is_generator = True
        for factor in factors:
            if pow(g, phi // factor, p) == 1:
                is_generator = False
                break
        if is_generator:
            return g
    
    return None  # Aucun générateur trouvé (ne devrait pas arriver si p est premier)

def extended_gcd(a, b):
    """Algorithme d'Euclide étendu pour trouver gcd(a, b) et les coefficients de Bézout."""
    if a == 0:
        return (b, 0, 1)
    else:
        gcd, x, y = extended_gcd(b % a, a)
        return (gcd, y - (b // a) * x, x)

def mod_inverse(a, m):
    """Calcule l'inverse modulaire de a modulo m."""
    gcd, x, y = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("L'inverse modulaire n'existe pas")
    else:
        return x % m

def generate_elgamal_keys(bits=10):
    """Génère une paire de clés pour la signature El-Gamal."""
    # Dans une implémentation réelle, utilisez un p beaucoup plus grand
    # Pour l'exemple, on utilise un petit p
    p = random.randint(2**(bits-1), 2**bits)
    while not is_prime(p):
        p = random.randint(2**(bits-1), 2**bits)
    
    g = find_generator(p)
    
    # Clé privée
    x = random.randint(1, p-2)
    
    # Clé publique
    y = pow(g, x, p)
    
    return {
        'private_key': x,
        'public_key': {
            'p': p,
            'g': g,
            'y': y
        }
    }

def elgamal_sign(message, private_key, public_key):
    """Génère une signature El-Gamal pour un message."""
    p = public_key['p']
    g = public_key['g']
    x = private_key
    
    # Hacher le message pour obtenir un entier
    hash_obj = hashlib.sha256(message.encode())
    h = int(hash_obj.hexdigest(), 16) % (p-1)
    
    # Choisir un k aléatoire tel que gcd(k, p-1) = 1
    k = random.randint(1, p-2)
    while gcd(k, p-1) != 1:
        k = random.randint(1, p-2)
    
    # Calculer r = g^k mod p
    r = pow(g, k, p)
    
    # Calculer s = k^(-1) * (h - x*r) mod (p-1)
    k_inv = mod_inverse(k, p-1)
    s = (k_inv * (h - x * r)) % (p-1)
    
    return (r, s)

def elgamal_verify(message, signature, public_key):
    """Vérifie une signature El-Gamal."""
    p = public_key['p']
    g = public_key['g']
    y = public_key['y']
    r, s = signature
    
    # Vérifier que 0 < r < p et 0 < s < p-1
    if r <= 0 or r >= p or s <= 0 or s >= p-1:
        return False
    
    # Hacher le message pour obtenir un entier
    hash_obj = hashlib.sha256(message.encode())
    h = int(hash_obj.hexdigest(), 16) % (p-1)
    
    # Vérifier que y^r * r^s ≡ g^h (mod p)
    left_side = (pow(y, r, p) * pow(r, s, p)) % p
    right_side = pow(g, h, p)
    
    return left_side == right_side

# Exemple d'utilisation
if __name__ == "__main__":
    # Génération des clés
    keys = generate_elgamal_keys()
    private_key = keys['private_key']
    public_key = keys['public_key']
    
    print(f"Clé publique: p={public_key['p']}, g={public_key['g']}, y={public_key['y']}")
    print(f"Clé privée: x={private_key}")
    
    # Message à signer
    message = "Bonjour, ceci est un message à signer avec El-Gamal."
    
    # Signature
    signature = elgamal_sign(message, private_key, public_key)
    print(f"Signature: r={signature[0]}, s={signature[1]}")
    
    # Vérification
    is_valid = elgamal_verify(message, signature, public_key)
    print(f"La signature est valide: {is_valid}")
    
    # Test avec un message modifié
    modified_message = message + " Modification!"
    is_valid = elgamal_verify(modified_message, signature, public_key)
    print(f"La signature est valide pour le message modifié: {is_valid}")