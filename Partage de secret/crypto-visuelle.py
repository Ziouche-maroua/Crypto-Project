from PIL import Image
import random

def generate_shares(image_path):
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

def overlay_shares(share1, share2):
    width, height = share1.size
    result = Image.new('1', (width, height))
    for x in range(width):
        for y in range(height):
            # superposition logique OU
            pixel = share1.getpixel((x, y)) | share2.getpixel((x, y))
            result.putpixel((x, y), pixel)
    return result




