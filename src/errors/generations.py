import time

class GenerationNotFoundError(Exception):
    """Raised when a generation cannot be found."""

    def __init__(self, generation_id: str):
        self.generation_id = generation_id
        super().__init__(f"Generation with id {generation_id} not found")


class UploadError(Exception):
    """Raised when a upload error occured to google cloud storage."""

    def __init__(self, generation_id: str):
        self.generation_id = generation_id
        super().__init__(f"Generation with id {generation_id} has failed")
