import unittest
import json
from app import app, db
from models import Sum

class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory SQLite for tests
        self.app = app.test_client()

        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_sum(self):
        response = self.app.post('/sum', json={'num1': 5, 'num2': 3})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json.loads(response.data)['result'], 8)

    def test_get_sums(self):
        with app.app_context():
            sum1 = Sum(num1=5, num2=3, result=8)
            sum2 = Sum(num1=2, num2=2, result=4)
            db.session.add(sum1)
            db.session.add(sum2)
            db.session.commit()

        response = self.app.get('/sums')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data['sums']), 2)

    def test_get_sums_by_result(self):
        with app.app_context():
            sum1 = Sum(num1=5, num2=3, result=8)
            sum2 = Sum(num1=2, num2=2, result=4)
            sum3 = Sum(num1=1, num2=3, result=4)
            db.session.add(sum1)
            db.session.add(sum2)
            db.session.add(sum3)
            db.session.commit()

        # Test with existing result
        response = self.app.get('/sum/result/4')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data['sums']), 2)

        # Test with non-existent result
        response = self.app.get('/sum/result/999')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data['sums']), 0)

    def test_get_sums_by_result_invalid(self):
        response = self.app.get('/sum/result/invalid')  # Test with invalid filter value
        self.assertEqual(response.status_code, 404)  # Expect a 404 not found error


if __name__ == '__main__':
    unittest.main()