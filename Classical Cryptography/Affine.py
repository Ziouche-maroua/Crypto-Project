from collections import Counter

def compute_frequency(text):
    """ Computes letter frequency in a given text """
    text = text.upper()
    letter_counts = Counter(c for c in text if c.isalpha())  # Count only letters
    total_letters = sum(letter_counts.values())
    
    # Normalize frequencies
    return {char: (count / total_letters) * 100 for char, count in letter_counts.items()} if total_letters > 0 else {}

def get_top_cipher_letters(ciphertext, n=2):
    freq = compute_frequency(ciphertext)
    return sorted(freq, key=freq.get, reverse=True)[:n]



def find_affine_parameters(ciphertext, top_cipher_letters, expected_plain_letters=('E', 'T')):
    """
    Deduce affine cipher parameters (a, b) based on frequency mapping.
    """
    # Ciphertext letters (most frequent)
    c1_num = ord(top_cipher_letters[0].upper()) - ord('A')
    c2_num = ord(top_cipher_letters[1].upper()) - ord('A')

    # Expected plaintext letters they likely map to
    p1_num = ord(expected_plain_letters[0]) - ord('A')
    p2_num = ord(expected_plain_letters[1]) - ord('A')

    # Calculate 'a' using modular inverse
    delta_p = (p1_num - p2_num) % 26
    delta_c = (c1_num - c2_num) % 26
    inv_delta_p = pow(delta_p, -1, 26)  # This will fail if delta_p has no inverse

    a = (delta_c * inv_delta_p) % 26
    b = (c1_num - a * p1_num) % 26

    return a, b



def affine_decrypt(ciphertext, a, b):
    """
    Decrypt using affine cipher with deduced parameters
    """
    # Calculate modular multiplicative inverse of 'a'
    a_inv = pow(a, -1, 26)
    
    plaintext = ""
    for char in ciphertext:
        if char.isalpha():
            # Convert to number
            x = ord(char) - ord('A')
            
            # Decrypt: D(x) = a^(-1)(x - b) mod 26
            decrypted_num = (a_inv * (x - b)) % 26
            
            # Convert back to letter
            plaintext += chr(decrypted_num + ord('A'))
        else:
            plaintext += char
    
    return plaintext

# Example usage
ciphertext = "KHRKN KNHAVUG BQQZON".upper()
top_letters = get_top_cipher_letters(ciphertext)
a, b = find_affine_parameters(ciphertext, top_letters)
plaintext = affine_decrypt(ciphertext, a, b)
print("Top letters in ciphertext:", top_letters)
print("Affine a, b:", a, b)
print("Decrypted:", plaintext)
