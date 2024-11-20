n=int(n)
def sum_of_digits(n):

    while n >= 10:
      sum = 0
      while  n > 0:
        sum += n % 10
        n //= 10


      n = sum
    return sum
print(sum_of_digits(n))