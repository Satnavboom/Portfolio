import os
from PIL import Image

def recolour_pixel(r, g, b):
    if r > g and r > b:
        r, g, b = 255, 0, 0
    elif g > r and g > b:
        r, g, b = 0, 255, 0
    elif b > r and b > g:
        r, g, b = 0, 0, 255
        
    elif r == g == b:
        r, g, b = 255, 255, 255
        
    elif r == g and r != b:
        r, g, b = 255, 255, 0
    elif g == b and g != r:
        r, g, b = 0, 255, 255
    elif b == r and b != g:
        r, g, b = 255, 0, 255
        
    return r, g, b

def create_image(input_path, output_path):
    file_ext = os.path.splitext(input_path)[1].lower()
    if file_ext in ['.png', '.jpg', '.jpeg', '.webp']:
        image = Image.open(input_path)
        image = image.convert('RGB')
        
        width, height = image.size
        pixels = image.load()
        
        recoloured_pixels = []
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                r, g, b = recolour_pixel(r, g, b)
                recoloured_pixels.append((r, g, b))
        
        output_image = Image.new('RGB', image.size)
        output_image.putdata(recoloured_pixels)
        
        output_path = output_path
        output_image.save(output_path)
        output_image.show()

if __name__ == "__main__":
    file_path = input("Enter image path: ").strip()
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    
    if os.path.isfile(file_path):
        output_path = os.path.join(os.path.dirname(file_path), f"{base_name}_3color.png")
        create_image(file_path, output_path)
    else:
        print("File does not exist. Please check the file path and try again.")
