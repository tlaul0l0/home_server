from django.db import models

class YearManager(models.Manager):
    def create_year(self, name):
        year = self.create(name=name)
        return year

class Year(models.Model):
    name = models.IntegerField()

    objects = YearManager()

class MonthManager(models.Manager):
    def create_month(self, index, name, year):
        month = self.create(index=index, name=name, year=year)
        return month

class Month(models.Model):
    index = models.IntegerField()
    name = models.CharField(max_length=20)
    year = models.ForeignKey(Year, on_delete=models.CASCADE)

    objects = MonthManager()

class DayManager(models.Manager):
    def create_day(self, day, name, name_abbr, month):
        day = self.create(day=day, name=name, name_abbr=name_abbr, month=month)
        return day


class Day(models.Model):
    day = models.IntegerField()
    name = models.CharField(max_length=20)
    name_abbr = models.CharField(max_length=2)
    month = models.ForeignKey(Month, on_delete=models.CASCADE)

    objects = DayManager()
