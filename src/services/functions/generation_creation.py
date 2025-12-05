from core.settings import get_settings
from services.cloud_tasks import TaskManager
from utils.helper import HelperMethods

settings = get_settings()


class GenerationCreationService:
    """Service to handle generation creation events"""

    def __init__(
        self,
    ):
        self.task_manager = TaskManager()
        self.webhook_url = settings.WEBHOOK_URL

    def generate_timeout(self) -> int:
        return HelperMethods.generate_random_timeout(lower_bound=3, upper_bound=10)

    def schedule_webhook_task(self, generation_id: str, timeout: int) -> None:
        scheduled_at = HelperMethods.get_current_time() + timeout

        print(f"Task: {generation_id} scheduled for {timeout} seconds later.")

        self.task_manager.create_cloud_task(
            target_url=self.webhook_url,
            payload={"generation_id": generation_id},
            schedule_time_seconds=scheduled_at,
        )

    def process_generation_created(self, generation_id: str) -> None:
        timeout = self.generate_timeout()
        try:
            self.schedule_webhook_task(generation_id, timeout)
            print(
                f"Webhook task created successfully for generation: {generation_id}"
            )
        except Exception as e:
            print(
                f"Failed to create webhook task for generation {generation_id}: {str(e)}"
            )
            raise

    def handle_generation_created(self, generation_id: str) -> None:
        try:
            self.process_generation_created(generation_id)
        except Exception as e:
            print(
                f"Error handling generation created event for {generation_id}: {str(e)}"
            )
            raise
