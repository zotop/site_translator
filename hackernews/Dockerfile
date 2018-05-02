FROM python:3.6.5
ADD . /hackernews_client
WORKDIR /hackernews_client
EXPOSE 5000
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "hackernews/app.py"]
CMD ["echo", "Hackernews Client App"]
