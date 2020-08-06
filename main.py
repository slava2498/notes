import calendar
import datetime
now = datetime.datetime.now()
print(calendar.monthrange(now.year, 1)[1])