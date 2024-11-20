str1=input('enter string')

def str_compress(str1):
  compress = " "
  length = len(str1)


  i = 0
  while i < length:
    count =1
    char = str1[i]


    while i +1 < length and str1[i] == str1[i+1]:
      count += 1
      i += 1
    compress += char + str(count)
    i += 1
  return compress
print(str_compress(str1))