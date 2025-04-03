import numpy as np

def hill_encrypt(plaintext, key_matrix):
    if not all(len(row) == len(key_matrix) for row in key_matrix):
        raise ValueError("Key matrix must be square (n x n).")

    letters = []
    non_letters = []  # Stores non-letters with their positions

    # Step 1: Separate letters and non-letters
    for i, char in enumerate(plaintext):
        if char.isalpha():
            letters.append(char.upper())  # Convert letters to uppercase
        else:
            non_letters.append((i, char))  # Store index and character

    # Step 2: Organize letters into vectors of size n
    n = len(key_matrix)
    while len(letters) % n != 0:
        letters.append('X')  # Padding if needed

    vectors = [letters[i:i+n] for i in range(0, len(letters), n)]

    # Step 3: Convert letters to numbers (A=0, B=1, ..., Z=25)
    numeric_vectors = [[ord(char) - ord('A') for char in vector] for vector in vectors]

    # Step 4: Multiply by key matrix and take mod 26
    key_matrix = np.array(key_matrix)
    encrypted_vectors = [(np.dot(key_matrix, vector) % 26).tolist() for vector in numeric_vectors]

    # Step 5: Convert numbers back to letters
    encrypted_text = ''.join(''.join(chr(num + ord('A')) for num in vector) for vector in encrypted_vectors)

    # Step 6: Reinsert non-letters in their original positions
    encrypted_list = list(encrypted_text)  # Convert to list to allow insertion
    for index, char in non_letters:
        encrypted_list.insert(index, char)

    return ''.join(encrypted_list)  # Convert back to string

# Example Usage
key = [[9, 4], [5, 7]]  # Example 2x2 key matrix
plaintext = "hi7ll, world! How's everything?"
ciphertext = hill_encrypt(plaintext, key)
print("Encrypted Message:", ciphertext)



