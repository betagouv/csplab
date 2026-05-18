from dataclasses import dataclass


@dataclass(frozen=True)
class Diploma:
    MAX_DIPLOMA_LEVEL = 8
    MIN_DIPLOMA_LEVEL = 1

    value: int  # 1-8=CNCP levels

    def __new__(cls, value: int):
        if not isinstance(value, int):
            raise ValueError("Diploma level must be an integer")
        if value < cls.MIN_DIPLOMA_LEVEL or value > cls.MAX_DIPLOMA_LEVEL:
            raise ValueError("Diploma level must be between 1 and 8")

        return super().__new__(cls)

    def __str__(self) -> str:
        return str(self.value)
