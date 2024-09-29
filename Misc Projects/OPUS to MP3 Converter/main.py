import sys
import subprocess
import os

if len(sys.argv) != 2:
    print("Usage: python convert_opus_to_mp3.py <input_file>")
    sys.exit(1)

input_file = sys.argv[1]
output_file = os.path.splitext(input_file)[0] + '.mp3'

if not os.path.isfile(input_file):
    print(f"Error: File does not exist: {input_file}")
    input("Press enter to exit...")
    sys.exit(1)

if os.path.exists(output_file):
    print(f"Error: File already exists: {output_file}")
    input("Press enter to exit...")
    sys.exit(1)

command = ['ffmpeg', '-i', input_file, output_file]

try:
    subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(f"Successfully converted to: {output_file}")
except subprocess.CalledProcessError as e:
    print(f"An error occurred: {e.stderr.decode()}")
    input("Press enter to exit...")
    sys.exit(1)
