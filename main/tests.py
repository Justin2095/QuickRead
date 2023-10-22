import json
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from main.models import Subject


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user():
    return User.objects.create_user(
        username='adminuser', email='adminuser@example.com', password='adminpassword', is_staff=True, is_superuser=True
    )


@pytest.fixture
def auth_header(api_client, admin_user):
    url = reverse('api-token-auth')
    response = api_client.post(url, {'username': 'adminuser', 'password': 'adminpassword'})
    token = response.data['token']
    return {'HTTP_AUTHORIZATION': f'JWT {token}'}


def test_create_subject(api_client, auth_header):
    url = reverse('subject-list')
    data = {'name': 'Test Subject'}
    response = api_client.post(url, data, format='json', **auth_header)
    assert response.status_code == status.HTTP_201_CREATED
    assert Subject.objects.count() == 1
    assert Subject.objects.get().name == 'Test Subject'


def test_edit_profile(api_client, auth_header):
    user = User.objects.create_user('testuser', '', 'testpassword')
    url = reverse('user-detail', args=[user.id])
    api_client.get(url, format='json', **auth_header)

    url = reverse('profile-detail', args=[user.id])
    data = {
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'testuser@example.com',
        'about': 'I enjoy coding',
    }

    response = api_client.put(url, data, **auth_header)
    assert response.status_code == status.HTTP_200_OK

    response = api_client.get(url, format='json', **auth_header)
    assert response.status_code == status.HTTP_200_OK

    url = reverse('user-detail', args=[user.id])
    response = api_client.get(url, format='json', **auth_header)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['username'] == 'testuser'
    assert response.data['first_name'] == 'Test'
    assert response.data['last_name'] == 'User'
    assert response.data['profile']['about'] == 'I enjoy coding'
    assert response.data['email'] == 'testuser@example.com'


def test_create_subjects(api_client, auth_header):
    url = reverse('subject-list')
    subjects = [
        {
            'name': 'Science',
            'hours_per_week': '2,5',
        },
        {
            'name': 'Art',
            'hours_per_week': '0,5',
        }
    ]

    for subject_data in subjects:
        response = api_client.post(url, subject_data, format='json', **auth_header)
        assert response.status_code == status.HTTP_201_CREATED

    response = api_client.get(url, format='json', **auth_header)
    assert response.status_code == status.HTTP_200_OK
    subjects = json.loads(response.content)
    assert len(subjects) == 2
    assert subjects[0]['name'] == 'Science'


def test_edit_profile_subjects(api_client, auth_header):
    user = User.objects.create_user('testuser', '', 'testpassword')
    url = reverse('user-detail', args=[user.id])
    api_client.get(url, format='json', **auth_header)

    url = reverse('subject-list')
    subjects = [
        {
            'name': 'Science',
            'hours_per_week': '2,5',
            'user': 'testuser'

        },
        {
            'name': 'Art',
            'hours_per_week': '0,5',
            'user': 'testuser'
        }
    ]

    for subject_data in subjects:
        response = api_client.post(url, subject_data, format='json', **auth_header)
        assert response.status_code == status.HTTP_201_CREATED

    response = api_client.get(url, format='json', **auth_header)
    assert response.status_code == status.HTTP_200_OK
    subjects = json.loads(response.content)
    assert len(subjects) == 2
    assert subjects[0]['name'] == 'Science'

    url = reverse('profile-detail', args=[user.id])
    data = {
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'testuser@example.com',
        'about': 'I enjoy coding',
    }

    response = api_client.put(url, data, **auth_header)
    assert response.status_code == status.HTTP_200_OK
