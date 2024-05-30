class Cell:
    def __init__(self, value=None):
        self.value = value
        if self.value is not None:
            self.domain = [self.value]
        else:
            self.domain = [1, 2, 3, 4, 5, 6, 7, 8, 9]

    def set_value(self, value: int) -> None:
        self.value = value
        self.domain = [self.value]