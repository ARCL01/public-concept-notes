FROM python:3

WORKDIR /usr/src/app

COPY ../requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app and server
COPY public/public.py public/server.py ./

COPY shared/static ./static
COPY shared/templates ./templates

CMD [ "python", "./server.py" ]