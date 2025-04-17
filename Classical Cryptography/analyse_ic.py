from collections import Counter

def clean_text(text):
    return ''.join([c.upper() for c in text if c.isalpha()])

def indice_coincidence(text):
    text = clean_text(text)
    n = len(text)
    if n <= 1:
        return 0
    freq = Counter(text)
    ic = sum(f * (f - 1) for f in freq.values()) / (n * (n - 1))
    return ic

def detect_cipher_type(text):
    ic = indice_coincidence(text)
    print(f"Indice de Coïncidence : {round(ic, 4)}")

    if 0.065 <= ic <= 0.08:
        print("Probable chiffre monoalphabétique (César, Affine...)")
        return "mono"
    elif 0.038 <= ic < 0.065:
        print("Probable chiffre polyalphabétique (Vigenère, Hill...)")
        return "poly"
    #else:
     #   print("Indice de coïncidence inhabituel ou texte trop court.")
      #  return "inconnu"

def detect_language(text):
    # IC values for different languages
    language_ic = {
        "Arabe": 0.0758,
        "Anglais": 0.0667,
        "Italien": 0.0738,
        "Portugais": 0.0745,
        "Russe": 0.0529,
        "Allemand": 0.0762,
        "Espagnol": 0.0770,
        "Français": 0.0778
    }

    # Calculate the IC of the input text
    ic = indice_coincidence(text)
    print(f"Indice de Coïncidence : {round(ic, 4)}")

    # Find the closest matching language based on IC
    closest_language = min(language_ic, key=lambda lang: abs(language_ic[lang] - ic))

    print(f"Probable langue : {closest_language}")
    return closest_language

# Exemple d'utilisation
if __name__ == "__main__":
    texte_chiffre = input("Entrer le texte chiffré : ")
    type_chiffre = detect_cipher_type(texte_chiffre)

    if type_chiffre == "mono":
        print("→ Tu peux tester un déchiffrement par César ou Affine.")
    elif type_chiffre == "poly":
        print("→ Tu peux essayer une attaque de Vigenère (Kasiski, Friedman, etc.).")
    print("the language is:",detect_language(texte_chiffre))