from datetime import datetime, timedelta

class Utility:
    def get_dates(self):
        self.date_time = datetime.today()
        self.delivery_date = datetime.today() + timedelta(1)
        return [self.date_time, self.delivery_date]