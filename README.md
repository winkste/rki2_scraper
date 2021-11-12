# RKI DATA SCRAPER V2
RKI data reader running in a docker container using crone

## Introduction
The theory of concept of this python program is to connect to the RKI web page API to readout for one particular country the actual COVID-19 statistics. Currently this is done exemplary for two contries I'm interested in: Celle, Nordhorn.
The data is distributed to the MQTT broker. The last data set is stored to calculate a trend from last day (rising, stable, falling).

<img width="382" alt="Bildschirmfoto 2021-04-22 um 05 58 14" src="https://user-images.githubusercontent.com/9803344/115653866-449f9980-a330-11eb-8991-7aa8b52b673f.png">

Please note: This version of the RKI scraper is reduced to a minimum and is targeted to run on a Synology NAS in a docker container.


## Setup & Preparation
You can run the python project for test directly on the development machine, therefore a virtual environment including pylint is available.

### run static code analysis
```
pylint scripts/rki_scrape.py
```

### run program with virtual environment as stand alone
```
python3 -m venv venv_rki_scrape_3_8_10
source venv_rki_scrape_3_8_10/bin/activate .
pip install -r requirements.txt
python scripts/rki_scrape.py
deactivate
```

## generate and run/stop the docker container including the cron job
```
docker build -t docker-rki_scraper .
docker run -it --name docker-rki_scraper docker-rki_scraper
docker ps
docker stop docker-rki_scraper
docker rm docker-rki_scraper
docker save -o docker-rki.tar docker-rki
```
### Identify another country
Under /resources there is an example export from the RKI database stored. This example include all countries and with this the country number needed to modify the api request. use this file to identify the correct country.
```
Example:
Celle has the Object ID 34, this leads to a api request with the following entry:
https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?where=OBJECTID%20%3E%3D%2034%20AND%20OBJECTID%20%3C%3D%2034&outFields=OBJECTID,GEN,BEZ,death_rate,cases,deaths,cases_per_100k,cases_per_population,last_update,cases7_per_100k,recovered,cases7_bl_per_100k,cases7_bl,death7_bl,cases7_lk,death7_lk,cases7_per_100k_txt,AdmUnitId&outSR=4326&f=json

find the 34 in the api request above.

```
