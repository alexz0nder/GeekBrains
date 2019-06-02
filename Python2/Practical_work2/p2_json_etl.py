import json

data_dir = 'data'
data_file = 'orders.json'

def load_json_data():
    with open(data_dir + '/' + data_file, 'r') as file:
        return json.load(file)

def write_order_to_json(item, quantity, price, buyer, date):
    data = load_json_data()
    data['orders'].append({"item": item, "quantity": quantity, "price": price, "buyer": buyer, "date": date})
    with open(data_dir + '/' + data_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

write_order_to_json('Pepsi', 20, '24 руб.', 'Иванов Иван', '02.06.2019')
