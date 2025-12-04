import random
import datetime


class HelperMethods:
    @staticmethod
    def generate_random_timeout(lower_bound: int = 30, upper_bound: int = 60):
        return random.randint(lower_bound, upper_bound)

    @staticmethod
    def is_failed():
        return random.random() < 0.5

    @staticmethod
    def get_current_time():
        """
        Returns the current time in Utc
        """
        return int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp())

    @staticmethod
    def generate_random_image_url():
        images = [
            "https://storage.googleapis.com/case-study-0001/mock/mock_1.png",
            "https://storage.googleapis.com/case-study-0001/mock/mock_2.png",
            "https://storage.googleapis.com/case-study-0001/mock/mock_3.png",
            "https://storage.googleapis.com/case-study-0001/mock/mock_4.png",
            "https://storage.googleapis.com/case-study-0001/mock/mock_5.png",
            "https://storage.googleapis.com/case-study-0001/mock/mock_6.jpg",
        ]
        return random.choice(images)