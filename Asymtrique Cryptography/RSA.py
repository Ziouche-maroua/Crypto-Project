from math import gcd

def est_premier(n):
    """Teste si un nombre est premier (méthode simple)"""
    if n <= 1:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

def egcd(a, b):
    """Algorithme d’Euclide étendu"""
    if a == 0:
        return b, 0, 1
    g, y, x = egcd(b % a, a)
    return g, x - (b // a) * y, y

def modinv(a, m):
    """Inverse modulaire"""
    g, x, _ = egcd(a, m)
    if g != 1:
        raise Exception("Pas d’inverse modulaire")
    return x % m

def rsa_init(p, q, e):
    """Initialise RSA : vérifie les conditions et calcule les clés"""
    if not (est_premier(p) and est_premier(q)):
        raise ValueError("p et q doivent être des nombres premiers.")
    if p == q:
        raise ValueError("p et q doivent être distincts.")

    n = p * q
    phi = (p - 1) * (q - 1)

    if gcd(e, phi) != 1:
        raise ValueError("e doit être premier avec φ(n).")

    d = modinv(e, phi)

    print(f"Clé publique (n={n}, e={e})")
    print(f"Clé privée (n={n}, d={d})")

    def chiffrer(M):
        if M >= n:
            raise ValueError("Le message M doit être strictement inférieur à n.")
        return pow(M, e, n)

    def dechiffrer(C):
        return pow(C, d, n)

    return chiffrer, dechiffrer, n  # retourne aussi n pour que tu puisses vérifier M < n

# Exemple d’utilisation :
p = 31
q = 53
e = 11

chiffrer, dechiffrer, n = rsa_init(p, q, e)

M = 13
C = chiffrer(M)
print(f"Message chiffré : {C}")

M_dechiffre = dechiffrer(C)
print(f"Message déchiffré : {M_dechiffre}")


def lettre_vers_nombre(c):
    """Convertit une lettre (maj ou min) en un nombre (0-25), ignore le reste"""
    c = c.lower()
    if 'a' <= c <= 'z':
        return ord(c) - ord('a')
    return None

def nombre_vers_lettre(n):
    """Convertit un nombre (0–25) en lettre minuscule"""
    if 0 <= n <= 25:
        return chr(n + ord('a'))
    return '?'


def texte_vers_chiffre(texte, chiffrer, n):
    """Convertit un texte en liste de chiffres chiffrés RSA"""
    resultats = []
    for c in texte:
        num = lettre_vers_nombre(c)
        if num is not None:
            if num >= n:
                raise ValueError(f"Le nombre {num} ne peut pas être chiffré (doit être < n={n})")
            resultats.append(chiffrer(num))
    return resultats

def chiffre_vers_texte(chiffres, dechiffrer):
    """Convertit une liste de chiffres RSA déchiffrés en texte"""
    texte = ""
    for c in chiffres:
        num = dechiffrer(c)
        lettre = nombre_vers_lettre(num)
        texte += lettre
    return texte


texte = "BONJOUR!"
chiffres = texte_vers_chiffre(texte, chiffrer, n)
print(f"Texte chiffré en RSA : {chiffres}")

texte_dechiffre = chiffre_vers_texte(chiffres, dechiffrer)
print(f"Texte déchiffré : {texte_dechiffre}")
