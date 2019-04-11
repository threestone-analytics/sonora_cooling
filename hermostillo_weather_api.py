#/usr/bin/python3
# -*- coding: utf-8 -*-

#Import libraries
import pyowm
import pandas as pd
from time import sleep
from sqlalchemy import create_engine
import datetime


#Make the request

def get_weather_data():
	weather_datadf_list = []

	for i in range(0,5): #Minutes
	    
	    #Call
	    owm = pyowm.OWM('4924239659ffd4f536f72b1beed83650')
	    observation = owm.weather_at_place('Hermosillo,MX')
	    w = observation.get_weather()
	    
	    #Get Vars
	    local_timestamp = datetime.datetime.now()
	    obs_timestamp = w.get_reference_time(timeformat='date')
	    wind_speed = w.get_wind()['speed'] 
	    humidity = w.get_humidity()  
	    temperature = w.get_temperature('celsius')['temp']
	    temperature_max = w.get_temperature('celsius')['temp_max']
	    temperature_min = w.get_temperature('celsius')['temp_min']
	    sunrise_time = w.get_sunset_time('iso') 
	    sunset_time = w.get_sunset_time('iso') 
	    
	    # Store
	    weather_dic = {
	        "local_timestamp":[local_timestamp],
	        "obs_timestamp":[obs_timestamp],
	        "wind_speed":[wind_speed],
	        "humidity":[humidity],
	        "temperature":[temperature],
	        "temperature_max":[temperature_max],
	        "temperature_min":[temperature_min],
	        "sunrise_time":[sunrise_time],
	        "sunset_time":[sunset_time]
	    }
	    
	    # create a list of strings
	    columns = ['local_timestamp','obs_timestamp', 'wind_speed','humidity','temperature','temperature_max','temperature_min','sunrise_time','sunset_time']
	    #index = ['1', '2', '3','4','5','6','7','8','9']
	    
	    df = pd.DataFrame(weather_dic, columns=columns)
	    
	    weather_datadf_list.append(df)
	    # print(str(local_timestamp))
	    # print(obs_timestamp)
	    sleep(5) # Seconds


	# Create Data Frame
	df_weather = pd.concat(weather_datadf_list,axis=0)

	# CREATE TABLE hermosillo_weather (
	#  index text,
	#  local_timestamp timestamp without time zone,
	#  obs_timestamp timestamp without time zone,
	#  wind_speed double precision,
	#  humidity bigint,
	#  temperature double precision,
	#  temperature_max double precision,
	#  temperature_min double precision,
	#  sunrise_time timestamp without time zone,
	#  sunset_time timestamp without time zone
	# );

	# Add table to psql table
	engine = create_engine('postgresql://diego:password@localhost:5432/sonora_sensors')
	df_weather.to_sql('hermosillo_weather', engine, if_exists='append')

	return(print("Weather updated!"))

##### Set as function and run
if __name__ == "__main__":

	get_weather_data()



    
