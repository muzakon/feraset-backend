from services.firebase import FirebaseService
from utils.helper import HelperMethods
from enums.generations import GenerationStatus
from errors.generations import GenerationNotFoundError


class GenerationCallbackService:
    """Service to handle generation callback processing"""

    def __init__(self):
        self.firebase_service = FirebaseService()

    def validate_request(self, method: str, json_data: dict) -> tuple[bool, str, int]:
        if method != "POST":
            return False, "Only POST requests are accepted", 405

        if not json_data or not json_data.get("generation_id"):
            return False, "Generation ID is required", 200

        return True, "", 200

    def process_generation_callback(self, generation_id: str | None) -> tuple[str, int]:
        try:
            # Simulate processing and determine if failed
            is_failed = HelperMethods.is_failed()

            # Update generation status
            new_status = GenerationStatus.FAILED if is_failed else GenerationStatus.DONE

            self.firebase_service.update_generation(
                generation_id=generation_id, status=new_status
            )

            print(
                f"Generation {generation_id} processed successfully with status: {new_status.value}"
            )
            return "OK", 200

        except GenerationNotFoundError:
            # Return 200 to prevent retry for non-existent generations
            print(f"Generation not found: {generation_id}")
            return "Generation not found", 200

        except Exception as e:
            # Return 500 to trigger retry for unexpected errors
            print(f"Error processing generation {generation_id}: {str(e)}")
            return "Internal Server Error", 500

    def handle_callback(self, method: str, json_data: dict) -> dict[str, any]:
        # Validate request
        is_valid, message, status = self.validate_request(method, json_data)
        if not is_valid:
            return {"message": message, "status": status}

        # Process generation
        generation_id = json_data.get("generation_id")
        message, status = self.process_generation_callback(generation_id)

        return {"message": message, "status": status}
