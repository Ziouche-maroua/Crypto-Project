def caesar_cipher(plaintext: str, k: int) -> str:
    ciphertext = ""
    for char in plaintext:
        if char.isalpha():  # Process only letters
            shift = k % 26   # Ensure k is within 0-25
            base = ord('A') if char.isupper() else ord('a')
            new_char = chr((ord(char) - base + shift) % 26 + base)
        else:
            new_char = char  # Keep spaces and symbols unchanged
        ciphertext += new_char
    return ciphertext

def caesar_decrypt(ciphertext: str, k: int) -> str:
    plaintext = ""
    for char in ciphertext:
        if char.isalpha():  # Only shift letters
            shift = k % 26
            base = ord('A') if char.isupper() else ord('a')
            new_char = chr((ord(char) - base - shift) % 26 + base)
        else:
            new_char = char  # Keep punctuation/numbers unchanged
        plaintext += new_char
    return plaintext

# Example of Caesar cipher
plaintext = "Hello@maroua"
k = 3
ciphertext = caesar_cipher(plaintext, k)
print(ciphertext)

# Example of decryption
ciphertext = "Khoor!"
k = 3
plaintext = caesar_decrypt(ciphertext, k)
print(plaintext)

