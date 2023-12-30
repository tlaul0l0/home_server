from datetime import datetime
import calendar
import locale
from .models import Year, Month, Day

def get_current_date_info():
    """
    @returns: day, name of month and year of current date in german
    """
    # get current day info
    current_day = datetime.now()
    day = current_day.day
    month = current_day.month
    year = current_day.year
    
    return get_months_info(year=year, month=month)


def get_months_info(year, month):
    """
    loads all days of a given month of a given year from database
    @returns: year object, month object and all day objects"""
    year_obj = Year.objects.filter(name=year).get()
    month_obj = Month.objects.filter(index=month).filter(year=year_obj.id).get()
    days_obj = Day.objects.filter(month=month_obj.id)

    return year_obj, month_obj, days_obj

def get_all_day_names_with_abbr():
    """
    generates names of days and its abbreviation in german
    @returns: dict of name:abbr, e.g.: montag:mo
    """
    locale.setlocale(locale.LC_ALL, 'de_DE.utf8')
    day_names = list(calendar.day_name)
    day_abbr = list(calendar.day_abbr)
    return dict(zip(day_names, day_abbr))
