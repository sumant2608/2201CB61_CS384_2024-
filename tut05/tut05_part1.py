def find_unique_triplets(nums):
    # Sort the list to simplify the process of avoiding duplicates
    nums.sort()
    triplets = []

    # Iterate through the list
    for i in range(len(nums)):
        # Avoid duplicate values for the first element
        if i > 0 and nums[i] == nums[i - 1]:
            continue

        # Use two pointers to find the remaining two numbers
        left, right = i + 1, len(nums) - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            
            if total == 0:
                triplets.append([nums[i], nums[left], nums[right]])
                
                # Move the left pointer to the next unique value
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                # Move the right pointer to the next unique value
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                
                left += 1
                right -= 1
            elif total < 0:
                left += 1
            else:
                right -= 1

    return triplets


# Input from user
user_input = input("Enter a list of integers separated by spaces: ")
nums = list(map(int, user_input.split()))

# Output
result = find_unique_triplets(nums)
print("Unique triplets that sum up to zero:", result)
