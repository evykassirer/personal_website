months = ['January','February','March','April','May','June','July','August','September', 'October','November','December']
month_abbvs = dict((m[:3].lower(), m) for m in months)

def valid_month(month):
    if month:
        short_month = month[:3].lower()
    return month_abbvs.get(short_month)


def valid_day(day):
    if day.isdigit():
        iday = int(day)
        if iday >= 1 and iday <= 31: 
            return iday

def valid_year(year):
    if year and year.isdigit():
        if int(year) >= 1900 and int(year) <= 2020:
            return int(year)
