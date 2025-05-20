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

def generate_elgamal_keys(bits=10):
    """Génère une paire de clés pour le chiffrement El-Gamal."""
    # Dans une implémentation réelle, utilisez un p beaucoup plus grand
    # Pour l'exemple, on utilise un petit p
    p = random.randint(2**(bits-1), 2**bits)
    while not is_prime(p):
        p = random.randint(2**(bits-1), 2**bits)
    
    g = find_generator(p)
    
    # Clé privée
    s = random.randint(1, p-2)
    
    # Clé publique
    y = pow(g, s, p)
    
    return {
        'private_key': s,
        'public_key': {
            'p': p,
            'g': g,
            'y': y
        }
    }

def elgamal_encrypt(message, public_key):
    """Chiffre un message avec El-Gamal."""
    p = public_key['p']
    g = public_key['g']
    y = public_key['y']
    
    # Dans une vraie implémentation, assurez-vous que le message est dans [1, p-1]
    m = message % (p-1)
    
    # Générer une clé éphémère k
    k = random.randint(1, p-2)
    
    # Calculer le texte chiffré (C1, C2)
    C1 = pow(g, k, p)
    C2 = (m * pow(y, k, p)) % p
    
    return (C1, C2)

def elgamal_decrypt(ciphertext, private_key, p):
    """Déchiffre un message chiffré avec El-Gamal."""
    C1, C2 = ciphertext
    s = private_key
    
    # Calculer le message en clair: m = C2 * (C1^s)^(-1) mod p
    # (C1^s)^(-1) peut être calculé comme C1^(p-1-s) en utilisant le petit théorème de Fermat
    m = (C2 * pow(C1, p-1-s, p)) % p
    
    return m

def demonstrate_multiplicative_homomorphism(public_key, private_key, m1, m2):
    """Démontre la propriété homomorphe multiplicative d'El-Gamal."""
    p = public_key['p']
    
    # Chiffrer les deux messages séparément
    c1 = elgamal_encrypt(m1, public_key)
    c2 = elgamal_encrypt(m2, public_key)
    
    print(f"Message 1: {m1}")
    print(f"Message 2: {m2}")
    print(f"Produit des messages en clair: {(m1 * m2) % p}")
    
    # La propriété homomorphe: le produit des chiffrés correspond au chiffré du produit
    # (C1_1, C2_1) * (C1_2, C2_2) = (C1_1 * C1_2, C2_1 * C2_2)
    homomorphic_product = ((c1[0] * c2[0]) % p, (c1[1] * c2[1]) % p)
    
    print(f"Chiffré de m1: ({c1[0]}, {c1[1]})")
    print(f"Chiffré de m2: ({c2[0]}, {c2[1]})")
    print(f"Produit des chiffrés: ({homomorphic_product[0]}, {homomorphic_product[1]})")
    
    # Déchiffrer le produit homomorphe
    decrypted_product = elgamal_decrypt(homomorphic_product, private_key, p)
    
    print(f"Déchiffrement du produit des chiffrés: {decrypted_product}")
    
    # Vérifier si la propriété homomorphe fonctionne
    expected = (m1 * m2) % p
    result = decrypted_product
    
    print(f"La propriété homomorphe est vérifiée: {expected == result}")
    if expected != result:
        # Dans une vraie implémentation, cela pourrait échouer en raison des réencryptions avec différentes valeurs de k
        # Pour une démonstration correcte, il faudrait utiliser le même k pour les deux chiffrements
        print(f"Note: Dans une démonstration complète, il faudrait utiliser le même k pour les deux chiffrements")

# Exemple d'utilisation
if __name__ == "__main__":
    # Génération des clés
    keys = generate_elgamal_keys()
    private_key = keys['private_key']
    public_key = keys['public_key']
    
    p = public_key['p']
    g = public_key['g']
    y = public_key['y']
    
    print(f"Paramètres El-Gamal:")
    print(f"p = {p} (nombre premier)")
    print(f"g = {g} (générateur)")
    print(f"Clé publique y = g^s mod p = {y}")
    print(f"Clé privée s = {private_key}")
    print("-" * 50)
    
    # Démonstrer la propriété homomorphe multiplicative
    # Choisir des messages plus petits que p
    m1 = random.randint(1, p-1)
    m2 = random.randint(1, p-1)
    
    demonstrate_multiplicative_homomorphism(public_key, private_key, m1, m2)
    
    print("-" * 50)
    print("Démonstration avancée avec des valeurs de k spécifiques:")
    
    # Démonstration manuelle avec un k fixe pour montrer clairement la propriété homomorphe
    def manual_encrypt(m, k, public_key):
        p = public_key['p']
        g = public_key['g']
        y = public_key['y']
        
        C1 = pow(g, k, p)
        C2 = (m * pow(y, k, p)) % p
        
        return (C1, C2)
    
    # Utiliser le même k pour les deux chiffrements (dans la pratique, cela compromettrait la sécurité)
    k_fixed = random.randint(1, p-2)
    
    c1_fixed = manual_encrypt(m1, k_fixed, public_key)
    c2_fixed = manual_encrypt(m2, k_fixed, public_key)
    
    # Calculer le produit des chiffrés
    homomorphic_product_fixed = ((c1_fixed[0] * c2_fixed[0]) % p, (c1_fixed[1] * c2_fixed[1]) % p)
    
    # Déchiffrer le produit
    decrypted_product_fixed = elgamal_decrypt(homomorphic_product_fixed, private_key, p)
    
    print(f"Message 1: {m1}")
    print(f"Message 2: {m2}")
    print(f"Produit des messages en clair: {(m1 * m2) % p}")
    print(f"Déchiffrement du produit homomorphe (k fixe): {decrypted_product_fixed}")
    print(f"La propriété homomorphe avec k fixe est vérifiée: {(m1 * m2) % p == decrypted_product_fixed}")