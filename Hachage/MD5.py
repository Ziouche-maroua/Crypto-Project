# -*- coding: utf-8 -*-
import math
import struct

def md5_implementation(message):
    """
    Implémentation de l'algorithme MD5 en Python
    
    Args:
        message: Message à hacher (chaîne de caractères)
        
    Returns:
        Empreinte MD5 en hexadécimal
    """
    # Définition des constantes
    s = [
        7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
        5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20,
        4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
        6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21
    ]
    
    # Constantes K basées sur le sinus
    K = [int(abs(math.sin(i + 1)) * 2**32) & 0xFFFFFFFF for i in range(64)]
    
    # Valeurs initiales des registres (petits-boutistes)
    a0 = 0x67452301
    b0 = 0xEFCDAB89
    c0 = 0x98BADCFE
    d0 = 0x10325476
    
    # Préparation du message
    # Conversion en bytes si nécessaire
    if isinstance(message, str):
        message = message.encode('utf-8')
    
    # Calcul de la longueur originale en bits
    original_bit_len = (8 * len(message)) & 0xffffffffffffffff
    
    # Padding (ajout de bits)
    # 1. Ajouter un bit '1'
    # 2. Ajouter des bits '0' jusqu'à ce que la longueur soit congrue à 448 modulo 512
    # 3. Ajouter la longueur originale sur 64 bits
    message += b'\x80'  # 0x80 = 10000000 en binaire
    
    # Ajouter des zéros jusqu'à atteindre (longueur mod 512) = 448 bits
    while (len(message) % 64) != 56:
        message += b'\x00'
    
    # Ajouter la longueur originale en bits (codée sur 64 bits en little-endian)
    message += struct.pack('<Q', original_bit_len)
    
    # Fonction auxiliaire pour les opérations bit à bit
    def F(x, y, z): return (x & y) | (~x & z)
    def G(x, y, z): return (x & z) | (y & ~z)
    def H(x, y, z): return x ^ y ^ z
    def I(x, y, z): return y ^ (x | ~z)
    
    def leftrotate(x, c):
        return ((x << c) | (x >> (32 - c))) & 0xFFFFFFFF
    
    # Pour chaque bloc de 512 bits (64 octets)
    for i in range(0, len(message), 64):
        # Extraire le bloc courant
        block = message[i:i+64]
        
        # Diviser le bloc en 16 mots de 32 bits (4 octets) en little-endian
        M = [struct.unpack("<I", block[j:j+4])[0] for j in range(0, 64, 4)]
        
        # Initialiser les registres pour ce bloc
        A, B, C, D = a0, b0, c0, d0
        
        # Traitement principal - 64 étapes (4 rondes de 16 étapes)
        for j in range(64):
            if j < 16:
                # Ronde 1
                F_result = F(B, C, D)
                g = j
            elif j < 32:
                # Ronde 2
                F_result = G(B, C, D)
                g = (5 * j + 1) % 16
            elif j < 48:
                # Ronde 3
                F_result = H(B, C, D)
                g = (3 * j + 5) % 16
            else:
                # Ronde 4
                F_result = I(B, C, D)
                g = (7 * j) % 16
            
            # Mettre à jour les registres
            temp = D
            D = C
            C = B
            B = (B + leftrotate((A + F_result + K[j] + M[g]) & 0xFFFFFFFF, s[j])) & 0xFFFFFFFF
            A = temp
        
        # Ajouter les résultats au bloc précédent
        a0 = (a0 + A) & 0xFFFFFFFF
        b0 = (b0 + B) & 0xFFFFFFFF
        c0 = (c0 + C) & 0xFFFFFFFF
        d0 = (d0 + D) & 0xFFFFFFFF
    
    # Conversion du résultat en hexadécimal (petit-boutiste)
    result = struct.pack('<4I', a0, b0, c0, d0)
    return ''.join(f'{b:02x}' for b in result)


if __name__ == "__main__":
    # Exemple d'utilisation
    passwd = input("Entrez le mot de passe à hacher : ")
    hashed = md5_implementation(passwd)
    print(f"MD5 hash: {hashed}")
    
    # Vérification avec la bibliothèque hashlib
    import hashlib
    verification = hashlib.md5(passwd.encode('utf-8')).hexdigest()
    print(f"Vérification: {verification}")
    print(f"Résultat correct: {hashed == verification}")