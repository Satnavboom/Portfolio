import matplotlib.pyplot as plt
import numpy as np

def open_file(filepath):
    try:
        with open(filepath, 'r') as f:
            text = f.read()
            return text
    except FileNotFoundError:
        print("File path could not be found.")
        return ""

filepath = input("Enter file path: ")

text = open_file(filepath)

letters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
numbers = list('0123456789')
chars = ['!', '"', '£', '$', '%', '^', '&', '*', '(', ')', '-', '=', '_', '+', '/', ',', '.', '@', "'", ':', ';', '#', '~', '[', ']', '{', '}', '`', '¬']

uppercase_count = [0] * 26
lowercase_count = [0] * 26
number_count = [0] * 10
other_count = 0
space_count = 0
newline_count = 0
unknown_count = 0

for char in text:
    if char in letters:
        uppercase_count[letters.index(char)] += 1
    elif char.upper() in letters:
        lowercase_count[letters.index(char.upper())] += 1
    elif char in numbers:
        number_count[numbers.index(char)] += 1
    elif char in chars:
        other_count += 1
    elif char == ' ':
        space_count += 1
    elif char == '\n':
        newline_count += 1
    else:
        unknown_count += 1
        print(f"Unknown character: {char}")

labels = []
counts = []

for i in range(26):
    labels.append(letters[i].upper())
    labels.append(letters[i].lower())
    counts.append(uppercase_count[i])
    counts.append(lowercase_count[i])

labels += numbers + ["Other", "Space", "Newline", "Unknown"]
counts += number_count + [other_count, space_count, newline_count, unknown_count]

x = np.arange(len(labels))
width = 0.7

fig, ax = plt.subplots()

ax.bar(x[:52:2], counts[:52:2], width, label='Uppercase', color='#ffa7a7')
ax.bar(x[1:52:2], counts[1:52:2], width, label='Lowercase', color='#a7a7ff')

ax.bar(x[52:], counts[52:], width, color='#a7ffa7')

ax.set_ylabel('Appearances')
ax.set_title('Number of each character in a file')
ax.set_xticks(x)
ax.set_xticklabels(labels)
xticks = ax.get_xticklabels()
xticks[-4].set_rotation(90)
xticks[-3].set_rotation(90)
xticks[-2].set_rotation(90)
xticks[-1].set_rotation(90)

ax.legend()

plt.tight_layout()
plt.show()
