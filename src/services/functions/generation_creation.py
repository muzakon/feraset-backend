from typing import Optional
from core.settings import get_settings
from services.cloud_tasks import TaskManager
from utils.helper import HelperMethods
import time

settings = get_settings()


class GenerationCreationService:
    """Service to handle generation creation events"""

    def __init__(
        self,
    ):
        self.task_manager = TaskManager()
        self.create_webhook = settings.CREATE_WEBHOOK == "True"
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

        if self.create_webhook:
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
        else:
            print(f"Sleeping for {timeout} seconds for generation: {generation_id}")
            time.sleep(timeout)
            print(f"Sleep completed for generation: {generation_id}")

    def handle_generation_created(self, generation_id: str) -> None:
        try:
            self.process_generation_created(generation_id)
        except Exception as e:
            print(
                f"Error handling generation created event for {generation_id}: {str(e)}"
            )
            raise
