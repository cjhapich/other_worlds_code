import matplotlib.pyplot as plt
from datetime import date
import math
import numpy as np
plt.style.use('dark_background')
earth_year_length = 365.2425


def is_leap_year(year_num):
    if (year_num % 4) == 0 and (year_num % 100) != 0:
        return True
    elif (year_num % 100) == 0 and (year_num % 400) != 0:
        return False
    elif (year_num % 100) == (year_num % 400) == 0:
        return True
    else:
        return False


def days_in_month(m, y):
    if m in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    elif m in [4, 6, 9, 11]:
        return 30
    else:
        return 28 + is_leap_year(y)


def day_of_year(m, d, y):
    num = d
    month = 1
    while month < m:
        num += days_in_month(month, y)
        month += 1
    return int(num)


def days_left(m, d, y):
    day = day_of_year(m, d, y)
    leap = is_leap_year(y)
    if leap is True:
        return 366 - day
    else:
        return 365 - day


def days_in_between(y1, y2):
    y = y1 + 1
    days = 0
    while y < y2:
        if is_leap_year(y):
            days += 366
        else:
            days += 365
        y += 1
    return days


def days_since_birth(m, d, y):  # Date of birth as input
    mt = date.today().month
    dt = date.today().day
    yt = date.today().year
    if y != yt:
        in_birth_year = days_left(m, d, y)
        in_this_year = day_of_year(mt, dt, yt)
        in_between = days_in_between(y, yt)
        days = in_birth_year + in_this_year + in_between
    else:
        birthday = day_of_year(m, d, y)
        today = day_of_year(mt, dt, yt)
        days = today - birthday
    return days


def new_date(days):
    days_count = days
    m = date.today().month
    d = date.today().day
    y = date.today().year
    ly = is_leap_year(y)
    while days_count >= 365 + ly:
        days_count -= 365 + ly
        y += 1
        ly = is_leap_year(y)
    while days_count >= days_in_month(m, y):
        days_count -= days_in_month(m, y)
        if m < 12:
            m += 1
        else:
            y += 1
            m = 1
    if days_count >= 1:
        if (d + days_count) <= days_in_month(m, y):
            d += days_count
        else:
            if m < 12:
                days_count -= days_in_month(m, y)
                m += 1
                d += days_count
            else:
                days_count -= days_in_month(m, y)
                y += 1
                m = 1
                d += days_count
    return m, d, y


def next_birthday(planet_age_years, planet_year_length):
    new_age = math.ceil(planet_age_years)
    earth_days_left = (new_age - planet_age_years) * planet_year_length
    return earth_days_left


"""Below code is set up to produce Figure 3 in the analysis. To reproduce Figure 2 change entries to 100.
To reproduce Figure 1 change entries to 100, apply math.floor to earth_days_left in next_birthday function,
and change next_birthday_float plot to a scatter plot."""
entries = 400
y = [x for x in range(0, entries)]
birth_year_list = []
next_birthday_float = []
test_month, test_day, test_year = new_date(10)  # Test a birthday ten days from current date at various birth years

for i in y:
    birth_year = test_year - i
    birth_year_list += [birth_year]
    days_old = days_since_birth(test_month, test_day, birth_year)
    next_birthday_float += [next_birthday(days_old / earth_year_length, earth_year_length)]
avg_value = np.mean(next_birthday_float)
print(avg_value)
"""
Ultimately, your birthday is the day on the calendar. But an integer number of 'days' until the
next integer multiple of 'years' can drift to place your birthday one day before or after that same
calendar day the way leap years are placed over the 400 year cycle.
"""
avg = np.full((entries, 1), avg_value)  # Plottable array of average
true = np.full((entries, 1), 10)  # Plottable array of true value
plt.plot(birth_year_list, avg, label='Mean')
plt.plot(birth_year_list, true, label='True value')
plt.grid()
plt.plot(birth_year_list, next_birthday_float, label='Days until next Earth birthday', marker='o', markersize=3, linewidth=1)
plt.title('Non-integer days until next birthday this year for past 400 birth years')
plt.legend(); plt.xlabel('Birth year'); plt.ylabel('Days until next birthday')
plt.show()
