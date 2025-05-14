import unittest
from app import app

from tests.TestUtils import TestUtils
class FunctionalTests(unittest.TestCase):
    def setUp(self):
        self.test_obj = TestUtils()
        self.client = app.test_client()
        self.client.testing = True

    def test_home_page(self):
        try:
            response = self.client.get('/')
            result = response.status_code == 200 and b'Featured Books' in response.data
            self.test_obj.yakshaAssert("TestHomePage", result, "functional")
            print("TestHomePage = Passed" if result else "TestHomePage = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestHomePage", False, "functional")
            print(f"TestHomePage = Failed | Exception: {e}")

    def test_get_books(self):
        try:
            response = self.client.get('/books')
            result = response.status_code == 200 and isinstance(response.get_json(), list)
            self.test_obj.yakshaAssert("TestGetBooks", result, "functional")
            print("TestGetBooks = Passed" if result else "TestGetBooks = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestGetBooks", False, "functional")
            print(f"TestGetBooks = Failed | Exception: {e}")

    def test_add_book(self):
        try:
            book = {"id": 10, "title": "Yaksha Guide", "author": "AI"}
            response = self.client.post('/books', json=book)
            result = response.status_code == 201 and response.get_json() == book
            self.test_obj.yakshaAssert("TestAddBook", result, "functional")
            print("TestAddBook = Passed" if result else "TestAddBook = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestAddBook", False, "functional")
            print(f"TestAddBook = Failed | Exception: {e}")

    def test_get_book_by_id(self):
        try:
            response = self.client.get('/book/1')
            result = response.status_code == 200 and 'title' in response.get_json()
            self.test_obj.yakshaAssert("TestGetBookById", result, "functional")
            print("TestGetBookById = Passed" if result else "TestGetBookById = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestGetBookById", False, "functional")
            print(f"TestGetBookById = Failed | Exception: {e}")

    def test_search_books(self):
        try:
            response = self.client.get('/search?q=flask')
            result = response.status_code == 200 and isinstance(response.get_json(), list)
            self.test_obj.yakshaAssert("TestSearchBooks", result, "functional")
            print("TestSearchBooks = Passed" if result else "TestSearchBooks = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestSearchBooks", False, "functional")
            print(f"TestSearchBooks = Failed | Exception: {e}")

    def test_login_get(self):
        try:
            response = self.client.get('/login')
            result = response.status_code == 200 and b'<form' in response.data
            self.test_obj.yakshaAssert("TestLoginFormGet", result, "functional")
            print("TestLoginFormGet = Passed" if result else "TestLoginFormGet = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestLoginFormGet", False, "functional")
            print(f"TestLoginFormGet = Failed | Exception: {e}")

    def test_login_post_valid_credentials(self):
        try:
            response = self.client.post('/login', data={'username': 'admin', 'password': 'secret'})
            result = response.status_code == 200 and b'Logged in as admin' in response.data
            self.test_obj.yakshaAssert("TestLoginValidCredentials", result, "functional")
            print("TestLoginValidCredentials = Passed" if result else "TestLoginValidCredentials = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestLoginValidCredentials", False, "functional")
            print(f"TestLoginValidCredentials = Failed | Exception: {e}")

    def test_post_review(self):
        try:
            review = {"book_id": 1, "rating": 5, "comment": "Excellent!"}
            response = self.client.post('/api/review', json=review)
            result = response.status_code == 201 and response.get_json() == review
            self.test_obj.yakshaAssert("TestPostReview", result, "functional")
            print("TestPostReview = Passed" if result else "TestPostReview = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestPostReview", False, "functional")
            print(f"TestPostReview = Failed | Exception: {e}")

if __name__ == "__main__":
    unittest.main()
