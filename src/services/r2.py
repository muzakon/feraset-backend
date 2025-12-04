from io import BytesIO
from PIL import Image
import httpx
from core.settings import get_settings
import boto3

settings = get_settings()

class R2Service:
    '''
        Normal koşullarda kullanıcılara Signed URL döndürmek çok daha sağlıklı olurdu ancak bunu case-study için es geçiyorum.
        Firebase'de tutulan alan URL değil, Blob path olmalı. Diğer türlü başka insanların ürettikleri görseller Public hale gelir. Hem veri boyutu, hem de güvenlik açısından bu daha uygundur.
        Eğer ki uygulama içerisinde kullanıcının görsel upload etme durumu varsa da aynı şekilde, server'e yük bindirmek yerine Signed URL ile belirlenen Blob'a direkt upload edilmesi daha sağlıklı olur.
    '''
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.client = boto3.client(
                service_name="s3",
                endpoint_url=settings.R2_API_URL,
                aws_access_key_id=settings.R2_ACCESS_KEY_ID,
                aws_secret_access_key=settings.R2_SECRET,
                region_name=settings.R2_REGION,
            )
        return cls._instance


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
            self.client.put_object(
                Bucket=settings.R2_BUCKET_NAME,
                Key=destination_blob_name,
                Body=converted_content,
                ContentType="image/jpeg",
            )
            
            return f"{settings.R2_PUBLIC_URL}/{destination_blob_name}"

        except httpx.HTTPError as e:
            print(f"HTTP error while downloading from {url}: {e}")
            return None

        except Exception as e:
            print(
                f"Error uploading or converting file from {url} to {destination_blob_name}: {e}"
            )
            return None
