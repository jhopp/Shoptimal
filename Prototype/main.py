from input_data import InputData
from data_generator import DataGenerator
from schedulers import BasicScheduler, Model1Scheduler
from validators import ScheduleValidator

if __name__ == '__main__':
    data_generator = DataGenerator('shop_names.txt', 'product_names.txt')
    data_generator.to_csv()

    input_data = InputData.from_csv('input/')

    while len(input_data.unavailable_items()) > 0: # force no unavailable items for now
        data_generator = DataGenerator('shop_names.txt', 'product_names.txt')
        data_generator.to_csv()
        input_data = InputData.from_csv('input/')
        print(input_data.unavailable_items())

    print(input_data)
    print(f"Unavailable: {input_data.unavailable_items()}")
    #print(input_data.shop_distances())

    basic_schedule = BasicScheduler(input_data).schedule()
    print(basic_schedule)
    print(f"Cost: {round(basic_schedule.cost, 2)}")
    print(f"Distance: {round(basic_schedule.total_distance, 2)}")
    ScheduleValidator(input_data, basic_schedule).validate()

    model1_schedule = Model1Scheduler(input_data).schedule(0.5,0.5)
    print(model1_schedule)
    print(f"Cost: {round(model1_schedule.cost, 2)}")
    print(f"Distance: {round(model1_schedule.total_distance, 2)}")
    ScheduleValidator(input_data, model1_schedule).validate()
    