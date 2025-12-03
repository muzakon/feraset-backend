from enum import Enum


class TaskStatus(Enum):
    IDLE = "IDLE"
    PROCESSING = "PROCESSING"
    DONE = "DONE"
    FAILED = "FAILED"
