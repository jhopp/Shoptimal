from input_data import InputData
from data_generator import DataGenerator
from schedulers import BasicScheduler, Model1Scheduler, BestPriceScheduler, Model2Scheduler
from validators import ScheduleValidator

if __name__ == '__main__':
    data_generator = DataGenerator('shop_names.txt', 'product_names.txt')
    data_generator.to_csv(all_items_available=True)

    input_data = InputData.from_csv('input/')

    #print(input_data)
    #print(f"Unavailable: {input_data.unavailable_items()}")
    #print(input_data.shop_distances())

    basic_schedule = BasicScheduler(input_data).schedule()
    print(basic_schedule)
    print(f"Cost: {round(basic_schedule.cost, 2)}")
    print(f"Distance: {round(basic_schedule.duration, 2)}")
    ScheduleValidator(input_data, basic_schedule).validate()

    cheap_schedule = BestPriceScheduler(input_data).schedule()
    print(cheap_schedule)
    print(f"Cost: {round(cheap_schedule.cost, 2)}")
    print(f"Distance: {round(cheap_schedule.duration, 2)}")
    ScheduleValidator(input_data, cheap_schedule).validate()

    model1_schedule = Model1Scheduler(input_data).schedule(kpi_cost=7,kpi_distance=1)
    print(model1_schedule)
    print(f"Cost: {round(model1_schedule.cost, 2)}")
    print(f"Distance: {round(model1_schedule.duration, 2)}")
    ScheduleValidator(input_data, model1_schedule).validate()

    model2_schedule = Model2Scheduler(input_data).schedule(kpi_cost=7,kpi_distance=1)
    print(model2_schedule)
    print(f"Cost: {round(model2_schedule.cost, 2)}")
    print(f"Distance: {round(model2_schedule.duration, 2)}")
    ScheduleValidator(input_data, model2_schedule).validate()
    