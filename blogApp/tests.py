
# import required modules
import requests, json
 
# Enter your API key here
api_key = "af78b062b7068b1667494cc118fcd076"
 
# base_url variable to store url
base_url = "http://api.openweathermap.org/data/2.5/weather?"
 
# Give city name
city_name = 'seoul'
 
# complete_url variable to store
# complete url address
complete_url = base_url + "appid=" + api_key + "&q=" + city_name
 
# get method of requests module
# return response object
response = requests.get(complete_url)
 
# json method of response object
# convert json format data into
# python format data
list_of_data = response.json()
 
data = {
    "country_code": str(list_of_data['sys']['country']),
    "coordinate": str(list_of_data['coord']['lon']) + ' '
                + str(list_of_data['coord']['lat']),
    "temp": str(list_of_data['main']['temp']) + 'k',
    "feel_temp": str(list_of_data['main']['feels_like']) + 'k',
    "cloud": str(list_of_data['clouds']['all']),
    "humidity": str(list_of_data['main']['humidity']) + '%',
    "description": str(list_of_data['weather'][0]['description'])
    }
print(data)

 
