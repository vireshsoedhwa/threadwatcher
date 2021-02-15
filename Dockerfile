FROM python:3.9.0-slim
ENV PYTHONUNBUFFERED 1
# ENV VIRTUAL_ENV=/opt/venv
WORKDIR /code

# RUN python3 -m venv $VIRTUAL_ENV
# ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apt-get update &&  \
    apt-get upgrade -y && \
    apt-get install ffmpeg -y && \
    apt-get autoremove --purge && \
    apt-get -y clean

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN echo "America/Vancouver" > /etc/timezone
# RUN export TZ=America/Vancouver
RUN dpkg-reconfigure -f noninteractive tzdata

COPY v1 .
COPY threadwatcher .
COPY manage.py .
COPY docker-entrypoint.sh .

# EXPOSE 9000
RUN chmod +x ./docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:9000"]
