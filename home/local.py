from datetime import datetime, timedelta
from django.utils import timezone
class Utility:
    def get_dates(self):
        #self.date_time = datetime.today()
        self.date_time = timezone.now()
        #self.delivery_date = datetime.today() + timedelta(1)
        self.delivery_date = timezone.now() + timedelta(1)
        return [self.date_time, self.delivery_date]

    