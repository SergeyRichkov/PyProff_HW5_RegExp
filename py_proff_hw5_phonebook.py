import re
import csv


def file_reading(path):
    with open(path, encoding='utf-8', newline='') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    return contacts_list


def string_normalize(contacts_list_wrong):
    for id_, i in enumerate(contacts_list_wrong):
        pattern = r"(\+7|8)+\s*\(*(\d{3})\)*\s*-*(\d{3})\s*-*\s*" \
                  r"(\d{2})\s*-*\s*(\d{2})\s*\(*([доб.]*)\s*(\d+)*\)*"
        regex = re.compile(pattern)
        result = regex.sub(r"+7(\2)\3-\4-\5\6\7", i[5])
        i[5] = result

        data_string = ','.join(i)
        pattern2 = r"(\s+)"
        regex2 = re.compile(pattern2)
        temp_string = regex2.sub(r",", data_string).split(',')
        i[0], i[1], i[2] = temp_string[0], temp_string[1], temp_string[2]

    contacts_list_right = contacts_list_wrong.copy()
    return contacts_list_right


def double_remove(list_with_double):
    full_name_list = [f'{x[0]}, {x[1]}' for x in list_with_double]
    add_to_contact_list = []

    for id_, name in enumerate(full_name_list):
        count = 0
        for_delete = []
        for_add = []
        for j, item in enumerate(list_with_double):
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
                del list_with_double[index]
    list_with_double.extend(add_to_contact_list)
    list_without_double = list_with_double.copy()
    return list_without_double


def write_to_file(list_without_double):
    with open("NEW_phonebook.csv", "w", newline='') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(list_without_double)
    return print('файл успешно записан')


if __name__ == '__main__':
    path = "phonebook_raw.csv"
    contacts_list_wrong = file_reading(path)
    list_with_double = string_normalize(contacts_list_wrong)
    list_without_double = double_remove(list_with_double)
    write_to_file(list_without_double)
