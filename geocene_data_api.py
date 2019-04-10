#/usr/bin/python3
# -*- coding: utf-8 -*-

#Import libraries
import json
import requests
import time
from tempfile import NamedTemporaryFile
import tempfile 
import shutil
import urllib
import zipfile
import os
from sqlalchemy import create_engine
import pandas as pd


###########
# Functions
def get_update(url_request,id_request,token_headers):

    get_request_id = url_request + str(id_request)
    result = requests.get(get_request_id,headers = token_headers)
    update = result.json()

    if update['progress'] is None:
         update['progress'] = 0
            
    return (update)

def wait_for_export(url_request,id_request,token_headers):
    progress = 0
    while progress <100:
        update_var = get_update(url_request,id_request,token_headers)
        if update_var['status'] == "error":
            print("error processing export")
            return ()

        progress = update_var['progress']
        print(str(progress) + "% of data export completed")

        if(progress<100):
            time.sleep(3)
            
def get_url(url_request,id_request,token_headers):
        
    while (requests.get(url_request + str(id_request) + "/", headers = token_headers)).json()['download_url'] is None:
        time.sleep(1)

    download_url_var = (requests.get(url_request + str(id_request) + "/", headers = token_headers)).json()['download_url']

    return(download_url_var)



def geocene_get_data(filter_date_var):
	#########
	# Make the request

	#filter_date = "2019-02-05T00:00:00Z"
	filter_date = filter_date_var

	r = (requests.post(api_token_auth_url, data= PARAMS, headers = post_headers)).json()

	# Get Key
	token = r['token']
	token_header = 'Token ' + token
	token_headers = {'Authorization':token_header,'content-type': 'application/json'}

	# Secure request
	export_request_body = '{"after":"' + filter_date + '"}'
	id_request = ((requests.post(data_export_request_url, data= PARAMS, headers = token_headers)).json())['id']
	url_path = get_url(data_export_request_url,id_request,token_headers)

	# Wait for request
	wait_for_export

	# Create a local temporary file to call the url, unzip data and read
	temp_dir = tempfile.TemporaryDirectory()

	empty_zip_data = b'PK\x05\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

	zip_path = temp_dir.name + '/this_zip.zip'
	with open(zip_path, 'wb') as zip:
	    zip.write(empty_zip_data)

	#Get Data
	urllib.request.urlretrieve(url_path, zip_path)

	#Extract Data
	zipzip = zipfile.ZipFile(zip_path,'r')
	zipzip.extractall(temp_dir.name)
	zipzip.close()


	#########
	# Read into postgres
	# 1. Create tables for all households first in database
	# In POSTGRES DATABASE
	# CREATE DATABASE sonora_sensors;
	# GRANT ALL PRIVILEGES ON DATABASE sonora_sensors TO diego;

	# CREATE TABLE taqueria (
	#  index bigint,
	#  created_at timestamp,
	#  timestamp timestamp,
	#  value double precision,
	#  sensor_type_id text,
	#  channel bigint,
	#  sensor_id text,
	#  house_name text);


	# 2. Write to database and table

	list_files = os.listdir(temp_dir.name)

	#Creating a data frame for each house
	house_list = list(house_sensors.keys())
	house_df_list = []
	            
	for house in house_list:
	    
	    list_dfs = []
	    sensor_list = house_sensors[house]
	    for file in list_files:
	     
	        for sensor_id in range(0,len(sensor_list)):
	            
	            if file[-8:] == (house_sensors[house][sensor_id] + ".csv"):
	                
	                path = temp_dir.name + "/" + file
	                this_df = pd.read_csv(path)
	                this_df['sensor_id'] = str((file[-8:]).replace(".csv",""))
	                list_dfs.append(this_df)
	     
	    #Appending the house together
	    appended_data = pd.concat(list_dfs, axis=0)
	    appended_data['house_name'] = house

	    #Adding 
	    house_df_list.append(appended_data)


	# Add table to psql table
	engine = create_engine('postgresql://diego:password@localhost:5432/sonora_sensors')
	appended_data.to_sql('taqueria', engine, if_exists='append')

	return(print("Data loaded!"))


######
# Houses in Study Dict

house_sensors = {}
house_sensors['taqueria']= ("07A3","F335","25A4")

    
#####
# Define API URLs
base_url = 'https://collect.geocene.com/'
data_export_request_url = base_url +  'data_export_request/'
api_token_auth_url = base_url + 'api-token-auth/'
PARAMS = '{"username":"diegoleonbarido","password":"stistutorapa"}'
post_headers = {'content-type': 'application/json'}


##### Set as function and run
if __name__ == "__main__":

	filter_date_var = "2019-02-05T00:00:00Z"
	geocene_get_data(filter_date_var)






    
