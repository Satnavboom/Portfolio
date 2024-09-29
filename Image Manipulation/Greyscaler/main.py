from PIL import Image

filename = input("Input the directory of the image: ")
manipulation_type = input("""
How should the image be manipulated?
Black or White [2 colors] (BW)
Black, White, Grey [3 colors] (G)
Greyscale [256 colors] (GS)
: """).upper()

img = Image.open(filename)
img = img.convert('RGB')

width, height = img.size
new_pixels = []

for y in range(height):
    for x in range(width):
        r, g, b = img.getpixel((x, y))
        pixel_sum = r + g + b

        if manipulation_type == "BW":
            if pixel_sum > 255 * 1.5:
                new_pixels.append((255, 255, 255))
            else:
                new_pixels.append((0, 0, 0))
        elif manipulation_type == "G":
            if pixel_sum > 255 * 2:
                new_pixels.append((255, 255, 255))
            elif pixel_sum > 255:
                new_pixels.append((127, 127, 127))
            else:
                new_pixels.append((0, 0, 0))
        elif manipulation_type == "GS":
            greyscale_value = int(0.299 * r + 0.587 * g + 0.114 * b)
            new_pixels.append((greyscale_value, greyscale_value, greyscale_value))
        else:
            print("Invalid input.")
            exit()

new_img = Image.new('RGB', (width, height))
new_img.putdata(new_pixels)

output_filename = f"{filename.split('.')[0]}_{manipulation_type}.png"
new_img.save(output_filename)
new_img.show()

print(f"Manipulated image saved as: {output_filename}")
