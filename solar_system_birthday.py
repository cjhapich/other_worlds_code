"""
Non-Earth years defined relative to sidereal year. Our calendar is defined (approximately)
relative to the tropical earth year since our operations are with respect to the seasons, but on
other worlds with complicated or unknown tropical years we can use the year with respect to the stars.
"""

from datetime import date
import math

# Units of earth days, obtained from https://nssdc.gsfc.nasa.gov/planetary/factsheet/
mercury_year_length = 87.97
venus_year_length = 224.70
earth_year_length = 365.2425  # Gregorian calendar year definition
mars_year_length = 686.98
ceres_year_length = 1680.82
jupiter_year_length = 4332.59
saturn_year_length = 10759.22
uranus_year_length = 30685.4
neptune_year_length = 60189.0
pluto_year_length = 90560.0

earth_weeks = 52.1789  # Weeks in a year


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
    month_count = 1
    while month_count < m:
        num += days_in_month(month_count, y)
        month_count += 1
    return int(num)


def days_left(m, d, y):  # Return number of days left in the year for a given date
    day_num = day_of_year(m, d, y)
    leap = is_leap_year(y)
    if leap is True:
        return 366 - day_num
    else:
        return 365 - day_num


def days_in_between(y1, y2):  # Return number of days elapsed between two years excluding the days in those years
    y = y1 + 1
    days = 0
    while y < y2:
        if is_leap_year(y):
            days += 366
        else:
            days += 365
        y += 1
    return days


def days_since_birth(m, d, y):  # Date of birth as arguments
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


def new_date(n):  # Return the calendar date that is n days from today's date
    days_count = n
    m = date.today().month
    d = date.today().day
    y = date.today().year
    leap = is_leap_year(y)
    while days_count >= 365 + leap:
        days_count -= 365 + leap
        y += 1
        leap = is_leap_year(y)
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
    earth_days_left = math.floor((new_age - planet_age_years) * planet_year_length)
    birthday_month, birthday_day, birthday_year = new_date(earth_days_left)
    return birthday_month, birthday_day, birthday_year


def next_birthday_earth(m, d):  # Earth birthdays are different due to leap years, see analysis for details
    y = date.today().year
    if m >= date.today().month:
        if d >= date.today().day:
            return y
        else:
            return y + 1
    else:
        return y + 1


def next_half_birthday(planet_age_years, planet_year_length):
    fractional_age = planet_age_years % 1
    if fractional_age >= 0.5:
        half_birthday = math.ceil(planet_age_years) + 0.5
        earth_days_left = math.floor((half_birthday - planet_age_years) * planet_year_length)
        half_birthday_month, half_birthday_day, half_birthday_year = new_date(earth_days_left)
        return half_birthday_month, half_birthday_day, half_birthday_year
    if fractional_age < 0.5:
        half_birthday = math.floor(planet_age_years) + 0.5
        earth_days_left = math.floor((half_birthday - planet_age_years) * planet_year_length)
        half_birthday_month, half_birthday_day, half_birthday_year = new_date(earth_days_left)
        return half_birthday_month, half_birthday_day, half_birthday_year


bd = input('Enter your birthday (MM/DD/YYYY): ')
m_d_y = bd.split('/')
month = int(m_d_y[0])
day = int(m_d_y[1])
year = int(m_d_y[2])

since_birth = days_since_birth(month, day, year)
mercury_age = since_birth / mercury_year_length
venus_age = since_birth / venus_year_length
earth_age = since_birth / earth_year_length
mars_age = since_birth / mars_year_length
ceres_age = since_birth / ceres_year_length
jupiter_age = since_birth / jupiter_year_length
saturn_age = since_birth / saturn_year_length
uranus_age = since_birth / uranus_year_length
neptune_age = since_birth / neptune_year_length
pluto_age = since_birth / pluto_year_length

mercury_month, mercury_day, mercury_year = next_birthday(mercury_age, mercury_year_length)
venus_month, venus_day, venus_year = next_birthday(venus_age, venus_year_length)
earth_year = next_birthday_earth(month, day)
mars_month, mars_day, mars_year = next_birthday(mars_age, mars_year_length)
ceres_month, ceres_day, ceres_year = next_birthday(ceres_age, ceres_year_length)
jupiter_month, jupiter_day, jupiter_year = next_birthday(jupiter_age, jupiter_year_length)
saturn_month, saturn_day, saturn_year = next_birthday(saturn_age, saturn_year_length)
uranus_month, uranus_day, uranus_year = next_birthday(uranus_age, uranus_year_length)
neptune_month, neptune_day, neptune_year = next_birthday(neptune_age, neptune_year_length)
pluto_month, pluto_day, pluto_year = next_birthday(pluto_age, pluto_year_length)

mercury_half_month, mercury_half_day, mercury_half_year = next_half_birthday(mercury_age, mercury_year_length)
venus_half_month, venus_half_day, venus_half_year = next_half_birthday(venus_age, venus_year_length)
earth_half_month, earth_half_day, earth_half_year = next_half_birthday(earth_age, earth_year_length)
mars_half_month, mars_half_day, mars_half_year = next_half_birthday(mars_age, mars_year_length)
ceres_half_month, ceres_half_day, ceres_half_year = next_half_birthday(ceres_age, ceres_year_length)
jupiter_half_month, jupiter_half_day, jupiter_half_year = next_half_birthday(jupiter_age, jupiter_year_length)
saturn_half_month, saturn_half_day, saturn_half_year = next_half_birthday(saturn_age, saturn_year_length)
uranus_half_month, uranus_half_day, uranus_half_year = next_half_birthday(uranus_age, uranus_year_length)
neptune_half_month, neptune_half_day, neptune_half_year = next_half_birthday(neptune_age, neptune_year_length)
pluto_half_month, pluto_half_day, pluto_half_year = next_half_birthday(pluto_age, pluto_year_length)

# Weeks are defined here as the number of Earth days making up the equivalent fraction of the year
mercury_week = round(mercury_year_length / earth_weeks, 1)
venus_week = round(venus_year_length / earth_weeks, 1)
earth_week = round(earth_year_length / earth_weeks, 1)
mars_week = round(mars_year_length / earth_weeks, 1)
ceres_week = round(ceres_year_length / earth_weeks)
jupiter_week = round(jupiter_year_length / earth_weeks)
saturn_week = round(saturn_year_length / earth_weeks)
uranus_week = round(uranus_year_length / earth_weeks)
neptune_week = round(neptune_year_length / earth_weeks)
pluto_week = round(pluto_year_length / earth_weeks)

print('\n')
print('{0:35s} {1:10s} {2:10s} {3:10s} {4:10s} {5:10s} {6:10s} {7:10s} {8:10s} {9:10s} {10:10s}'.format('World:',
                                                                    'Mercury', 'Venus', 'Earth', 'Mars', 'Ceres',
                                                                    'Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto'))

print('{0:35s} {1:10s} {2:10s} {3:10s} {4:10s} {5:10s} {6:10s} {7:10s} {8:10s} {9:10s} {10:10s}'.format('Year length (Earth days):',
                                                                        str(round(mercury_year_length, 4)), str(round(venus_year_length, 4)),
                                                                        str(round(earth_year_length, 4)), str(round(mars_year_length, 4)),
                                                                        str(round(ceres_year_length, 4)), str(round(jupiter_year_length, 4)),
                                                                        str(round(saturn_year_length, 4)), str(round(uranus_year_length, 4)),
                                                                        str(round(neptune_year_length, 4)), str(round(pluto_year_length, 4))))

print('{0:35s} {1:10s} {2:10s} {3:10s} {4:10s} {5:10s} {6:10s} {7:10s} {8:10s} {9:10s} {10:10s}'.format('Current age (local years):',
                                                                        str(round(mercury_age, 4)), str(round(venus_age, 4)),
                                                                        str(round(earth_age, 4)), str(round(mars_age, 4)),
                                                                        str(round(ceres_age, 4)), str(round(jupiter_age, 4)),
                                                                        str(round(saturn_age, 4)), str(round(uranus_age, 4)),
                                                                        str(round(neptune_age, 4)), str(round(pluto_age, 4))))

print('{0:35s} {1:10s} {2:10s} {3:10s} {4:10s} {5:10s} {6:10s} {7:10s} {8:10s} {9:10s} {10:10s}'.format('Next birthday:',
                                       str(mercury_month) + '/' + str(mercury_day) + '/' + str(mercury_year),
                                       str(venus_month) + '/' + str(venus_day) + '/' + str(venus_year),
                                       str(month) + '/' + str(day) + '/' + str(earth_year),
                                       str(mars_month) + '/' + str(mars_day) + '/' + str(mars_year),
                                       str(ceres_month) + '/' + str(ceres_day) + '/' + str(ceres_year),
                                       str(jupiter_month) + '/' + str(jupiter_day) + '/' + str(jupiter_year),
                                       str(saturn_month) + '/' + str(saturn_day) + '/' + str(saturn_year),
                                       str(uranus_month) + '/' + str(uranus_day) + '/' + str(uranus_year),
                                       str(neptune_month) + '/' + str(neptune_day) + '/' + str(neptune_year),
                                       str(pluto_month) + '/' + str(pluto_day) + '/' + str(pluto_year)))

print('{0:35s} {1:10s} {2:10s} {3:10s} {4:10s} {5:10s} {6:10s} {7:10s} {8:10s} {9:10s} {10:10s}'.format('Next half-birthday:',
                                       str(mercury_half_month) + '/' + str(mercury_half_day) + '/' + str(mercury_half_year),
                                       str(venus_half_month) + '/' + str(venus_half_day) + '/' + str(venus_half_year),
                                       str(earth_half_month) + '/' + str(earth_half_day) + '/' + str(earth_half_year),
                                       str(mars_half_month) + '/' + str(mars_half_day) + '/' + str(mars_half_year),
                                       str(ceres_half_month) + '/' + str(ceres_half_day) + '/' + str(ceres_half_year),
                                       str(jupiter_half_month) + '/' + str(jupiter_half_day) + '/' + str(jupiter_half_year),
                                       str(saturn_half_month) + '/' + str(saturn_half_day) + '/' + str(saturn_half_year),
                                       str(uranus_half_month) + '/' + str(uranus_half_day) + '/' + str(uranus_half_year),
                                       str(neptune_half_month) + '/' + str(neptune_half_day) + '/' + str(neptune_half_year),
                                       str(pluto_half_month) + '/' + str(pluto_half_day) + '/' + str(pluto_half_year)))

print('{0:35s} {1:10s} {2:10s} {3:10s} {4:10s} {5:10s} {6:10s} {7:10s} {8:10s} {9:10s} {10:10s}'.format('Length of birthweek (Earth days):',
                                                                        str(mercury_week), str(venus_week),
                                                                        str(earth_week), str(mars_week),
                                                                        str(ceres_week), str(jupiter_week),
                                                                        str(saturn_week), str(uranus_week),
                                                                        str(neptune_week), str(pluto_week)))
