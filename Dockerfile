FROM myflask
WORKDIR /web/api
#RUN python loadingdb.py
#RUN adduser -D myuser
#USER myuser
ENTRYPOINT ["python"]
CMD ["app.py"]