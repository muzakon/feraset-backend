from services.firebase import FirebaseService
from services.r2 import R2Service
from utils.helper import HelperMethods
from enums.generations import GenerationStatus
from errors.generations import GenerationNotFoundError, UploadError
import uuid


class GenerationCallbackService:
    """Service to handle generation callback processing"""

    def __init__(self):
        self.firebase_service = FirebaseService()
        self.r2_service = R2Service()

    def validate_request(self, method: str, json_data: dict) -> tuple[bool, str, int]:
        if method != "POST":
            return False, "Only POST requests are accepted", 405

        if not json_data or not json_data.get("generation_id"):
            return False, "Generation ID is required", 200

        return True, "", 200

    def upload_image_to_bucket(self, generation_id: str):
        mock_url = HelperMethods.generate_random_image_url()
        public_url = self.r2_service.upload_from_url(
            url=mock_url, destination_blob_name=f"logo-generations/{uuid.uuid4()}.jpeg"
        )

        if not public_url:
            raise UploadError(generation_id)

        return public_url

    def process_generation_callback(self, json_data: dict) -> tuple[str, int]:
        try:
            generation_id = json_data.get("generation_id")
            is_failed = HelperMethods.is_failed()
            new_status = GenerationStatus.FAILED if is_failed else GenerationStatus.DONE
            image_url = None

            if not is_failed:
                image_url = self.upload_image_to_bucket(generation_id=generation_id)

            self.firebase_service.update_generation(
                generation_id=generation_id, status=new_status, image_url=image_url
            )

            print(
                f"Generation {generation_id} processed successfully with status: {new_status.value}"
            )
            return "OK", 200

        except GenerationNotFoundError:
            # Return 200 to prevent retry for non-existent generations
            print(f"Generation not found: {generation_id}")
            return "Generation not found", 200

        except UploadError:
            # Return 200 to prevent retry for non-existent generations
            print(f"Generation upload failed: {generation_id}")
            return "Generation upload failed", 200

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
        message, status = self.process_generation_callback(json_data)

        return {"message": message, "status": status}
