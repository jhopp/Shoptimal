from input_data import InputData
from data_generator import DataGenerator

if __name__ == '__main__':
    data_generator = DataGenerator('shop_names.txt', 'product_names.txt')
    data_generator.to_csv()

    input_data = InputData.from_csv('')
    print(input_data)