from collections import defaultdict, Counter
from itertools import permutations

def group_anagrams(words):
    # Dictionary to store grouped anagrams
    anagram_dict = defaultdict(list)

    # Group words by sorted character tuple (used as key)
    for word in words:
        sorted_word = ''.join(sorted(word))
        anagram_dict[sorted_word].append(word)

    # Prepare the output dictionary with a canonical form as the key
    output_dict = {}
    for group in anagram_dict.values():
        canonical_form = sorted(group)[0]  # Choose the first word in sorted order as canonical form
        output_dict[canonical_form] = group

    return output_dict

def calculate_frequency(anagram_groups):
    frequency_dict = {}

    # Calculate total character frequency for each group
    for key, words in anagram_groups.items():
        combined_counter = Counter()
        for word in words:
            combined_counter.update(word)

        # Each character's frequency multiplied by the number of words in the group
        total_frequency = {char: count * len(words) for char, count in combined_counter.items()}
        frequency_dict[key] = total_frequency

    return frequency_dict

def generate_anagrams(word):
    # Generate all permutations of the word
    permuted_words = set(''.join(p) for p in permutations(word))
    # Remove the original word from the set of anagrams
    permuted_words.discard(word)
    return list(permuted_words)

def expand_anagram_groups(anagram_groups):
    # Expand each anagram group by generating more anagrams
    expanded_groups = {}

    for key, words in anagram_groups.items():
        # Generate additional anagrams for each canonical form
        additional_anagrams = generate_anagrams(key)

        # Remove already existing words from generated anagrams
        new_anagrams = [ana for ana in additional_anagrams if ana not in words]

        # Add the new anagrams to the group
        expanded_groups[key] = words + new_anagrams

    return expanded_groups

def find_highest_frequency_group(frequency_dict):
    # Find the group with the highest total character frequency
    max_frequency = 0
    max_group = None

    for key, freq in frequency_dict.items():
        total_frequency = sum(freq.values())
        if total_frequency > max_frequency: # This line was not indented correctly, causing the error. Fixed the indentation here.
            max_frequency = total_frequency
            max_group = key

    return max_group

# Input words from the user
words = input("Enter words separated by spaces: ").split()

# Step 1: Group anagrams
anagram_groups = group_anagrams(words)
print("\nAnagram Dictionary (Initial):")
print(anagram_groups)

# Step 2: Expand anagram groups by generating new anagrams
expanded_anagram_groups = expand_anagram_groups(anagram_groups)
print("\nAnagram Dictionary (Expanded with Generated Anagrams):")
print(expanded_anagram_groups)

# Step 3: Calculate character frequency for each group
frequency_dict = calculate_frequency(expanded_anagram_groups)
print("\nCharacter Frequencies for Each Anagram Group:")
for group, freq in frequency_dict.items():
    print(f"{group}: {freq}")

# Step 4: Find the group with the highest total character frequency
highest_frequency_group = find_highest_frequency_group(frequency_dict)
print("\nGroup with the Highest Total Character Frequency:")
print(f"{highest_frequency_group}: {frequency_dict[highest_frequency_group]}")