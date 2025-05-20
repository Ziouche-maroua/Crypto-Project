# since we are using python we would take benifit of the hashlib library
# which provide us with a lot of hashing algorithms
import hashlib

def hash_text(text):
    data = text.encode()

    print("MD5       :", hashlib.md5(data).hexdigest())
    print("SHA-1     :", hashlib.sha1(data).hexdigest())
    print("SHA-256   :", hashlib.sha256(data).hexdigest())
    print("SHA-512   :", hashlib.sha512(data).hexdigest())

#here we update the text to be hashed
hash_text("Hello World")
