FROM python:3.6-stretch
WORKDIR /app
ENV TOKEN=""
CMD ["cd", "/app"]
RUN pip install bs4 discord
CMD ["sh", "-c", "python3 patchbot.py $TOKEN"]
