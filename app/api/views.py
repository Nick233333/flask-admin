from flask import jsonify, json, request
from . import api


@api.route("/jsonify/", methods=["GET", "POST"])
def test1():
    name = request.args.get("name")
    num = request.values.get("num")
    # age = request.form['age']
    # age = request.form.get('age', default='adasd')
    age = request.form.get("age", type=str, default='age')
    print(request.get_data())
    print(request.get_json())
    print(request.data)
    return jsonify({'code': 200, 'msg': 'success', 'data': {'user': {'name' : name, 'num': num, 'age': age}}})


@api.route("/json/")
def test2():
    return json.dumps(['json', '1', 2])
