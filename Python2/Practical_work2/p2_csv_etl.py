import csv, chardet, re, os

data_dir = 'data'

def get_data(src_data_dir):
    main_data = []
    main_data.append(['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы'])

    for file_name in [f for f in os.listdir(src_data_dir) if re.match(r'info.*.txt', f)]:
        with open(src_data_dir + '/' + file_name, 'rb') as file:
            file_data = file.read()
            source_data = file_data.decode(chardet.detect(file_data)['encoding'])
            main_data.append([
                re.findall(r'Изготовитель системы:.*', source_data)[0].split(':')[1].strip(),
                re.findall(r'Название ОС:.*', source_data)[0].split(':')[1].strip(),
                re.findall(r'Код продукта:.*', source_data)[0].split(':')[1].strip(),
                re.findall(r'Тип системы:.*', source_data)[0].split(':')[1].strip()
            ])
    return main_data

def write_to_csv(write_file):
    with open(data_dir + '/' + write_file, mode='w') as file:
        writer = csv.writer(file)
        main_data = get_data(data_dir)
        for index, _ in enumerate(main_data):
            writer.writerow([
                main_data[index][0],
                main_data[index][1],
                main_data[index][2],
                main_data[index][3]
            ])

write_to_csv('main_data.csv')
