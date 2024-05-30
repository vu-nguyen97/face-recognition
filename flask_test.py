from flask_test import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

# https://stackoverflow.com/questions/67997606/how-can-i-run-flask-in-windows
# app.run(host='127.0.0.1',port=8000,debug=True)

# Not working
# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=5000, debug=True)

# if __name__ == '__main__':
#    app.run()