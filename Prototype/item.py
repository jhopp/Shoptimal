
class Item:
    def __init__(self, name: str, quantity: int) -> None:
        self.name = name
        self.quantity = quantity # desired quantity

    def __repr__(self) -> str:
        return f"{self.name}"