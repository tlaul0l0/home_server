from django.shortcuts import render
import datetime as dt
from . import logic

def get_calendar(request):
    year, month, days = logic.get_current_date_info()
    day_names = logic.get_all_day_names_with_abbr()

    data = {"year": year, "month": month, "days": days, "names": day_names}
    return render(request, 'calendar.html', data)
