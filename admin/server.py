from waitress import serve
from admin import app

if __name__ == "__main__":
    print(f'Running ADMIN app on port 9090!')
    serve(app,host='0.0.0.0', port=9090)