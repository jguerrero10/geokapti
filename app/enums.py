from enum import Enum


class StatusEnum(str, Enum):
    PROCESSING = "PROCESSING"
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
