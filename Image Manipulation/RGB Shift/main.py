import os
from PIL import Image

def shift_pixel(r, g, b, rI, gI, bI):
    rS, gS, bS = r, g, b
    
    if rI == 'r':
        r = rS
    elif rI == 'g':
        r = gS
    elif rI == 'b':
        r = bS
        
    if gI == 'r':
        g = rS
    elif gI == 'g':
        g = gS
    elif gI == 'b':
        g = bS
        
    if bI == 'r':
        b = rS
    elif bI == 'g':
        b = gS
    elif bI == 'b':
        b = bS
    
    return r, g, b

def create_image(input_path, output_path, rI, gI, bI):
    file_ext = os.path.splitext(input_path)[1].lower()
    if file_ext in ['.png', '.jpg', '.jpeg', '.webp']:
        image = Image.open(input_path)
        image = image.convert('RGB')

        width, height = image.size
        pixels = image.load()
        
        shifted_pixels = []
        
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                r, g, b = shift_pixel(r, g, b, rI, gI, bI)
                shifted_pixels.append((r, g, b))
        
        output_image = Image.new('RGB', image.size)
        output_image.putdata(shifted_pixels)
        
        output_image.save(output_path)
        output_image.show()

if __name__ == "__main__":
    file_path = input("Enter image path: ").strip()
    
    rI = input("For red channel (r, g, b): ").strip()
    gI = input("For green channel (r, g, b): ").strip()
    bI = input("For blue channel (r, g, b): ").strip()
    
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    
    if os.path.isfile(file_path):
        output_path = os.path.join(os.path.dirname(file_path), f"{base_name}_rgbshifted.png")
        create_image(file_path, output_path, rI, gI, bI)
    else:
        print("File does not exist. Please check the file path and try again.")
