
def vigenere_decrypt(ciphertext, key):
    plaintext = ''
    key = key.upper()  # Ensure key is uppercase
    
    # Extend the key to match the length of the ciphertext
    key_repeated = (key * (len(ciphertext) // len(key))) + key[:len(ciphertext) % len(key)]
    
    for i in range(len(ciphertext)):
        char = ciphertext[i]
        if char.isalpha():  # Only decrypt letters
            shift = ord(key_repeated[i]) - ord('A')  # Get shift value from key
            base = ord('A') if char.isupper() else ord('a')
            new_char = chr((ord(char) - base - shift) % 26 + base)  # Subtract shift for decryption
        else:
            new_char = char  # Keep non-alphabetic characters unchanged
        plaintext += new_char
    
    return plaintext

# Example of Vigenère decryption
ciphertext = 'KMGMAZXDUSMEYCOBCATHTGQEOGZQNLSLPLWIWIYPAYMZCFGJVTKWUNKEMAZUULGTZWMCAMNVRYUKSMVSYUHPDZSHWTIQQEOGMEBMOFCBKLMBNCAMNVRYUJCAMFGGUEBMGYVKIRDWINHXHWBMFLHNVBYGZMKMGNKTTDZONKMHZLCJVLVCMGMQSYSQCHUYSACGNGZISMTZKJEBMGJQBVOZCNGNIQTSMKUJNZAUVPSMAGYPZMATSMIYEBMOXGZXDKVHKXYDARYEOMENFYOLRSIJUPJIDAQYUZCRBSGGZXQIBMHVVLMBNNLWCWBHGLWDVTITTESAWFNPWHJZYUNEQIBNKZWZVHUKUWHTSOTJSMNWXGUXHIZCVLISTSOTPRSMULKAI'
key = "ZIOUCHE"
plaintext = vigenere_decrypt(ciphertext, key)
print(plaintext)




def vigenere_encrypt(plaintext, key):
    ciphertext = ""
    key = key.upper()  # Ensure key is uppercase
    key_repeated = (key * (len(plaintext) // len(key))) + key[:len(plaintext) % len(key)]  # Extend key to match plaintext
    
    for i in range(len(plaintext)):
        char = plaintext[i]
        if char.isalpha():  # Encrypt only letters
            shift = ord(key_repeated[i]) - ord('A')  # Get shift from key letter
            base = ord('A') if char.isupper() else ord('a')
            new_char = chr((ord(char) - base + shift) % 26 + base)
        else:
            new_char = char  # Keep spaces, punctuation, and numbers unchanged
        ciphertext += new_char
    return ciphertext