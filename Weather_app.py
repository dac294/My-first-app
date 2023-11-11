from IPython.display import Image, display
import pgeocode
from pgeocode import Nominatim
import os
import requests
import json
from dotenv import load_dotenv
from app.email_service import send_email


load_dotenv()

def get_data():
	DEGREE_SIGN = u"\N{DEGREE SIGN}"

	zip_code = input("Please input a zip code (e.g. '06510'): ") or "06510"
	nomi = Nominatim('US')
	geo = nomi.query_postal_code(zip_code)
	print("LOCATION INFO:")
	print(geo)
	latitude = geo["latitude"]
	longitude = geo["longitude"]

	request_url = f"https://api.weather.gov/points/{latitude},{longitude}"
	print(request_url)
	response = requests.get(request_url)
	parsed_response = json.loads(response.text)
	print(response.status_code)
	forecast_url = parsed_response["properties"]["forecast"]
	print(forecast_url)
	forecast_response = requests.get(forecast_url)
	parsed_forecast_response = json.loads(forecast_response.text)

	periods = parsed_forecast_response["properties"]["periods"]

	daytime_periods = [period for period in periods if period["isDaytime"] == True]
	print(daytime_periods)
	for period in daytime_periods:
	    #print(period.keys())
	    print("-------------")
	    print(period["name"], period["startTime"][0:7])
	    print(period["shortForecast"], f"{period['temperature']} {DEGREE_SIGN}{period['temperatureUnit']}")
	    #print(period["detailedForecast"])
	    display(Image(url=period["icon"]))




if __name__ == "__main__":
    data = get_data()

    user_address = input("please enter your email address: ")

    content = f"""
    <h1> Weather Report Email </h1>

    <p> {data} </p>
    """

    send_email(recipient_address=user_address,html_content=content,subject="Weather Report")