FROM python:3

WORKDIR /usr/src/app

COPY ../requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir ./notes

# Copy app and server
COPY admin/admin.py admin/server.py ./

# Copy resources
COPY shared/static ./static
COPY shared/templates ./templates
COPY admin/schema.sql ./

CMD [ "python", "./server.py" ]