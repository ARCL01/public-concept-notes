from waitress import serve
import threading
from public import app as public
from admin import app as admin

def run_public():
    print(f'Running PUBLIC app on port 8080!')
    serve(public,host='0.0.0.0', port=8080)


def run_admin():
    print(f'Running ADMIN app on port 9090!')
    serve(admin,host='0.0.0.0', port=9090)


if __name__ == "__main__":
    print(f'Serving apps...')
    threading.Thread(target=run_admin).start()
    threading.Thread(target=run_public).start() 