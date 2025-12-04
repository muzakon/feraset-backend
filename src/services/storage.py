from io import BytesIO
from PIL import Image
import httpx
from google.cloud import storage
from core.settings import get_settings

settings = get_settings()

class StorageService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = storage.Client()
        return cls._instance

  
    # Normal koşullarda kullanıcılara Signed URL döndürmek çok daha sağlıklı olurdu ancak bunu case-study için es geçiyorum.
    # Firebase'de tutulan alan URL değil, Blob path olmalı. Diğer türlü başka insanların ürettikleri görseller Public hale gelir. Hem veri boyutu, hem de güvenlik açısından bu daha uygundur.
    # Eğer ki uygulama içerisinde kullanıcının görsel upload etme durumu varsa da aynı şekilde, server'e yük bindirmek yerine Signed URL ile belirlenen Blob'a direkt upload edilmesi daha sağlıklı olur.
    
    # def generate_signed_url_v4(self, destination: str, minutes: int = 15):
    #     bucket: storage.Bucket = self.client.bucket(settings.GCP_BUCKET_NAME)
    #     blob = bucket.blob(destination)

    #     return blob.generate_signed_url(
    #         version="v4",
    #         expiration=datetime.timedelta(minutes=minutes),
    #         method="GET",
    #     )

  
    def upload_from_url(self, url: str, destination_blob_name: str) -> str | None:
        """
            Download an image synchronously, convert to JPEG, and upload to GCS.
        """

        try:
            response = httpx.get(url)
            response.raise_for_status()
            file_content = response.content

            # Convert to JPEG using Pillow
            input_buffer = BytesIO(file_content)
            output_buffer = BytesIO()

            with Image.open(input_buffer) as img:
                img = img.convert("RGB")
                img.save(output_buffer, format="jpeg", quality=90)

            output_buffer.seek(0)
            converted_content = output_buffer.getvalue()

            # Upload to Google Cloud Storage
            bucket: storage.Bucket = self.client.bucket(settings.GCP_BUCKET_NAME)
            blob = bucket.blob(destination_blob_name)

            blob.upload_from_string(
                converted_content,
                content_type="image/jpeg",
            )
            blob.make_public()

            return blob.public_url

        except httpx.HTTPError as e:
            print(f"HTTP error while downloading from {url}: {e}")
            return None

        except Exception as e:
            print(
                f"Error uploading or converting file from {url} to {destination_blob_name}: {e}"
            )
            return None
