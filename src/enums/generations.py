from enum import Enum


class GenerationStatus(Enum):
    IDLE = "IDLE"
    PROCESSING = "PROCESSING"
    DONE = "DONE"
    FAILED = "FAILED"
