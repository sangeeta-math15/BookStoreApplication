import pytest
import json
from django.urls import reverse


@pytest.fixture
def get_token_header(django_user_model, client):
    user = django_user_model.objects.create_user(username='suma', password='1234')
    user.save()
    # login user
    url = reverse('Login')
    data = {'username': 'suma', 'password': '1234'}
    response = client.post(url, data)
    json_data = json.loads(response.content)
    token = json_data['data']['token']
    header = {'HTTP_TOKEN': token, "content_type": "application/json"}
    return user, header



class TestBooksAPI:
    """
        Test Books API
    """

    @pytest.mark.django_db
    def test_response_as_create_book_successfully(self, client, get_token_header):
        # Create user
        user, header = get_token_header

        # Create books
        url = reverse('BooksView')
        data = {"author": "wilbur  Smith ",
                "title": "Ghost Fire",
                "quantity": 6,
                "price": 60}

        response = client.post(url, data, **header)
        json_data = json.loads(response.content)
        assert response.status_code == 201
        assert json_data['data']['title'] == 'Ghost Fire'

    @pytest.mark.django_db
    def test_response_as_validation_error_while_create_books(self, client, get_token_header):
        user, header = get_token_header
        # Create books
        url = reverse('BooksView')
        data = {"autho": "wilbur  Smith ",
                "title": "Ghost Fire",
                "quantity": 6,
                "price": 60}
        response = client.post(url, data, **header)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_response_as_get_books_successfully(self, client, get_token_header):
        user, header = get_token_header
        # Create books
        url = reverse('BooksView')
        data = {"author": "wilbur  Smith ",
                "title": "Ghost Fire",
                "quantity": 6,
                "price": 60}
        response = client.post(url, data, **header)
        json_data = json.loads(response.content)
        assert response.status_code == 201
        assert json_data['data']['title'] == 'Ghost Fire'

        # Get books
        user_data = {'user_id': user.id}
        url = reverse('BooksView')
        response = client.get(url, user_data, **header)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_response_as_update_books_successfully(self, client, get_token_header):
        user, header = get_token_header
        # create book
        url = reverse('BooksView')
        data = {"author": "wilbur  Smith ",
                "title": "Ghost Fire",
                "quantity": 6,
                "price": 60}
        response = client.post(url, data, **header)
        json_data = json.loads(response.content)
        book_id = json_data['data']['id']
        assert response.status_code == 201
        assert json_data['data']['title'] == 'Ghost Fire'

        # Update books
        url = reverse('BooksView')
        data = json.dumps(
            {'id': book_id,
             "author": "wilbur  Smith ",
             "title": "Ghost Fire",
             "quantity": 6,
             "price": 60})

        response = client.put(url, data, **header)
        json_data = json.loads(response.content)
        assert response.status_code == 202

    @pytest.mark.django_db
    def test_response_as_delete_books_successfully(self, client, get_token_header):
        user, header = get_token_header

        # Create books
        url = reverse('BooksView')
        data = json.dumps(
            {"author": "wilbur  Smith ",
             "title": "Ghost Fire",
             "quantity": 6,
             "price": 60})

        response = client.post(url, data, **header)
        json_data = json.loads(response.content)

        assert response.status_code == 201
        assert json_data['data']['title'] == 'Ghost Fire'

        # Delete books
        book_id = json_data['data']['id']
        url = reverse('BooksView')
        data = {'id': book_id}
        data = json.dumps(data)
        response = client.delete(url, data, **header)
        assert response.status_code == 204
