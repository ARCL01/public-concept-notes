from waitress import serve
from public import app

if __name__ == "__main__":
    print(f'Running PUBLIC app on port 8080!')
    serve(app,host='0.0.0.0', port=8080)