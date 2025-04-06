import numpy as np
import math


def is_invertible_mod26(matrix):
    # Compute determinant
    det = int(round(np.linalg.det(matrix)))  # Ensure determinant is an integer
    det_mod26 = det % 26  # Take mod 26

    # Check if gcd(det, 26) is 1 (matrix is invertible if true)
    return math.gcd(det_mod26, 26) == 1

def mod_inverse(a, m=26):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    return None

# Function to compute the inverse of a matrix modulo 26
def mod_matrix_inverse(matrix, mod=26):
    # Step 1: Compute the determinant modulo 26
    det = int(np.round(np.linalg.det(matrix))) % mod
    
    # Step 2: Find the modular inverse of the determinant
    det_inv = mod_inverse(det, mod)
    
    # If determinant is not invertible modulo 26, raise an error
    if det_inv is None:
        raise ValueError("Matrix is not invertible modulo 26.")
    
    # Step 3: Compute the matrix of cofactors (adjugate matrix)
    cofactors = []
    for i in range(matrix.shape[0]):
        cofactor_row = []
        for j in range(matrix.shape[1]):
            # Compute minor for element (i,j)
            minor = np.delete(matrix, i, axis=0)  # Remove row i
            minor = np.delete(minor, j, axis=1)   # Remove column j
            cofactor = (-1) ** (i + j) * int(np.round(np.linalg.det(minor)))  # Cofactor
            cofactor_row.append(cofactor)
        cofactors.append(cofactor_row)

    cofactors = np.array(cofactors)  # Convert to numpy array
    
    # Step 4: Transpose the cofactor matrix to get the adjugate matrix
    adjugate = cofactors.T
    
    # Step 5: Multiply adjugate by the modular inverse of the determinant
    inverse_matrix = (det_inv * adjugate) % mod
    
    return inverse_matrix

def hill_encrypt(plaintext, key_matrix):
    if not (all(len(row) == len(key_matrix) for row in key_matrix)) or not is_invertible_mod26(key_matrix):
        raise ValueError("Key matrix must be square (n x n) and invertible.")

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

def hill_decrypt(ciphertext, key_matrix):
    if not (all(len(row) == len(key_matrix) for row in key_matrix)) or not is_invertible_mod26(key_matrix):
        raise ValueError("Key matrix must be square (n x n) and invertible.")

    key_matrix_inv = mod_matrix_inverse(np.array(key_matrix), 26)

    letters = []
    non_letters = []  # Stores non-letters with their positions

    # Step 1: Separate letters and non-letters
    for i, char in enumerate(ciphertext):
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
    key_matrix_inv = np.array(key_matrix_inv)
    encrypted_vectors = [(np.dot(key_matrix_inv, vector) % 26).tolist() for vector in numeric_vectors]

    # Step 5: Convert numbers back to letters
    encrypted_text = ''.join(''.join(chr(num + ord('A')) for num in vector) for vector in encrypted_vectors)

    # Step 6: Reinsert non-letters in their original positions
    encrypted_list = list(encrypted_text)  # Convert to list to allow insertion
    for index, char in non_letters:
        encrypted_list.insert(index, char)

    return ''.join(encrypted_list)  # Convert back to string

# Example Usage
key = [[9, 4], [5, 7]]  # Example 2x2 key matrix
ciphertext= "RN7NC, UAPGD! MGQ'W OXDPTROUBQ?J"
plaintext = hill_decrypt(ciphertext, key)
print("decrypted Message:", plaintext)
