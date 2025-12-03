from google.cloud.tasks_v2 import (
    Task,
    CloudTasksClient,
    HttpMethod,
    HttpRequest,
    CreateTaskRequest,
)

from google.protobuf import timestamp_pb2
from core.settings import get_settings

import json

settings = get_settings()


class TaskManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = CloudTasksClient()
        return cls._instance

    def create_task(
        self,
        target_url: str,
        payload: dict,
        method: HttpMethod = HttpMethod.POST,
        schedule_time_seconds: int | None = None,
    ) -> Task | None:
        try:
            # 1. Prepare Request Body
            json_payload = json.dumps(payload)
            body_bytes = json_payload.encode("utf-8")

            # 2. Configure Task Request
            http_request = HttpRequest(
                http_method=method,
                url=target_url,
                oidc_token=None,  # Burada normal şartlarda güvenlik için OIDC token kullanmak önemlidir. Case-study için şimdilik atladım.
                body=body_bytes,
                headers={"Content-Type": "application/json"},
            )

            # 3. Create the Task object and apply scheduling if required
            task_options = {"http_request": http_request}

            if schedule_time_seconds:
                # Convert the Unix timestamp (seconds) into a Timestamp object for scheduling
                timestamp = timestamp_pb2.Timestamp(seconds=schedule_time_seconds)
                task_options["schedule_time"] = timestamp

            task = Task(**task_options)

            # 4. Construct the Queue Parent Path
            parent_path = self.client.queue_path(
                settings.GCP_PROJECT_ID, settings.QUEUE_LOCATION, settings.QUEUE_NAME
            )

            # 5. Send the Create Task Request
            return self.client.create_task(
                CreateTaskRequest(
                    parent=parent_path,
                    task=task,
                )
            )

        except Exception as e:
            # Log the error with specific queue context
            print(
                f"Error creating Cloud Task for queue '{settings.QUEUE_NAME}' at location '{settings.QUEUE_LOCATION}': {e}"
            )
            return None
