FROM python:3

WORKDIR /usr/src/app

COPY ../requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir ./notes

# Copy app and server
COPY admin.py admin/server.py ./

# Copy resources
COPY static ./static
COPY templates ./templates
COPY schema.sql ./

CMD [ "python", "./server.py" ]