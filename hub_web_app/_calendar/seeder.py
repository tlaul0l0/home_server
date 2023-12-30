from _calendar.models import Year, Day, Month
import calendar
from datetime import datetime
import locale

locale.setlocale(locale.LC_ALL, 'de_DE.utf8')

YEAR = 2023
year = Year.objects.create_year(name=YEAR)

for i in range(1, 13):
    month = Month.objects.create_month(index=i, name=calendar.month_name[i], year=year)
    for j in range(1, calendar.monthrange(YEAR, i)[1]+1):
        dt = datetime(year=YEAR, month=i, day=j)
        day = Day.objects.create_day(day=j, name=dt.strftime('%A'), name_abbr=dt.strftime('%a'), month=month)
        day.save()
    month.save()
year.save()
