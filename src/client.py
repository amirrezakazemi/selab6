from clientsDataBase import run_migrations, close_connection, query_db
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.before_first_request
def start_up():
    run_migrations()


@app.teardown_appcontext
def tear_down(exception):
    close_connection()


@app.route('/user/show-profile', methods=['GET'])
def show_profile():
    username = request.headers.get('User')
    if username:

        info = query_db('select * from profile where username=?', [username])
        if info:

            return jsonify(info), 200

        else:
            return jsonify({'error': 'Bad request'}), 400
    else:
        return ({'error': 'You are Not Logged IN'}), 401


@app.route('/user/update-profile', methods=['POST'])
def update_profile():
    username = request.headers.get('Authentication')
    if username:
        info = query_db('select * from profile where username=?', [username])
        if info:
            email = request.json.get('email')
            mobile = request.json.get('mobile')
            email = info.get('email') if email is None else email
            mobile = info.get('mobile') if mobile is None else mobile
            query_db('update profile set email=?, mobile=? where username=?', [email, mobile, username],
                     with_commit=True)
            return jsonify({'response':'profile updated'}), 200
        else:
            return jsonify({'error': 'Bad request'}), 400
    else:
        return ({'error': 'You are Not Logged IN'}), 401


@app.route('/user/create-profile', methods=['POST'])
def create_profile():
    username = request.json.get('username')
    email = request.json.get('email')
    mobile = request.json.get('mobile')
    query_db("""
            insert into profile(username, email, mobile, type)
            values (?, ?, ?, ?)
        """, [username, email, mobile, 'client'], with_commit=True)
    return jsonify({}), 201


if __name__ == '__main__':
    app.run(port=5000)
