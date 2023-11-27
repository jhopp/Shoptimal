from input_data import InputData
from data_generator import DataGenerator
from schedulers import BasicScheduler

if __name__ == '__main__':
    data_generator = DataGenerator('shop_names.txt', 'product_names.txt')
    data_generator.to_csv()

    input_data = InputData.from_csv('input/')
    print(input_data)
    print(input_data.unavailable_items())

    schedule = BasicScheduler(input_data).schedule()
    print(schedule)
    print(round(schedule.cost, 2))
    