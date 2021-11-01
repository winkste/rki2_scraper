# rki2_scraper
RKI data reader running in a docker container using crone

## run static code analysis
pylint scripts/rki_scrape.py

## run program with virtual environment as stand alone
python3 -m venv venv_rki_scrape_3_8_10
source venv_rki_scrape_3_8_10/bin/activate .
pip install -r requirements.txt
python scripts/rki_scrape.py 
deactivate

## generate and run/stop the docker container including the cron job
docker build -t docker-rki_scraper .
docker run -it --name docker-rki_scraper docker-rki_scraper
docker ps
docker stop docker-rki_scraper
docker rm docker-rki_scraper