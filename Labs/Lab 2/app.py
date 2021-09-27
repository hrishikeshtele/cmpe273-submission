from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
from flasgger import Swagger
from flask import Flask, jsonify

from students.model import StudentSchema

spec = APISpec(
    title="SJSU Student Registration API",
    version="0.0.1",
    openapi_version="3.0.3",
    plugins=[
        FlaskPlugin(),
        MarshmallowPlugin()
    ],
)

app = Flask(__name__)
swagger = Swagger(app)


@app.route("/")
def index():
    return jsonify({"foo": "bar"})


@app.route("/spec")
def get_apispec():
    return jsonify(spec.to_dict())


@app.route("/students")
def get_students():
    """
    Get all SJSU students
    ---
    get:
        description: Get all students
        responses:
            200:
                content:
                    application/json:
                        schema: StudentSchema
    """
    student = dict(first_name="Michael", last_name="Scott",
                   sjsu_id="512", email="michael.scott@sjsu.edu")

    return StudentSchema().dump(student)


with app.test_request_context():
    spec.path(view=index)
    spec.path(view=get_students)
