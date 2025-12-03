import random
import datetime


class HelperMethods:
    @staticmethod
    def generate_random_timeout():
        # Todo: 30, 60 arasında random sayı üretilecek
        return random.randint(1, 10)

    @staticmethod
    def get_current_time():
        """
        Returns the current time in Utc
        """
        return int(datetime.datetime.now(tz=datetime.timezone.utc).timestamp())
