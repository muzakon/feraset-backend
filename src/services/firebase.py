from repositories.firebase import FirebaseRepository
from enums.generations import GenerationStatus
from errors.generations import GenerationNotFoundError


class FirebaseService:
    def __init__(self):
        self.repository = FirebaseRepository()

    def validate_generation(self, generation_id: str):
        task = self.repository.get_generation(generation_id=generation_id)
        if not task:
            print(f"Generation: {generation_id} not found")
            raise GenerationNotFoundError(generation_id)
        
    def update_generation(self, generation_id: str, status: GenerationStatus, image_url: str | None):
        self.validate_generation(generation_id=generation_id)
        self.repository.update_generation(generation_id=generation_id, status=status, image_url=image_url)
