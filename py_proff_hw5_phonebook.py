import re


import csv
with open("phonebook_raw.csv", encoding='utf-8', newline='') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

full_name = []
for id, i in enumerate(contacts_list):
    pattern = r"(\+7|8)+\s*\(*(\d{3})\)*\s*-*(\d{3})\s*-*\s*(\d{2})\s*-*\s*(\d{2})\s*\(*([доб.]*)\s*(\d+)*\)*"
    regex = re.compile(pattern)
    result = regex.sub(r"+7(\2)\3-\4-\5\6\7", i[5])
    i[5] = result

    data_string = ','.join(i)
    pattern2 =r"(\s+)"
    regex2 = re.compile(pattern2)
    temp_string = regex2.sub(r",", data_string).split(',')
    i[0], i[1], i[2] = temp_string[0], temp_string[1], temp_string[2]
    full_name.append( (i[0] + ' ' + i[1], id))



full_name_list =[]
full_name_list = [f'{x[0]}, {x[1]}' for x in contacts_list]

add_to_contact_list = []

for id_, name in enumerate(full_name_list):
    count = 0
    for_delete = []
    for_add = []
    temp_zip_list = []
    for j, item in enumerate(contacts_list):
        if name == f"{item[0]}, {item[1]}":
            count += 1
            for_delete.append(j)
            for_add.append(item)
    if count > 1:
        add = []
        element = 0

        for_delete.reverse()
        temp_zip_list = list(zip(*for_add))

        for tuple_ in temp_zip_list:
            for cell in tuple_:
                if cell:
                    element = cell
                    break
                else:
                    element = cell
            add.append(element)
        add_to_contact_list.append(add)

        for index in for_delete:
             del contacts_list[index]


contacts_list.extend(add_to_contact_list)



with open("NEW_phonebook.csv", "w") as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerows(contacts_list)