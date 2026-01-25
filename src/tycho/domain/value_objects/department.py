"""French Department value object."""

from typing import ClassVar

from pydantic import BaseModel, field_validator


class Department(BaseModel):
    """French Department value object with validation."""

    code: str

    # Valid French department codes
    VALID_CODES: ClassVar[set[str]] = {
        "01",
        "02",
        "03",
        "04",
        "05",
        "06",
        "07",
        "08",
        "09",
        "10",
        "11",
        "12",
        "13",
        "14",
        "15",
        "16",
        "17",
        "18",
        "19",
        "21",
        "22",
        "23",
        "24",
        "25",
        "26",
        "27",
        "28",
        "29",
        "30",
        "31",
        "32",
        "33",
        "34",
        "35",
        "36",
        "37",
        "38",
        "39",
        "40",
        "41",
        "42",
        "43",
        "44",
        "45",
        "46",
        "47",
        "48",
        "49",
        "50",
        "51",
        "52",
        "53",
        "54",
        "55",
        "56",
        "57",
        "58",
        "59",
        "60",
        "61",
        "62",
        "63",
        "64",
        "65",
        "66",
        "67",
        "68",
        "69",
        "70",
        "71",
        "72",
        "73",
        "74",
        "75",
        "76",
        "77",
        "78",
        "79",
        "80",
        "81",
        "82",
        "83",
        "84",
        "85",
        "86",
        "87",
        "88",
        "89",
        "90",
        "91",
        "92",
        "93",
        "94",
        "95",
        "2A",
        "2B",
        "971",
        "972",
        "973",
        "974",
        "976",
    }

    @field_validator("code")
    @classmethod
    def validate_department_code(cls, v: str) -> str:
        """Validate French department code."""
        if v not in cls.VALID_CODES:
            raise ValueError(f"Invalid French department code: {v}")
        return v

    def __str__(self) -> str:
        """Return string representation."""
        return self.code
