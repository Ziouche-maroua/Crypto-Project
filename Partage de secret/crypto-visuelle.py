from PIL import Image
import random
import os

def generate_shares(image_path):
    try:
        # Vérifier si le fichier existe
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Le fichier {image_path} n'existe pas")
        
        img = Image.open(image_path).convert('1')  # Noir & blanc
        width, height = img.size
        
        share1 = Image.new('1', (width * 2, height * 2))
        share2 = Image.new('1', (width * 2, height * 2))
        
        for y in range(height):
            for x in range(width):
                pixel = img.getpixel((x, y))
                # motif aléatoire (2x2 bloc)
                pattern = random.randint(0, 1)
                if pixel == 0:  # pixel noir
                    if pattern == 0:
                        block1 = [(0, 1), (1, 0)]
                        block2 = [(0, 1), (1, 0)]
                    else:
                        block1 = [(1, 0), (0, 1)]
                        block2 = [(1, 0), (0, 1)]
                else:  # pixel blanc
                    if pattern == 0:
                        block1 = [(0, 1), (1, 0)]
                        block2 = [(1, 0), (0, 1)]
                    else:
                        block1 = [(1, 0), (0, 1)]
                        block2 = [(0, 1), (1, 0)]
                
                # appliquer le motif
                for dx in range(2):
                    for dy in range(2):
                        share1.putpixel((2*x + dx, 2*y + dy), block1[dy][dx])
                        share2.putpixel((2*x + dx, 2*y + dy), block2[dy][dx])
        
        return share1, share2
    
    except Exception as e:
        print(f"Erreur lors de l'ouverture de l'image : {e}")
        return None, None

def overlay_shares(share1, share2):
    if share1 is None or share2 is None:
        return None
    
    width, height = share1.size
    result = Image.new('1', (width, height))
    for x in range(width):
        for y in range(height):
            # superposition logique OU
            pixel = share1.getpixel((x, y)) | share2.getpixel((x, y))
            result.putpixel((x, y), pixel)
    return result

def create_sample_image():
    """Crée une image d'exemple simple"""
    img = Image.new('1', (50, 50), 1)  # Image blanche 50x50
    # Dessiner un carré noir au centre
    for x in range(20, 30):
        for y in range(20, 30):
            img.putpixel((x, y), 0)
    img.save("secret.png")
    print("Image d'exemple 'secret.png' créée")

# Solutions possibles :

# Solution 1: Créer une image d'exemple
print("Création d'une image d'exemple...")
create_sample_image()

# Solution 2: Utiliser le chemin correct
possible_paths = [
    "secret.png",  # Dans le répertoire courant
    "Partage de secret/secret.png",  # Chemin relatif
    r"C:\Users\HP\Desktop\Crypto\Partage de secret\secret.png"  # Chemin absolu
]

image_found = False
for path in possible_paths:
    if os.path.exists(path):
        print(f"Image trouvée : {path}")
        # Génère les parts
        s1, s2 = generate_shares(path)
        if s1 and s2:
            s1.save("share1.png")
            s2.save("share2.png")
            print("Parts sauvegardées : share1.png et share2.png")
            
            # Superposition
            reveal = overlay_shares(s1, s2)
            if reveal:
                reveal.save("revealed.png")
                print("Image révélée sauvegardée : revealed.png")
        image_found = True
        break

if not image_found:
    # Utiliser l'image d'exemple créée
    print("Utilisation de l'image d'exemple...")
    s1, s2 = generate_shares("secret.png")
    if s1 and s2:
        s1.save("share1.png")
        s2.save("share2.png")
        print("Parts sauvegardées : share1.png et share2.png")
        
        # Superposition
        reveal = overlay_shares(s1, s2)
        if reveal:
            reveal.save("revealed.png")
            print("Image révélée sauvegardée : revealed.png")

print("Terminé!")