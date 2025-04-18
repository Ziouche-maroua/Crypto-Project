import string

def prepare_playfair_key(key):
    key = key.upper().replace("J", "I")  # J = I dans Playfair
    result = ""
    seen = set()

    for char in key:
        if char in string.ascii_uppercase and char not in seen:
            seen.add(char)
            result += char

    # Compléter la grille avec les autres lettres
    for char in string.ascii_uppercase:
        if char not in seen and char != "J":
            result += char

    # Grille 5x5
    matrix = [list(result[i:i+5]) for i in range(0, 25, 5)]
    return matrix

def find_position(matrix, char):
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == char:
                return i, j

def process_text(text):
    text = text.upper().replace("J", "I")
    text = ''.join([c for c in text if c in string.ascii_uppercase])
    
    pairs = []
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1 < len(text) else 'X'
        if a == b:
            pairs.append((a, 'X'))
            i += 1
        else:
            pairs.append((a, b))
            i += 2
    return pairs

def encrypt_playfair(key, plaintext):
    matrix = prepare_playfair_key(key)
    pairs = process_text(plaintext)
    ciphertext = ""

    for a, b in pairs:
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)

        if row1 == row2:
            ciphertext += matrix[row1][(col1 + 1) % 5]
            ciphertext += matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            ciphertext += matrix[(row1 + 1) % 5][col1]
            ciphertext += matrix[(row2 + 1) % 5][col2]
        else:
            ciphertext += matrix[row1][col2]
            ciphertext += matrix[row2][col1]

    return ciphertext

def decrypt_playfair(key, ciphertext):
    matrix = prepare_playfair_key(key)
    pairs = process_text(ciphertext)
    plaintext = ""

    for a, b in pairs:
        row1, col1 = find_position(matrix, a)
        row2, col2 = find_position(matrix, b)

        if row1 == row2:
            plaintext += matrix[row1][(col1 - 1) % 5]
            plaintext += matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:
            plaintext += matrix[(row1 - 1) % 5][col1]
            plaintext += matrix[(row2 - 1) % 5][col2]
        else:
            plaintext += matrix[row1][col2]
            plaintext += matrix[row2][col1]

    return plaintext

# Exemple d’utilisation
key = "MONKEY"
message = "HELLO WORLD"

encrypted = encrypt_playfair(key, message)
print(f"Texte chiffré : {encrypted}")

decrypted = decrypt_playfair(key, encrypted)
print(f"Texte déchiffré : {decrypted}")
