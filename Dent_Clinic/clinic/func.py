import datetime


def number_of_days(date: datetime.date):
    first_day_of_next_month = date.replace(day=1, month=(date.month + 1) % 12 if date.month != 11 else 1)
    last_day_of_current_month = first_day_of_next_month - datetime.timedelta(days=1)

    return last_day_of_current_month.day


def make_calendar_page(today: datetime.date):
    num_of_days = number_of_days(today)

    calendar = [[[None, None] for j in range(7)] for i in range(6)]
    start = today.weekday()

    prev_month = number_of_days(datetime.date(year=today.year - 1 if today.month == 12 else today.year,
                                              month=today.month - 1 if today.month != 1 else 12,
                                              day=1)) - start + 1
    next_month = 1

    count = 1

    for week in range(6):
        for day in range(7):
            if week == 0 and day < start:
                calendar[week][day] = [prev_month, -1]
                prev_month += 1

            elif count > num_of_days:
                calendar[week][day] = [next_month, 1]
                next_month += 1

            else:
                calendar[week][day] = [count, 0]
                count += 1

    return calendar
