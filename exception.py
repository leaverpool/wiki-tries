try:
  a = 6 + b
except SyntaxError:
  print('Ошибка SyntaxError!')
  a = 0
except NameError:
  print('Ошибка NameError! b не определена')
  a = 0

try:
  print(x + 5)
except NameError:
  print('Ошибка NameError! х не определён')

