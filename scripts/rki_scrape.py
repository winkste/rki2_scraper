#!/usr/bin/python
'''This module supports reading the rki data sets'''
import datetime
import lastdata
import pprint
from paho.mqtt import publish
import my_secrets
import requests

RKI_API_STRING_FOR_CELLE = 'https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?where=OBJECTID%20%3E%3D%2034%20AND%20OBJECTID%20%3C%3D%2035&outFields=OBJECTID,GEN,BEZ,death_rate,cases,deaths,cases_per_100k,cases_per_population,last_update,cases7_per_100k,recovered,cases7_bl_per_100k,cases7_bl,death7_bl,cases7_lk,death7_lk,cases7_per_100k_txt,AdmUnitId&outSR=4326&f=json'
RKI_API_STRING_FOR_NOH   = 'https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?where=OBJECTID%20%3E%3D%2055%20AND%20OBJECTID%20%3C%3D%2056&outFields=OBJECTID,GEN,BEZ,death_rate,cases,deaths,cases_per_100k,cases_per_population,last_update,cases7_per_100k,recovered,cases7_bl_per_100k,cases7_bl,death7_bl,cases7_lk,death7_lk,cases7_per_100k_txt,AdmUnitId&outSR=4326&f=json'

def request_rki_data(dataset, api_link):
    '''This function read the RKI dataset based on a API link definition'''
    res = requests.get(api_link).json()
    features = res.get('features')
    feat = features[0]
    attrib = feat.get('attributes')
    date_key = attrib.get('last_update')
    dataset[date_key] = attrib
    return date_key

def publish_data(topic, payload):
    '''This function publishes data to the mqtt broker'''
    publish.single(topic, payload, hostname=my_secrets.hostname,
                    port=my_secrets.port, client_id=my_secrets.client_id,
                    auth=my_secrets.auth)

def main():
    '''This is the module main function '''
    # read and print the actual time / date information to the command line
    now = datetime.datetime.now()
    print("*******************************************************************")
    print("*** RKI SCRAPER ***************************************************")
    actual_time = now.strftime("%Y-%m-%d %H:%M:%S")
    print(f"Actual Time/Date of call: {actual_time}")
    #print("Actual Time/Date of call: %s"%(now.strftime("%Y-%m-%d %H:%M:%S")))
    print("*******************************************************************")

    # read RKI data from RKI page
    celle = {}
    noh   = {}
    date_key = request_rki_data(celle, RKI_API_STRING_FOR_CELLE)
    request_rki_data(noh, RKI_API_STRING_FOR_NOH)

    # process RKI data to get 7 day incident value
    celle_actual_inc = round(celle[date_key]['cases7_per_100k'], 2)
    noh_actual_inc = round(noh[date_key]['cases7_per_100k'], 2)

    if celle_actual_inc > lastdata.celle_last_inc:
        celle_7inc_trend = "^"
    elif celle_actual_inc < lastdata.celle_last_inc:
        celle_7inc_trend = "v"
    else:
        celle_7inc_trend = "-"

    # update RKI history buffer with new value
    file = open('lastdata.py', 'w')
    file.write('celle_last_inc =' + pprint.pformat(celle_actual_inc))
    file.write('\n')
    file.write('noh_last_inc =' + pprint.pformat(noh_actual_inc))
    file.close()

    # publish RKI data to MQTT
    topic = "std/dev200/s/rki/ce/c7"
    #publish_data(topic, str(celle_actual_inc))
    topic = "std/dev200/s/rki/ce/c7_t"
    #publish_data(topic, celle_7inc_trend)
    topic = "std/dev200/s/rki/noh/c7"
    #publish_data(topic, str(noh_actual_inc))
    topic = "std/dev200/s/rki/noh/c7_t"
    #publish_data(topic, noh_7inc_trend)



if __name__ == "__main__":
    main()
