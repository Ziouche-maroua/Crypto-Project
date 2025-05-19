# -*- coding: utf-8 -*-
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import dh
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import random
import math
from sympy import mod_inverse, isprime

class ElGamalCipher:
    def __init__(self, key_size=1024):
        """
        Initialise le chiffreur ElGamal et génère une paire de clés
        
        Args:
            key_size: Taille de clé en bits (par défaut 1024)
        """
        # Génération des paramètres (p, g)
        self.p = self._generate_prime(key_size)
        self.g = self._find_generator(self.p)
        
        # Génération de la clé privée (a)
        self.private_key = random.randint(2, self.p - 2)
        
        # Calcul de la clé publique (g^a mod p)
        self.public_key = pow(self.g, self.private_key, self.p)
    
    def _generate_prime(self, bits):
        """
        Génère un nombre premier de taille spécifiée
        Pour une implémentation plus simple, nous utilisons une approche basique
        Pour une implémentation réelle, il faudrait utiliser des méthodes plus robustes
        """
        # Pour simplifier, nous générons un nombre premier via sympy
        # (Dans une implémentation réelle, on utiliserait les paramètres DH standards)  
        p = random.getrandbits(bits)
        while not isprime(p):
            p = random.getrandbits(bits)
        return p
    
    def _find_generator(self, p):
        """
        Trouve un générateur dans le groupe multiplicatif de Z/pZ
        Pour simplifier, nous utilisons 2 ou 3 comme générateur
        """
        # Dans une implémentation réelle, il faudrait vérifier si c'est un générateur
        return 3
    
    def encrypt(self, plaintext):
        """
        Chiffre un message avec ElGamal
        
        Args:
            plaintext: Le message à chiffrer (entier)
            
        Returns:
            Tuple (c1, c2) représentant le texte chiffré
        """
        # Vérifier que le message est dans le bon format
        if isinstance(plaintext, str):
            plaintext = int.from_bytes(plaintext.encode('utf-8'), byteorder='big')
        
        # Vérifier que le message est plus petit que p
        if plaintext >= self.p:
            raise ValueError("Le message est trop grand pour être chiffré avec cette clé")
        
        # Générer un nombre aléatoire éphémère (k)
        k = random.randint(2, self.p - 2)
        
        # Calculer c1 = g^k mod p
        c1 = pow(self.g, k, self.p)
        
        # Calculer le secret partagé s = h^k mod p (où h est la clé publique)
        s = pow(self.public_key, k, self.p)
        
        # Calculer c2 = m * s mod p
        c2 = (plaintext * s) % self.p
        
        return (c1, c2)
    
    def decrypt(self, ciphertext):
        """
        Déchiffre un message chiffré avec ElGamal
        
        Args:
            ciphertext: Tuple (c1, c2) représentant le texte chiffré
            
        Returns:
            Le message déchiffré
        """
        c1, c2 = ciphertext
        
        # Calculer s = c1^a mod p (où a est la clé privée)
        s = pow(c1, self.private_key, self.p)
        
        # Calculer s^-1 mod p (inverse modulaire)
        s_inverse = mod_inverse(s, self.p)
        
        # Récupérer le message m = c2 * s^-1 mod p
        plaintext = (c2 * s_inverse) % self.p
        
        # Tenter de convertir en texte (si c'était un texte à l'origine)
        try:
            # Déterminer le nombre d'octets nécessaires
            byte_length = max(1, (plaintext.bit_length() + 7) // 8)
            plaintext_bytes = plaintext.to_bytes(byte_length, byteorder='big')
            return plaintext_bytes.decode('utf-8')
        except:
            # Sinon retourner le nombre
            return plaintext


if __name__ == "__main__":
    # Ask the user for input
    plaintext = input("Enter text to encrypt: ")
    
    # Initialize  (in real case key should be > 2048 bits)
    elgamal = ElGamalCipher(key_size=512)
    
    # Encrypt
    encrypted_data = elgamal.encrypt(plaintext)
    print("Encrypted:", encrypted_data)
    
    # Decrypt
    decrypted_text = elgamal.decrypt(encrypted_data)
    print("Decrypted:", decrypted_text)