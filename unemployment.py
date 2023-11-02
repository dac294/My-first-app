from getpass import getpass
import requests
import json
from pprint import pprint
from statistics import mean
from plotly.express import line
from operator import itemgetter
import matplotlib.pyplot as plt


API_KEY = getpass("Please input your AlphaVantage API Key: ")



request_url = f"https://www.alphavantage.co/query?function=UNEMPLOYMENT&apikey={API_KEY}"

response = requests.get(request_url)

parsed_response = json.loads(response.text)
print(type(parsed_response))
print(parsed_response.keys())
#pprint(parsed_response)

data = parsed_response["data"]

# Challenge A
#
# What is the most recent unemployment rate? And the corresponding date?
# Display the unemployment rate using a percent sign.

print("-------------------------")
print("LATEST UNEMPLOYMENT RATE:")
#print(data[0])
print(f"{data[0]['value']}%", "as of", data[0]["date"])


# Challenge B
#
# What is the average unemployment rate for all months during this calendar year?
# ... How many months does this cover?



this_year = [d for d in data if "2023-" in d["date"]]

rates_this_year = [float(d["value"]) for d in this_year]
#print(rates_this_year)

print("-------------------------")
print("AVG UNEMPLOYMENT THIS YEAR:", f"{round(mean(rates_this_year), 2)}%")
print("NO MONTHS:", len(this_year))


# Challenge C
#
# Plot a line chart of unemployment rates over time.



dates = [d["date"] for d in data]
rates = [float(d["value"]) for d in data]

fig = line(x=dates, y=rates, title="United States Unemployment Rate over time", labels= {"x": "Month", "y": "Unemployment Rate"})
fig.show()



sorted_data = sorted(data, key=(itemgetter("date"))) # sort first, then split
sorted_dates = [d["date"] for d in sorted_data]
sorted_rates = [float(d["value"]) for d in sorted_data]

plt.figure(figsize=(10, 6))  # Set the figure size
plt.plot(sorted_dates, sorted_rates, marker='o', linestyle='-', color='b', label="Unemployment Rate")
plt.title("United States Unemployment Rate over time")
plt.xlabel("Month")
plt.ylabel("Unemployment Rate")
plt.grid(True)
plt.show()

#def format_pct(my_number:float) -> str:

def format_pct(my_number):
    """
        Formats a percentage number like 3.6555554 as percent, rounded to two decimal places.

        Param my_number (float) like 3.6555554

        Returns (str) like '3.66%'
    """
    return f"{my_number:.2f}%"


print(format_pct(3.65554))

print(format_pct(25.4))

result = format_pct(25.4)
print(result)


assert format_pct(3.65554) == '3.66%'
assert format_pct(25.4) == '25.40%'

result = format_pct(25.4)
assert result == '25.40%'

