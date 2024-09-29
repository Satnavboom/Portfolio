import os

script_dir = os.path.dirname(os.path.abspath(__file__))

file_name = input("Enter the filename (no extension): ") + ".bmp"
file_path = os.path.join(script_dir, file_name)

width = int(input("Enter width (dec): "))
height = int(input("Enter height (dec): "))

row_padded_size = (width * 3 + 3) & ~3
image_size = row_padded_size * height

headers = f"42 4D 00 00 00 00 00 00 00 00 00 00 00 00 0C 00 00 00 {width:02X} 00 {height:02X} 00 01 00 18 00"
header_bytes = bytes.fromhex(headers)

image_data = []

print("(Whole RGB seperated by spaces, for example FFFFFF and not FF FF FF)")
for _ in range(height):
    row = input(f"Enter row ({width} long): ")
    rgb_values = row.split()
    
    if len(rgb_values) != width:
        print(f"You must have exactly {width} values.")
        exit()
    
    row_data = bytearray()
    for value in rgb_values:
        r = value[-2:]
        g = value[-4:-2]
        b = value[-6:-4]
        row_data.extend(bytes([int(b, 16), int(g, 16), int(r, 16)]))
    
    padding = row_padded_size - len(row_data)
    if padding > 0:
        row_data.extend(b'\x00' * padding)
    
    image_data.append(row_data)

with open(file_path, 'wb') as file:
    file.write(header_bytes)
    for row in image_data:
        file.write(row)

print(f"BMP file '{file_name}' created in '{script_dir}'.")
