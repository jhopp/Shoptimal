from input_data import InputData
from data_generator import DataGenerator
from schedulers import BasicScheduler

if __name__ == '__main__':
    data_generator = DataGenerator('shop_names.txt', 'product_names.txt')
    data_generator.to_csv()

    input_data = InputData.from_csv('input/')
    print(input_data)
    print(f"Unavailable: {input_data.unavailable_items()}")
    print(input_data.shop_distances())

    schedule = BasicScheduler(input_data).schedule()
    print(schedule)
    print(f"Cost: {round(schedule.cost, 2)}")
    print(f"Distance: {round(schedule.total_distance, 2)}")
    