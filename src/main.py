from firebase_functions import https_fn
from firebase_functions.options import set_global_options
from firebase_admin import initialize_app
from firebase_functions import firestore_fn
from core.settings import get_settings
from services.tasks import TaskManager
from utils.helper import HelperMethods
from services.firebase import FirebaseService
from enums.generations import GenerationStatus
from errors.generations import GenerationNotFoundError
import time
import json

settings = get_settings()

set_global_options(max_instances=1)
initialize_app()


@https_fn.on_request()
def on_callback(req: https_fn.Request) -> https_fn.Response:
    # Birinci adımda Request method kontrolü yapalım. Çünkü "on_generation_created" fonksiyonunda POST method ile task oluşturdum.
    if req.method != "POST":
        # METHOD_NOT_ALLOWED döndürmemiz kâfi. Case-study olması sebebiyle direkt olarak 405 (int) şeklinde döndürüyorum. Normal koşullarda Enum daha sağlıklı olur.
        return https_fn.Response(
            response=json.dumps({"message": "Only POST requests are accepted"}),
            mimetype="application/json",
            status=405,
        )

    generation_id = req.json.get("generation_id")
    if not generation_id:
        # Normal şartlarda 404, ya da 4XX döndürmemiz daha mantıklı olurdu ancak task retry'e girmesin diye direkt olarak 200 döndürüyorum.
        return https_fn.Response(
            response=json.dumps({"message": "Generation  is required"}),
            mimetype="application/json",
            status=200,
        )

    firebase_service = FirebaseService()
    try:
        firebase_service.update_generation(
            generation_id=generation_id, status=GenerationStatus.DONE
        )

    # Aynı şekilde burada da 200 döndürüyorum. Task yok ise retry etmesine gerek yok.
    except GenerationNotFoundError:
        return https_fn.Response(
            response=json.dumps({"message": "Generation not found"}),
            mimetype="application/json",
            status=200,
        )

    # Burada bilmediğimiz bir sebepten kaynaklı bir problem yaşanmış ise Retry edilmesinde problem yok.
    except Exception:
        return https_fn.Response(
            response=json.dumps({"message": "Internal Server Error"}),
            mimetype="application/json",
            status=500,
        )

    return https_fn.Response(
        response=json.dumps({"message": "OK"}), mimetype="application/json", status=200
    )


@firestore_fn.on_document_created(document="generations/{generation_id}")
def on_generation_created(event: firestore_fn.Event) -> None:
    generation_id = event.params["generation_id"]
    timeout = HelperMethods.generate_random_timeout()
    if settings.CREATE_WEBHOOK == "True":
        scheduled_at = HelperMethods.get_current_time() + timeout
        print(f"Task: {generation_id} scheduled for {timeout} seconds later.")
        task_manager = TaskManager()
        task_manager.create_generation(
            target_url=settings.WEBHOOK_URL,
            payload={"generation_id": generation_id},
            schedule_time_seconds=scheduled_at,
        )
    else:
        time.sleep(timeout)
