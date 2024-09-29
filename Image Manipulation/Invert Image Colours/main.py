import os
from PIL import Image

def reverse_pixel(r, g, b):
    r = 255 - r
    g = 255 - g
    b = 255 - b
    return r, g, b

def create_image(input_path, output_path):
    file_ext = os.path.splitext(input_path)[1].lower()
    if file_ext in ['.png', '.jpg', '.jpeg', '.webp']:
        image = Image.open(input_path)
        image = image.convert('RGB')

        width, height = image.size
        pixels = image.load()
        
        reversed_pixels = []
        
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                r, g, b = reverse_pixel(r, g, b)
                reversed_pixels.append((r, g, b))
        
        output_image = Image.new('RGB', image.size)
        output_image.putdata(reversed_pixels)
        
        output_image.save(output_path)
        output_image.show()

def create_checkered_image(input_path, output_path):
    file_ext = os.path.splitext(input_path)[1].lower()
    if file_ext in ['.png', '.jpg', '.jpeg', '.webp']:
        image = Image.open(input_path)
        image = image.convert('RGB')

        width, height = image.size
        pixels = image.load()
        
        reversed_pixels = []
        pixel_num = 0
        width_is_even = (width % 2 == 0)
        
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                pixel_num += 1
                if pixel_num % 2 == 0:
                    r, g, b = reverse_pixel(r, g, b)
                reversed_pixels.append((r, g, b))
            
            if width_is_even:
                pixel_num += 1
        
        output_image = Image.new('RGB', image.size)
        output_image.putdata(reversed_pixels)
        
        output_image.save(output_path)
        output_image.show()

def create_lined_image(input_path, output_path):
    file_ext = os.path.splitext(input_path)[1].lower()
    if file_ext in ['.png', '.jpg', '.jpeg', '.webp']:
        image = Image.open(input_path)
        image = image.convert('RGB')

        width, height = image.size
        pixels = image.load()
        
        reversed_pixels = []
        pixel_num = 0
        width_is_odd = (width % 2 == 1)
        
        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                pixel_num += 1
                if pixel_num % 2 == 0:
                    r, g, b = reverse_pixel(r, g, b)
                reversed_pixels.append((r, g, b))
            
            if width_is_odd:
                pixel_num += 1
        
        output_image = Image.new('RGB', image.size)
        output_image.putdata(reversed_pixels)
        
        output_image.save(output_path)
        output_image.show()

if __name__ == "__main__":
    file_path = input("Enter image path: ").strip()
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    
    if os.path.isfile(file_path):
        output_path = os.path.join(os.path.dirname(file_path), f"{base_name}_inverted.png")
        choice = input("'Normal', 'Checkered', or 'Lined': ").lower()
        if choice == "normal":
            create_image(file_path, output_path)
        elif choice == "checkered":
            create_checkered_image(file_path, output_path)
        elif choice == "lined":
            create_lined_image(file_path, output_path)
        else:
            print("Invalid choice.")
        
    else:
        print("File does not exist. Please check the file path and try again.")
