# English letter frequencies 
english_freq = {
    'A': 8.17, 'B': 1.49, 'C': 2.78, 'D': 4.25, 'E': 12.70, 'F': 2.23, 'G': 2.02, 'H': 6.09,
    'I': 6.97, 'J': 0.15, 'K': 0.77, 'L': 4.03, 'M': 2.41, 'N': 6.75, 'O': 7.51, 'P': 1.93,
    'Q': 0.10, 'R': 5.99, 'S': 6.33, 'T': 9.06, 'U': 2.76, 'V': 0.98, 'W': 2.36, 'X': 0.15,
    'Y': 1.97, 'Z': 0.07
}

# French letter frequencies
french_freq = {
    'A': 7.64, 'B': 0.90, 'C': 3.26, 'D': 3.67, 'E': 14.72, 'F': 1.06, 'G': 1.10, 'H': 0.74,
    'I': 7.53, 'J': 0.61, 'K': 0.07, 'L': 5.46, 'M': 2.97, 'N': 7.09, 'O': 5.80, 'P': 2.52,
    'Q': 1.36, 'R': 6.69, 'S': 7.95, 'T': 7.24, 'U': 6.31, 'V': 1.84, 'W': 0.06, 'X': 0.42,
    'Y': 0.30, 'Z': 0.15
}

from collections import Counter

def compute_frequency(text):
    """ Computes letter frequency in a given text """
    text = text.upper()
    letter_counts = Counter(c for c in text if c.isalpha())  # Count only letters
    total_letters = sum(letter_counts.values())
    
    # Normalize frequencies
    return {char: (count / total_letters) * 100 for char, count in letter_counts.items()} if total_letters > 0 else {}

# Example ciphertext
ciphertext = "WKH TXLFN EURZQ IRAA MXPSV RYHU WKH ODCB GRJ"
cipher_freq = compute_frequency(ciphertext)


def compare_frequencies(cipher_freq, lang_freq):
    """ Compares two frequency distributions and returns a similarity score (lower is better). """
    return sum(abs(cipher_freq.get(letter, 0) - lang_freq.get(letter, 0)) for letter in lang_freq)

def detect_language(cipher_freq):
    """ Detects whether the text is closer to English or French frequency distribution. """
    eng_diff = compare_frequencies(cipher_freq, english_freq)
    fr_diff = compare_frequencies(cipher_freq, french_freq)
    
    return "English" if eng_diff < fr_diff else "French"

# Detect language
language = detect_language(cipher_freq)
print("Detected Language:", language)

def frequency_substitution_decrypt(ciphertext, lang_freq):
    """Decrypts a simple substitution cipher using frequency analysis."""
    # Compute ciphertext letter frequencies
    cipher_freq = compute_frequency(ciphertext)
    
    # Sort letters by frequency (descending)
    sorted_cipher_letters = sorted(cipher_freq, key=cipher_freq.get, reverse=True)
    
    # Sort language letters by frequency (descending)
    sorted_lang_letters = sorted(lang_freq, key=lang_freq.get, reverse=True)
    
    # Create a mapping
    mapping = {cipher: plain for cipher, plain in zip(sorted_cipher_letters, sorted_lang_letters)}
    
    # Decrypt the text
    decrypted_text = "".join(mapping.get(char, char) for char in ciphertext.upper())
    
    return decrypted_text, mapping

# Detect language first
detected_lang = detect_language(cipher_freq)
lang_freq = english_freq if detected_lang == "English" else french_freq

# Decrypt
decrypted_text, letter_map = frequency_substitution_decrypt(ciphertext, lang_freq)

print("Detected Language:", detected_lang)
print("Letter Mapping:", letter_map)
print("Decrypted Text:", decrypted_text)
