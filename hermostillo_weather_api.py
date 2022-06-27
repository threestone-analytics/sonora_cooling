#/usr/bin/python3
# -*- coding: utf-8 -*-

#Import libraries
import pyowm
import pandas as pd
from time import sleep
from sqlalchemy import create_engine
from datetime import datetime
from pytz import timezone



#Make the request
def get_weather_data():
    weather_datadf_list = []
    
    for i in range(0,13): #Loops
        
        # CAll
        owm = pyowm.OWM('4924239659ffd4f536f72b1beed83650')
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place('Hermosillo,MX')
        weather = observation.weather

        #Get Vars
        utc_timestamp = datetime.now(timezone('UTC'))
        sonora_timestamp = datetime.now(timezone('America/Hermosillo'))
        temperature = weather.temperature('celsius')['temp']
        temperature_max = weather.temperature('celsius')['temp_max']
        temperature_min = weather.temperature('celsius')['temp_min']
        temperature_feelslike = weather.temperature('celsius')['feels_like']
        sunrise_time = weather.sunrise_time(timeformat='date') #UTC time
        sunset_time = weather.sunset_time(timeformat='date') #UTC time

        # Store
        weather_dic = {
            "utc_timestamp":[utc_timestamp],
            "sonora_timestamp":[sonora_timestamp],
            "temperature":[temperature],
            "temperature_max":[temperature_max],
            "temperature_min":[temperature_min],
            "temperature_feelslike":[temperature_feelslike],
            "sunrise_time":[sunrise_time],
            "sunset_time":[sunset_time]
        }

        # create a list of strings
        columns = ['utc_timestamp','sonora_timestamp','temperature','temperature_max','temperature_min','temperature_feelslike','sunrise_time','sunset_time']

        df = pd.DataFrame(weather_dic, columns=columns)
        weather_datadf_list.append(df)
        #sleep(300) # Seconds

    df_weather = pd.concat(weather_datadf_list,axis=0)
    	# CREATE TABLE hermosillo_weather (
    	#  index text,
    	#  utc_timestamp TIMESTAMPTZ,
    	#  sonora_timestamp timestamp,
    	#  temperature double precision,
    	#  temperature_max double precision,
    	#  temperature_min double precision,
    	#  temperature_feelslike double precision,
    	#  sunrise_time timestamp without time zone,
    	#  sunset_time timestamp without time zone
     #    	);
        
    # Add table to psql table
    df_weather = pd.concat(weather_datadf_list,axis=0)
    engine = create_engine('postgresql://diego:password@localhost:5432/sonora_sensors')
    df_weather.to_sql('hermosillo_weather', engine, if_exists='append')
    return(print("Weather updated!"))

##### Set as function and run
if __name__ == "__main__":

	get_weather_data()



    
