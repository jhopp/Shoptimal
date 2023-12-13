from abc import ABC, abstractmethod
from input_data import InputData
from schedule import Schedule

class ScheduleChecker(ABC):
    def __init__(self, input_data: InputData, schedule: Schedule):
        """
        Checks that the given schedule meets some criterion.
        """
        self._input_data = input_data
        self._schedule = schedule

    @abstractmethod
    def check(self):
        pass

class AllItemsArePurchased(ScheduleChecker):
    def check(self) -> bool:
        """
        Checks that all items have been purchased.
        """
        item_set = self._schedule.to_itemset()
        for item in self._input_data.items:
            if item.name not in item_set:
                return False
        return True

class AllPurchasesAreValid(ScheduleChecker):
    def check(self) -> bool:
        """
        Checks that all items are purchased at a shop that sells that item.
        """
        for decision in self._schedule.shop_decisions:
            if decision.item not in decision.shop.available_products():
                return False
        return True

class ScheduleValidator:
    def __init__(self, input_data: InputData, schedule: Schedule):
        self._input_data = input_data
        self._schedule = schedule
        self._checker_classes = [
            AllItemsArePurchased
        ]

    def validate(self) -> None:
        for checker_cls in self._checker_classes:
            checker = checker_cls(schedule=self._schedule, input_data=self._input_data)
            is_valid = checker.check()
            print(f"{checker_cls.__name__:30s} : {'PASS' if is_valid else 'FAIL'}")