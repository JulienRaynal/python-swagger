from flask import Flask
from blueprints import blueprint

app = Flask(__name__)
app.config['RESTPLUS_MASK_SWAGGER'] = False

app.register_blueprint(blueprint)


@app.route("/")
def hello_world():
    return "<p>Hello world</p>"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
