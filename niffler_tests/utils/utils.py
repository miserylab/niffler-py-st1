import datetime

date_format = "%Y-%m-%dT%H:%M:%S.%f"


class Utils:
    @staticmethod
    def get_current_date() -> str:
        return datetime.datetime.utcnow().strftime(date_format) + "Z"

    @staticmethod
    def get_timestamp() -> int:
        return int(datetime.datetime.utcnow().timestamp())

    @staticmethod
    def get_date(offset_days: int = 0) -> str:
        """
        Returns the current date in format 'DD/MM/YYYY'.

        :param offset_days: number of days from current date(positive - future date, negative - past date)
        """
        current_date = datetime.datetime.now() + datetime.timedelta(days=offset_days)
        return current_date.strftime("%d/%m/%Y")
