import unittest

import requests

from app import app, books_db

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

    def test_get_books_has_books(self):
        try:
            response = self.client.get('/books')
            response_data = response.get_json()

            # Basic checks
            is_status_ok = response.status_code == 200
            is_list = isinstance(response_data, list)
            has_some_books = len(response_data) > 0

            # Check required fields in all returned books
            books_have_required_fields = True
            for book in response_data:
                if not all(k in book for k in ("id", "title", "author")):
                    books_have_required_fields = False
                    break

            result = is_status_ok and is_list and has_some_books and books_have_required_fields

            self.test_obj.yakshaAssert("TestGetBooksHasBooks", result, "functional")
            print("TestGetBooksHasBooks = Passed" if result else "TestGetBooksHasBooks = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestGetBooksHasBooks", False, "functional")
            print(f"TestGetBooksHasBooks = Failed | Exception: {e}")

    def test_books_count_is_three(self):
        try:
            # Call the GET /books endpoint
            response = requests.get("http://127.0.0.1:5000/books")
            books = response.json()

            # Validate
            is_status_ok = response.status_code == 200
            is_books_list = isinstance(books, list)
            is_books_count_three = len(books) == 3

            result = is_status_ok and is_books_list and is_books_count_three
            self.test_obj.yakshaAssert("TestBooksCountIsThree", result, "functional")
            print("TestBooksCountIsThree = Passed" if result else "TestBooksCountIsThree = Failed")

        except Exception as e:
            self.test_obj.yakshaAssert("TestBooksCountIsThree", False, "functional")
            print(f"TestBooksCountIsThree = Failed | Exception: {e}")



    def test_get_book_by_id(self):
        try:
            response = self.client.get('/book/1')
            result = response.status_code == 200 and 'title' in response.get_json()
            self.test_obj.yakshaAssert("TestGetBookById", result, "functional")
            print("TestGetBookById = Passed" if result else "TestGetBookById = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestGetBookById", False, "functional")
            print(f"TestGetBookById = Failed | Exception: {e}")

    def test_login_valid_credentials(self):
        try:
            valid_data = {'username': 'admin', 'password': 'secret'}
            response = self.client.post('/login', data=valid_data)

            result = (response.status_code == 200) and (b"Logged in as admin" in response.data)

            self.test_obj.yakshaAssert("TestLoginValidCredentials", result, "functional")
            print("TestLoginValidCredentials = Passed" if result else "TestLoginValidCredentials = Failed")
        except Exception as e:
            self.test_obj.yakshaAssert("TestLoginValidCredentials", False, "functional")
            print(f"TestLoginValidCredentials = Failed | Exception: {e}")

    def test_get_reviews(self):
        try:
            response = requests.get("http://127.0.0.1:5000/api/reviews")
            data = response.json()

            # Check status code is 200 OK
            is_status_ok = response.status_code == 200

            # Check the data is a non-empty list
            is_list_and_not_empty = isinstance(data, list) and len(data) > 0

            # Ensure all reviews have required fields
            valid_reviews = all(
                isinstance(review, dict) and
                all(k in review for k in ("book_id", "rating", "comment"))
                for review in data
            )

            result = is_status_ok and is_list_and_not_empty and valid_reviews

            self.test_obj.yakshaAssert("TestGetReviews", result, "functional")
            print("TestGetReviews = Passed" if result else "TestGetReviews = Failed")

        except Exception as e:
            self.test_obj.yakshaAssert("TestGetReviews", False, "functional")
            print(f"TestGetReviews = Failed | Exception: {e}")
    def test_review_has_required_fields_for_book1(self):
        try:
            # Fetch all reviews from the live endpoint
            response = requests.get("http://127.0.0.1:5000/api/reviews")
            response_data = response.json()

            # Check for at least one review for book_id=1 with required fields
            review_found = any(
                isinstance(review, dict) and
                review.get("book_id") == 1 and
                all(key in review for key in ["rating", "comment"])
                for review in response_data
            )

            self.test_obj.yakshaAssert("TestReviewHasRequiredFieldsForBook1", review_found, "functional")
            print("TestReviewHasRequiredFieldsForBook1 = Passed" if review_found else "TestReviewHasRequiredFieldsForBook1 = Failed")

        except Exception as e:
            self.test_obj.yakshaAssert("TestReviewHasRequiredFieldsForBook1", False, "functional")
            print(f"TestReviewHasRequiredFieldsForBook1 = Failed | Exception: {e}")


if __name__ == "__main__":
    unittest.main()
