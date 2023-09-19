num = int(input("Enter a number: "))
num2 = int(input("Enter another number: "))
operator = input("Enter either + or - to add or subtract the numbers: ")

if operator == "+":
  print(num + num2)
elif operator == "-":
  print(num - num2)
else: 
  print("Invalid operator")
