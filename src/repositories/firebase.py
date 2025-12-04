from firebase_admin import firestore
from enums.generations import GenerationStatus
from core.settings import get_settings

settings = get_settings()


class FirebaseRepository:
    def __init__(self):
        self.db = firestore.client()
        self.collection_name = settings.COLLECTION_NAME

    def get_generation(self, generation_id: str) -> dict | None:
        try:
            doc_ref = self.db.collection(self.collection_name).document(generation_id)
            doc_snapshot = doc_ref.get()

        except Exception as e:
            print(f"CRITICAL: Firestore error getting {generation_id}: {e}")
            raise

        if not doc_snapshot.exists:
            return None

        return doc_snapshot.to_dict()

    def update_generation(self, generation_id: str, status: GenerationStatus, image_url: str):
        try:
            self.db.collection(self.collection_name).document(generation_id).update(
                {"status": status.value, "result": image_url}
            )
        except Exception as e:
            print(f"CRITICAL: Firestore error updating {generation_id}: {e}")
            raise
