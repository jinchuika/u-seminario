import calendar
from datetime import date
from calendar import Calendar

class Calendario:
    def __init__(self, *args, **kwargs):
        self.now = date.today()
        super(Calendario, self).__init__(*args, **kwargs)

    def get_dias_mes(self, year, month):
        num_days = calendar.monthrange(year, month)[1]
        days = [date(year, month, day) for day in range(1, num_days+1)]
        return days

    def get_mes_actual(self):
        return self.get_dias_mes(self.now.year, self.now.month)