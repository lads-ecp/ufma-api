FROM python:3.7-alpine
COPY . /web
WORKDIR /web/scripts
RUN pip install -r ./requirements.txt
RUN python script.py
WORKDIR /web/api
RUN pip install -r ./requirements.txt
RUN adduser -D myuser
USER myuser
ENTRYPOINT ["python"]
CMD ["app.py"]