import csv

## проверяем, есть ли уже запись в сегодняшнем файле, добавляем с нулялми, если нет
found_today = 0
that_user_id = str(292397556)
with open(r'stol_order_today.csv', newline='', encoding='utf-8') as f:
    for row in csv.reader(f, dialect='excel-tab'):
        if row and row[0] == that_user_id:
            found_today = 1
            break
if found_today == 0:
    with open(r'stol_order_today.csv', 'a', newline='', encoding='utf-8') as f:
        row = [that_user_id, '1', '0', '0', '0', '0', '0']
        csv.writer(f, dialect='excel-tab').writerow(row)

## ищем уже точно существующую строку с айди пользователя и прибавляем +1 первое
new_rows = []
perv = 0
with open(r'stol_order_today.csv', encoding='utf-8') as f:
    for row in csv.reader(f, dialect='excel-tab'):
        print(row)
        new_row = row
        if row and row[0] == that_user_id:  # ищем строку с айди пользоваетля в сегодняшнем файле
            print('FOUNDED USER! lets update shit')
            new_row = [row[0], int(row[1]) + 1, row[2], row[3], row[4], row[5], row[6]]
            perv = int(row[1]) + 1
            print(str(perv))
        new_rows.append(new_row)  # add the modified rows
# overwrite old shit with new temp shit
with open(r'stol_order_today.csv', 'w', newline='', encoding='utf-8') as f:  # 'a' - append - добавляем, 'w' - заменяем
    for row in new_rows:
        csv.writer(f, dialect='excel-tab').writerow(row)

print(type(perv))
