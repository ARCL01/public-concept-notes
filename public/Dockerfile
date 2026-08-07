FROM python:3

WORKDIR /usr/src/app

COPY ../requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app and server
COPY public.py public/server.py ./

COPY static ./static
COPY templates ./templates

CMD [ "python", "./server.py" ]