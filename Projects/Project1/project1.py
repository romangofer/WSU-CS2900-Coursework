import csv
from datetime import datetime
import plotly.express as px

#Read the data in from the csv file
with open('data/nasdaq_historical_data_36_yr.csv') as f:
    reader = csv.reader(f)
    header_row = next(reader)

    # Create empty lists to get date numbers and their closing prices. Also, there's a list for the converted dates.
    dates = []
    closes = []
    converted_dates = []
    
    # For loop to get the date and closing values from the stock data file so they can be plotted
    for row in reader:
        date = row[0]
        closing = int(float(row[4])) # Convert string number in csv to integer for plotting
        dates.append(date) # Append dates to dates list
        closes.append(closing) # Append closing price numbers to closing list
    for date in dates:
        d_parsed = datetime.strptime(date, '%Y-%m-%d').strftime('%B %d, %Y') # Transform date
        converted_dates.append(d_parsed) # Add transformed date to new converted_dates list

# Make Plotly Express Area Chart to Plot Stock Data
area_chart = px.area(x = converted_dates, y = closes)
area_chart.update_xaxes(title_text = 'Date', showgrid = False, color = '#0000FF')
area_chart.update_yaxes(title_text = 'Closing Price', tickprefix = '$', showgrid = False)
area_chart.update_layout(showlegend = False)
area_chart.update_layout(
    title={
        'text': "NASDAQ Composite Historical Closing Price Data Each Month for the Past 36 Years",
        'y': 0.975,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'}, font = dict(color = '#0000FF'), plot_bgcolor = '#FFFDD0')
area_chart.update_traces(mode='markers+lines', line=dict(color='#FFA500', width=1))
area_chart.show()

