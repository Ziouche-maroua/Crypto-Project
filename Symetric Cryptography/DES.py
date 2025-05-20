from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

def des_encrypt(key, plaintext):
    des = DES.new(key, DES.MODE_ECB)
    padded_text = pad(plaintext.encode('utf-8'), DES.block_size)
    encrypted_text = des.encrypt(padded_text)
    return base64.b64encode(encrypted_text).decode('utf-8')

def des_decrypt(key, ciphertext):
    des = DES.new(key, DES.MODE_ECB)
    encrypted_text = base64.b64decode(ciphertext)
    decrypted_text = des.decrypt(encrypted_text)
    return unpad(decrypted_text, DES.block_size).decode('utf-8')

# Example usage
if __name__ == "__main__":
    key = get_random_bytes(8)  # DES key must be 8 bytes
    plaintext = "Hello, DES!"

    ciphertext = des_encrypt(key, plaintext)
    decrypted = des_decrypt(key, ciphertext)

    print("Key (base64):", base64.b64encode(key).decode())
    print("Plaintext:", plaintext)
    print("Ciphertext:", ciphertext)
    print("Decrypted:", decrypted)
