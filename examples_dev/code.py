from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from typing import Union

def get_run_interval(begin: datetime) -> Union[None, timedelta]:
    delta = None
    if begin.day == 1 or begin.day == 11:
        delta = timedelta(days=10)
    elif begin.day == 21:
        next_month = begin + relativedelta(months=1)
        end = datetime(next_month.year, next_month.month, 1, next_month.hour, next_month.minute, next_month.second)
        delta = end - begin

    return delta

# datetime(year, month, day, hour, minute, second)
begin = datetime(2018, 7, 21, 00, 00, 00)
print(begin)

delta = get_run_interval(begin)

print(delta)

end = begin + delta
print(end)