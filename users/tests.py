from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


# test the user registration endpoint
class RegistrationTestCase(APITestCase):
    def test_member_registration(self):
        data={"email":"testuser@gmail.com","password":"PASwwordLit",'role':'Member'}
        response=self.client.post('/api/v1/auth/users/',data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
    def test_trainer_registration(self):
        data={"email":"testtrainer@gmail.com","password":"PASwwordLit",'role':'Trainer'}
        response=self.client.post('/api/v1/auth/users/',data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

# test case for the userprofile model
class userProfileTestCase(APITestCase):
    def setUp(self):
        # create a new user making a post request to djoser endpoint
        self.user=self.client.post('/api/v1/auth/users/',data={'email':'mario@gmail.com','password':'i-keep-jumping', 'role': 'Member'})
        # obtain an auth token for the newly created user
        response=self.client.post('/api/v1/auth/token/login/',data={'email':'mario@gmail.com','password':'i-keep-jumping'})
        self.token=response.data['auth_token']
        self.api_authentication()
        
    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token '+self.token)

    def test_member_profile_create(self):
        response = self.client.post(reverse('users:member_api_urls:create_member_profile'), data={'user': User.objects.get(id=1), 'is_disabled': True,'description': 'test desc'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_memberprofile_detail_retrieve(self):
        self.client.post(reverse('users:member_api_urls:create_member_profile'), data={'user': User.objects.get(id=1), 'is_disabled': True,'description': 'test desc'})
        response=self.client.get(reverse('users:member_api_urls:member_profile_details',kwargs={'pk':1}))

        self.assertEqual(response.status_code,status.HTTP_200_OK)

        profile_data={'description':'I am a very famous game character','is_disabled': False,}
        response=self.client.patch(reverse('users:member_api_urls:member_profile_details',kwargs={'pk': 1}), data=profile_data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)