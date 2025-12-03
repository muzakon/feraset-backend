from repositories.firebase import FirebaseRepository
from enums.status import TaskStatus
from errors.tasks import GenerationNotFoundError


class FirebaseService:
    def __init__(self):
        self.repository = FirebaseRepository()

    def validate_task(self, generation_id: str):
        task = self.repository.get_task(generation_id=generation_id)
        if not task:
            print(f"Generation: {generation_id} not found")
            raise GenerationNotFoundError(generation_id)

    def update_task(self, generation_id: str, status: TaskStatus):
        self.validate_task(generation_id=generation_id)
        self.repository.update_task(generation_id=generation_id, status=status)
