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
