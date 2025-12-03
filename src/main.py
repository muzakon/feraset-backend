"""
Firebase Cloud Functions with service layer separation
"""

from firebase_functions import https_fn
from firebase_functions.options import set_global_options
from firebase_admin import initialize_app
from firebase_functions import firestore_fn
from services.functions.generation_callback import GenerationCallbackService
from services.functions.generation_creation import GenerationCreationService
import json

set_global_options(max_instances=1)
initialize_app()


@https_fn.on_request()
def on_callback(req: https_fn.Request) -> https_fn.Response:
    service = GenerationCallbackService()
    result = service.handle_callback(method=req.method, json_data=req.json)

    return https_fn.Response(
        response=json.dumps({"message": result["message"]}),
        mimetype="application/json",
        status=result["status"],
    )


@firestore_fn.on_document_created(document="generations/{generation_id}")
def on_generation_created(event: firestore_fn.Event) -> None:
    generation_id = event.params["generation_id"]

    service = GenerationCreationService()
    service.handle_generation_created(generation_id)
