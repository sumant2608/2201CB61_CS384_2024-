def find_unique_triplets(nums):
  nums.sort()
  triplets=[]
  for i in range (len(nums)):
     if i>0 and nums[i]==nums[i-1]:
       continue

  left ,right = i+1 , len(nums)-1
  while left<right:
       current_sum = nums[i]+nums[left]+nums[right]
       if current_sum==0:
         triplets.append([nums[i],nums[left],nums[right]])
         left+=1
         right-=1
         while left<right and nums[left]==nums[left-1]:
           left+=1
         while left<right and nums[right]==nums[right+1]:
           right-=1

       elif current_sum<0:
         left+=1
       else:
         right-=1
  return triplets

nums = list(map(int,input("enter list of number : ").split()))
result = find_unique_triplets(nums)
print(result)