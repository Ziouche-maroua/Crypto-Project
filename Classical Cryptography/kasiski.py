from collections import defaultdict
from math import gcd
from functools import reduce

def kasiski_examination(ciphertext, min_len=3):
   
    repetitions = defaultdict(list)

    # Chercher tous les motifs de taille min_len ou plus
    for i in range(len(ciphertext) - min_len):
        seq = ciphertext[i:i+min_len]
        for j in range(i + 1, len(ciphertext) - min_len):
            if ciphertext[j:j+min_len] == seq:
                repetitions[seq].append((i, j))

    distances = []
   
    for seq, positions in repetitions.items():
        for (pos1, pos2) in positions:
            dist = pos2 - pos1
            distances.append(dist)
            print(f"Motif '{seq}' trouvé aux positions {pos1} et {pos2}, distance = {dist}")

    if not distances:
        print("Aucune répétition trouvée avec la taille donnée.")
        return None

    
    probable_key_length = reduce(gcd, distances)
    print(f"PGCD des distances : {probable_key_length}")
    return probable_key_length

# Exemple d’utilisation
cipher = "XYZABCVFSHKQXYZJQNXYZHHHXYZ"
kasiski_examination(cipher)
