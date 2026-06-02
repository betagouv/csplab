from datetime import datetime


class InvalidLimitDateError(ValueError):
    def __init__(self, limit_date: datetime):
        super().__init__(f"Invalid limit date: {limit_date}")
