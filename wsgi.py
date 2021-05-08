import json

from flasgger import Swagger

from employee_management import app

with open('configs/app_config.json', 'r') as f:
    template = json.load(f)
with open('configs/swagger_config.json', 'r') as f:
    swagger_config = json.load(f)

if __name__ == "__main__":
    swagger = Swagger(app, template=template, config=swagger_config)
    app.run('0.0.0.0', debug=True)
