def FirstFactorial(num):
  result = 1
  if num == 0:
    return 0
  # code goes here
  for i in range(1,num+1):
    
    result *= i

  print(result)

FirstFactorial(4)
