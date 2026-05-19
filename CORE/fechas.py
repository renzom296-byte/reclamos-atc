import pandas as pd

def is_business_day(d, holidays):
    if pd.isna(d):
        return False
    d = pd.to_datetime(d).normalize()
    return d.weekday() < 5 and d not in holidays.values

def add_business_days(start_date, days, holidays):
    if pd.isna(start_date):
        return pd.NaT
    cur = pd.to_datetime(start_date).normalize()
    added = 0
    while added < days:
        cur += pd.Timedelta(days=1)
        if is_business_day(cur, holidays):
            added += 1
    return cur
