def is_balanced(s):
    stack = []
    matching_bracket = {')': '(', '}': '{', ']': '['}

    for char in s:
        if char in matching_bracket.values():  # Opening brackets
            stack.append(char)
        elif char in matching_bracket.keys():  # Closing brackets
            if stack and stack[-1] == matching_bracket[char]:
                stack.pop()
            else:
                return "The input string is NOT balanced."

    return "The input string is balanced." if not stack else "The input string is NOT balanced."

# Input from user
s = input("Enter a string containing parentheses: ")
print(is_balanced(s))