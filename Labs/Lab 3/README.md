# Lab 3

## Pre-requisites

* Install _Pipenv_

```
pip install pipenv
```

* Install _[Flask](https://palletsprojects.com/p/flask/)_

```
pipenv install flask==1.1.1
```
* Install _[Ariadne](https://ariadnegraphql.org/docs/flask-integration.html)_ for handling GraphQL schema and binding.

```
pipenv install ariadne==0.10.0
```

* Run the application from a shell/terminal.

```sh
$ pipenv shell
$ pipenv run flask run
```

* Open [this URL](http://127.0.0.1:5000/) in a web browser or run this CLI to see the output.

```
curl -i http://127.0.0.1:5000/
```

## Requirements

You will be building a RESTful GraphQL server class registration API in this lab.

### Domain Model

```
|-------|               |---------|
| Class |* ---------- * | Student |
|-------|               |---------|
```

### GraphQL operations to be implemented.

* Mutate a new student

```
mutation Student {
  create_student(name: "HT", email: "ht@gmail.com") {
    success
    errors
    students{
      id
      name
      email
    }
  }
}
```

_Response_

```
{
  "data": {
    "create_student": {
      "errors": [],
      "students": [
        {
          "email": "ht@gmail.com",
          "id": 1,
          "name": "HT"
        }
      ],
      "success": true
    }
  }
}
```

* Query an existing student

_Request_

```
query getStudentById{
  student(id:1) {
    name
  }
}
```

_Response_

```
{
  "data": {
    "student": {
      "name": "HT"
    }
  }
}
```

* Mutate a class

```
mutation Class {
  create_class(name: "273", student_ids: [1]) {
    success
    errors
    classes {
        id
        name
      
    }
  }
}
```

* Query a class

```
query getClassesById{
  classes(id:1) {
    name
    students {
      name
    }
  }
}
```

_Response_

```
{
  "data": {
    "classes": {
      "name": "273",
      "students": [
        {
          "name": "HT"
        }
      ]
    }
  }
}
```

* Add students to a class

```
mutation {
  add_student_to_class(id: 2,student_id: 1) {
    success
    errors
    class {
      id
      name
    }
  }
}
```

_Response_

```
{
  "data": {
    "add_student_to_class": {
      "class": {
        "id": 2,
        "name": "273"
      },
      "errors": [],
      "success": true
    }
  }
}
```