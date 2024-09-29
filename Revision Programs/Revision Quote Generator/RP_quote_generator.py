import random

quote_dir = "D:\\misc\\code\\..important\\RP_quote_generator"
quote_filename = "RP_quotes.txt"
streak_filename = "streak.txt"
hide_word_chance = 0.5  # Out of 1, e.g. 0.50 = 50%

exclude_words = ['the', 'a', 'an', 'at', 'of', 'on', 'in', 'to', 'for', 'with', 'and', 'are', 'it', 'was', 'by', 'if', 'do', 'be', 'from', 'is', 'as', 'sanctity', 'parable']

def menu():
    try:
        choice = int(input(
"""
================================================================



1. Generate quote (Random)
2. Generate quote (Christianity)
3. Generate quote (Islam)

4. Quit program



================================================================

Input: """))
        
        if choice == 1:
            generate_quote("Random")
        elif choice == 2:
            generate_quote("Christianity")
        elif choice == 3:
            generate_quote("Islam")
        elif choice == 4:
            quit()
        else:
            print("Invalid option. Please enter a number between 1 and 4.")
            menu()
        
    except (TypeError, ValueError):
        print("Invalid input. Please enter a number.")
        menu()

def update_streak(streak):
    try:
        with open(f"{quote_dir}\\{streak_filename}", 'r') as streak_txt_file:
            current_streak = int(streak_txt_file.read().strip())
    
    except FileNotFoundError:
        current_streak = 0
        
    
    if streak == 0:
        current_streak = 0
    else:
        current_streak += streak
        
    with open(f"{quote_dir}\\{streak_filename}", 'w') as streak_txt_file:
        streak_txt_file.write(str(current_streak))
        
    return current_streak

def generate_quote(religion):
    print()
    
    try:
        with open(f"{quote_dir}\\{quote_filename}", 'r') as quotes_txt_file:
            quotes = [quote.strip() for quote in quotes_txt_file.readlines() if not quote.startswith("//") and quote.strip()]
            
        if quotes:
            if religion == "Random":
                filtered_quotes = quotes
            elif religion.lower() == "christianity":
                filtered_quotes = [quote for quote in quotes if extract_religion_info(quote)[0] == "Christianity"]
            elif religion.lower() == "islam":
                filtered_quotes = [quote for quote in quotes if extract_religion_info(quote)[0] == "Islam"]
            else:
                print("Invalid religion.")
                return
                
            if filtered_quotes:
                random_quote = random.choice(filtered_quotes)
                religion_info, random_quote = extract_religion_info(random_quote)
                if religion_info != "Religion not specified":
                    word_list = random_quote.split()
                    word_count = len([word for word in word_list if word.lower() not in exclude_words])
                    hide_count = 0
                    hidden_indices = []
                    for i in range(len(word_list)):
                        word = word_list[i].lower()
                        if word not in exclude_words:
                            if random.random() < hide_word_chance:
                                word_list[i] = "_" * len(word)
                                hide_count += 1
                                hidden_indices.append(i)
                            elif word_count - hide_count <= 2:
                                word_list[i] = "_" * len(word)
                                hide_count += 1
                                hidden_indices.append(i)

                    print(f"{religion_info}:")
                    guess = input(' '.join(word_list) + '\n')
                    if guess.lower() == ' '.join([word_list[i] if i not in hidden_indices else word for i, word in enumerate(random_quote.split())]).lower():
                        print(f"\nCorrect!\nYour streak is now {update_streak(1)}.")
                    else:
                        print(f"\nIncorrect. The quote was: {random_quote}.\nYour streak is now {update_streak(0)}.")
                    input("Enter to continue...")
                else:
                    print("No valid quotes found for the specified religion.")
            else:
                print(f"No quotes found for {religion}.")
        else:
            print("No quotes in the file.")
    except FileNotFoundError:
        print("Quotes file not found.")
    
    print()

def extract_religion_info(quote):
    if quote.endswith("/c"):
        return "Christianity", quote.rstrip("/c")
    elif quote.endswith("/i"):
        return "Islam", quote.rstrip("/i")
    elif quote.endswith("/b"):
        return "Both", quote.rstrip("/b")
    else:
        return "Religion not specified", quote
    
def run_program():
    menu()

while __name__ == "__main__":
    run_program()