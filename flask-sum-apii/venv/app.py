from flask import Flask, request, jsonify
from models import Sum
from database import db
import os

app = Flask(__name__)

# Database Configuration (Use an environment variable for production)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://user:password@host:port/database')
# Example for local: app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost:5432/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/sum', methods=['POST'])
def add_sum():
    data = request.get_json()
    num1 = data.get('num1')
    num2 = data.get('num2')
    if num1 is None or num2 is None:
        return jsonify({'error': 'Missing num1 or num2'}), 400

    try:
        num1 = int(num1)
        num2 = int(num2)
    except ValueError:
        return jsonify({'error': 'Invalid input for num1 or num2'}), 400

    result = num1 + num2
    new_sum = Sum(num1=num1, num2=num2, result=result)
    db.session.add(new_sum)
    db.session.commit()
    return jsonify({'message': 'Sum added successfully', 'result': result}), 201


@app.route('/sums', methods=['GET'])
def get_sums():
    sums = Sum.query.all()
    sum_list = []
    for sum_obj in sums:
        sum_list.append({'id': sum_obj.id, 'num1': sum_obj.num1, 'num2': sum_obj.num2, 'result': sum_obj.result})
    return jsonify({'sums': sum_list}), 200


@app.route('/sum/result/<int:result>', methods=['GET'])
def get_sums_by_result(result):
    sums = Sum.query.filter_by(result=result).all()
    sum_list = []
    for sum_obj in sums:
        sum_list.append({'id': sum_obj.id, 'num1': sum_obj.num1, 'num2': sum_obj.num2, 'result': sum_obj.result})

    return jsonify({'sums': sum_list}), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database if it doesn't exist
    app.run(debug=True)