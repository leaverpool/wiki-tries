class Matrix:
  def __init__(self, rows, columns):
    self.rows = rows
    self.columns = columns
    self.data = [[0 for x in range(rows)] for y in range(columns)] 
  def rows_count(self):
    return self.rows
  def columns_count(self):
    return self.columns
  def sett(self, i, j, value):
    self.data[i][j] = value
  def get(self, i, j):
    return self.data[i][j]
  
  # просто выводим сумму матриц
  # def __add__(self, other):
  #   res = []
  #   for i in range(len(self.data)):
  #       row = []
  #       for j in range(len(self.data[0])):
  #           row.append(self.data[i][j] + other.data[i][j])
  #       res.append(row)
  #   return res


  def __add__(self, other):
    res = Matrix(len(self.data), len(self.data[0]))
    for i in range(len(self.data)):  # rows```
        row = []
        for j in range(len(self.data[0])):  # columns
            res.sett(i, j, self.data[i][j] + other.data[i][j])
    return res   


  def __sub__(self, other):
    pass
  def __mul__(self, other):
    pass
  def __str__(self):
    return(str(self.data))
  def scalar_mul(self, other):
    pass


m1 = Matrix(3, 3)
m2 = Matrix(3, 3)

print(m1.rows_count())
print(m1.columns_count())
print(m1.get(2,2))

for i in range(3):
  m1.sett(i,i,6)
  m2.sett(2-i, 2-i, 4)

print(m2.data)
print(m1.data)



m3 = m1 + m2

print('SUMMA:', m3.data)
print(m3)




