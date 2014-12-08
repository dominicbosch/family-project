import datetime
Jan1st = datetime.date(2010,1,1)
Year,WeekNum,DOW = Jan1st.isocalendar() # DOW = day of week
print(Year,WeekNum,DOW)
