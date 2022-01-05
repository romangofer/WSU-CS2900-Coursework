import csv
import matplotlib.pyplot as plt
from datetime import datetime

#with open("weatherfile.csv", 'r') as f:
with open("weatherfile6_14.csv", 'r') as f:
    reader = csv.reader(f)
    header_row = next(reader)
    print(header_row)
    highs = []
    dates = []
    lows = []
    for row in reader:
      try:
        #print(row)
        high = int(row[5])
        low = int(row[6])
        date = row[2]   
      except ValueError:
            print(f'Data missing for {date}')
      else:
            lows.append(low)
            #print(type(row[5]))
            highs.append(high)
            #dates.append(date)
            date_to_dt = datetime.strptime(date, '%Y-%m-%d')
            dates.append(date_to_dt)

    #print(highs)
    #print(dates)

    plt.style.use('seaborn')
    fig, ax = plt.subplots()
    #ax.plot(highs, c='red')
    ax.set_title("High Temperature Based on Day", fontsize = 24)
    ax.set_xlabel("Days of the Month", fontsize = 18)
    ax.set_ylabel('High Temps', fontsize = 18)
    ax.tick_params(axis = 'both', which = 'major', labelsize = 16)
    #plt.plot(highs)
    ax.plot(dates, highs, c='red')
    ax.plot(dates, lows, c='blue' )
    ax.fill_between(dates, highs, lows, facecolor = "blue", alpha = 0.1)
    fig.autofmt_xdate()
    plt.savefig("high-lows-sitka-2018.png", bbox_inches='tight')
    plt.show()
