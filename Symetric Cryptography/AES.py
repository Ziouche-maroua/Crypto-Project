# -*- coding: utf-8 -*-
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

class AESCipher:
    def __init__(self, key=None):
        """
        Initialise le chiffreur AES avec une cle
        
        Args:
            key: Cle de chiffrement (générée aléatoirement si non fournie)
        """
        # Si aucune clé n'est fournie, on en génère une aléatoirement (256 bits = 32 octets)
        self.key = key if key else get_random_bytes(32)
    
    def encrypt(self, plaintext):
        """
        Chiffre un message avec AES en mode CBC
        
        Args:
            plaintext: Le texte en clair à chiffrer
            
        Returns:
            Un dictionnaire contenant le vecteur d'initialisation (iv) et le texte chiffré (ciphertext)
        """
        # Convertir en bytes si c'est une chaîne
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')
        
        # Générer un vecteur d'initialisation aléatoire (IV)
        iv = get_random_bytes(16)  # AES utilise des blocs de 16 octets
        
        # Créer le chiffreur en mode CBC avec la clé et l'IV
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        
        # Appliquer le padding PKCS#7 et chiffrer
        padded_data = pad(plaintext, AES.block_size)
        ciphertext = cipher.encrypt(padded_data)
        
        # Encoder en base64 pour faciliter le stockage/transmission
        return {
            'iv': base64.b64encode(iv).decode('utf-8'),
            'ciphertext': base64.b64encode(ciphertext).decode('utf-8')
        }
    
    def decrypt(self, encrypted_data):
        """
        Déchiffre un message chiffré avec AES
        
        Args:
            encrypted_data: Dictionnaire contenant l'IV et le texte chiffré
            
        Returns:
            Le message déchiffré
        """
        # Décoder l'IV et le texte chiffré depuis base64
        iv = base64.b64decode(encrypted_data['iv'])
        ciphertext = base64.b64decode(encrypted_data['ciphertext'])
        
        # Créer le déchiffreur avec la même clé et IV
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        
        # Déchiffrer et retirer le padding
        padded_plaintext = cipher.decrypt(ciphertext)
        plaintext = unpad(padded_plaintext, AES.block_size)
        
        # Retourner en format texte
        return plaintext.decode('utf-8')

if __name__ == "__main__":
    # Ask the user for input
    plaintext = input("Enter text to encrypt: ")
    
    # Initialize AES cipher
    cipher = AESCipher()
    
    # Encrypt
    encrypted_data = cipher.encrypt(plaintext)
    print("Encrypted:", encrypted_data)
    
    # Decrypt
    decrypted_text = cipher.decrypt(encrypted_data)
    print("Decrypted:", decrypted_text)
