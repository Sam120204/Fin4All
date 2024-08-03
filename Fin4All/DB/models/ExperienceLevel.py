from enum import Enum

class ExperienceLevel(Enum):
    BEGINNER = 1,
    INTERMEDIATE = 2,
    ADVANCED = 3
    @classmethod
    def from_string(cls, s):
        try:
            return cls[s]
        except KeyError:
            raise ValueError(f"'{s}' is not a valid ExperienceLevel")