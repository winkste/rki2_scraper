FROM python:3.11.0a1-alpine3.14
COPY requirements.txt ./
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
COPY /scripts/rki_scrape.py /bin/rki_scrape.py
COPY /scripts/my_secrets.py /bin/my_secrets.py
COPY /scripts/lastdata.py /bin/lastdata.py
COPY root /var/spool/cron/crontabs/root
RUN chmod +x /bin/rki_scrape.py
CMD crond -l 2 -f
