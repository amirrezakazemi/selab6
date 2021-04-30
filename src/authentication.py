from flask import Flask, request, jsonify, make_response
import requests
import jwt

from authenticationDataBase import run_migrations, close_connection, query_db

app = Flask(__name__)
jwt_secret_key = 'random secret'
create_profile_endpoint = 'http://localhost:5000/user/create-profile'


@app.before_first_request
def start_up():
    run_migrations()


@app.teardown_appcontext
def tear_down(exception):
    close_connection()


@app.route('/auth/sign-up', methods=['POST'])
def sign_up():
    username = request.json.get('username')
    password = request.json.get('password')
    mobile = request.json.get('mobile')
    email = request.json.get('email')


    response = requests.post(create_profile_endpoint, json={
        'username': username,
        'mobile': mobile,
        'email': email

    })

    if response.status_code != 201:
        return jsonify(response.json()), response.status_code

    query_db("""
            insert into auth_user(username, password)
            values (?, ?);
        """, args=(username, password), with_commit=True)

    return jsonify({'response':'Successfully Signed UP'}), 201


@app.route('/auth/login', methods=['POST'])
@app.route('/auth/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    print(username)

    user = query_db('select * from auth_user where username = ? and password = ?',
                    args=(username, password), one=True)
    if not user:
        return jsonify({"error": "Please enter password/username correctly"}), 401


    response = make_response(jsonify({'response':'You are now logged in '}))
    response.headers['Authorization'] = username
    return response


@app.route('/auth/get-username', methods=['GET'])
def get_username():
    token = request.headers.get('Authentication')
    if token is None:
        return jsonify({"error": "aAuthentication header NOT found"}), 401

    data = jwt.decode(
        jwt=token,
        key=jwt_secret_key,
        algorithms=["HS256"]
    )

    if 'username' not in data:
        return jsonify({"error": "Authentication header NOT valid"}), 401

    return jsonify({'username': data['username']}), 200


if __name__ == '__main__':
    app.run(port=3000)
