from flask import Flask
from routes import register_routes

app = Flask(__name__)

@app.route('/')
def home():
    return 'Welcome to Leave Type API'


register_routes(app)


#Run the app
if __name__ == '__main__':
    app.run(debug=True)