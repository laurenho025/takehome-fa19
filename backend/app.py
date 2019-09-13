from typing import Tuple

from flask import Flask, jsonify, request, Response
import mockdb.mockdb_interface as db

app = Flask(__name__)


def create_response(
    data: dict = None, status: int = 200, message: str = ""
) -> Tuple[Response, int]:
    """Wraps response in a consistent format throughout the API.
    
    Format inspired by https://medium.com/@shazow/how-i-design-json-api-responses-71900f00f2db
    Modifications included:
    - make success a boolean since there's only 2 values
    - make message a single string since we will only use one message per response
    IMPORTANT: data must be a dictionary where:
    - the key is the name of the type of data
    - the value is the data itself

    :param data <str> optional data
    :param status <int> optional status code, defaults to 200
    :param message <str> optional message
    :returns tuple of Flask Response and int, which is what flask expects for a response
    """
    if type(data) is not dict and data is not None:
        raise TypeError("Data should be a dictionary 😞")

    response = {
        "code": status,
        "success": 200 <= status < 300,
        "message": message,
        "result": data,
    }
    return jsonify(response), status


"""
~~~~~~~~~~~~ API ~~~~~~~~~~~~
"""


@app.route("/")
def hello_world():
    return create_response({"content": "hello world!"})


@app.route("/mirror/<name>")
def mirror(name):
    data = {"name": name}
    return create_response(data)

@app.route("/contacts", methods=['GET'])
def get_all_contacts():
    # If a hobby is provided, return contacts with that hobby, otherwise return all contacts
    # If no such contacts exist, return a 404 with a message
    if 'hobby' in request.args:
        target_hobby = request.args.get('hobby')
        contacts_with_hobby = []
        for x in db.get('contacts'):
            if x['hobby'] == target_hobby:
                contacts_with_hobby.append(x)
        if len(contacts_with_hobby) == 0:
            return create_response(status=404, message="No contact with this hobby exists")
        return create_response({"contacts": contacts_with_hobby})
    else:
        return create_response({"contacts": db.get('contacts')})

@app.route("/contacts/<id>", methods=['DELETE'])
def delete_show(id):
    if db.getById('contacts', int(id)) is None:
        return create_response(status=404, message="No contact with this id exists")
    db.deleteById('contacts', int(id))
    return create_response(message="Contact deleted")


# TODO: Implement the rest of the API here!

@app.route("/contacts/<id>", methods=['GET'])
def get_contact(id):
    if db.getById('contacts', int(id)) is None:
        return create_response(status=404, message="No contact with this id exists")
    return create_response(db.getById('contacts', int(id)))

@app.route("/contacts", methods=['POST'])
def add_contact():
    name = request.get_json()['name']
    nickname = request.get_json()['nickname']
    hobby = request.get_json()['hobby']

    # Check that all three parameters are provided/not empty strings
    if name == "" or nickname == "" or hobby == "":
        return create_response(status=422, message="Provide the contact's name, nickname, and hobby that you want to create")

    data = {"name": name, "nickname": nickname, "hobby": hobby} 
    return create_response(db.create('contacts', data), status=201)
    
"""
~~~~~~~~~~~~ END API ~~~~~~~~~~~~
"""
if __name__ == "__main__":
    app.run(port=8080, debug=True)
