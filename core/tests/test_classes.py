import json

from django.contrib.auth import get_user_model
from django.core.serializers.json import DjangoJSONEncoder
from django.urls import reverse
from django.utils.timezone import localtime, timedelta
from rest_framework import status
from rest_framework.test import APITestCase

from ..apiv1.serializers.gymclass import (GymClassListSerializer,
                                          WorkoutCategorySerializer)
from ..models import GymClass, WorkoutCategory

User = get_user_model()


class CreateGymClassTestCase(APITestCase):
    def setUp(self) -> None:
        self.category = WorkoutCategory.objects.create(
            name='HIIT', description='High intensity interval training')
        self.trainer = User.objects.create(first_name='Test',
                                           last_name='Trainer',
                                           email='testTrainer@gmail.com',
                                           role='Trainer')
        self.trainer.set_password('newasd123')
        self.trainer.save()
        # authenticate user for this test case
        response = self.client.post('/api/v1/auth/token/login/',
                                    data={
                                        'email': 'testTrainer@gmail.com',
                                        'password': 'newasd123'
                                    })
        self.token = response.data['auth_token']
        self.api_authentication()

        self.now = localtime()
        self.hour_from_now = localtime() + timedelta(hours=1)

        self.valid_class = {
            'name': 'hiit class',
            'category': self.category.pk,
            'location': 'Nairobi/Kenya',
            'day_of_week': 'Wednesday',
            'trainer': self.trainer.pk,
            'start_time': self.now,
            'end_time': self.hour_from_now,
            'description': f'best class by {self.trainer.get_full_name()}'
        }
        self.invalid_class = {
            'name': 'invalid class',
            'category': self.category.id,
            'location': 'Nairobi/Kenya',
            'day_of_week': 'Wednesday',
            'trainer': self.trainer.id,
            'description': f'invalid class by {self.trainer.get_full_name()}'
        }

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token}')

    def test_gym_class_creation(self):
        valid_class = json.dumps(self.valid_class, cls=DjangoJSONEncoder)
        invalid_class = json.dumps(self.invalid_class, cls=DjangoJSONEncoder)
        response = self.client.post(reverse('core:gym_class_api:new_class'),
                                    data=valid_class,
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        invalid_class_response = self.client.post(
            reverse('core:gym_class_api:new_class'),
            data=invalid_class,
            content_type='application/json')
        self.assertEqual(invalid_class_response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_gym_class_creation_unathenticated_user(self) -> None:
        self.client.force_authenticate(user=None)
        valid_class = json.dumps(self.valid_class, cls=DjangoJSONEncoder)
        response = self.client.post(reverse('core:gym_class_api:new_class'),
                                    data=valid_class,
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class RetrieveUpdateDeleteGymClassAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.category = WorkoutCategory.objects.create(
            name='HIIT', description='High intensity interval training')
        self.trainer = User.objects.create(first_name='Test',
                                           last_name='Trainer',
                                           email='testTrainer@gmail.com',
                                           role='Trainer')
        self.trainer.set_password('newasd123')
        self.trainer.save()

        self.now = localtime()
        self.hour_from_now = localtime() + timedelta(hours=1)
        self.valid_class = {
            'name': 'cardio class',
            'category': self.category,
            'location': 'Kiambu/Kenya',
            'day_of_week': 'Saturday',
            'trainer': self.trainer,
            'start_time': self.now,
            'end_time': self.hour_from_now,
            'description': f'best class by {self.trainer.get_full_name()}'
        }
        self.gym_class = GymClass.objects.create(**self.valid_class)

        # authenticate user for this test case
        response = self.client.post('/api/v1/auth/token/login/',
                                    data={
                                        'email': 'testTrainer@gmail.com',
                                        'password': 'newasd123'
                                    })
        self.token = response.data['auth_token']
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' +self.token)

    def test_valid_update_gym_class(self) -> None:
        get_response = self.client.get(
            reverse('core:gym_class_api:gymclass_details',
                    kwargs={'pk': self.gym_class.id}))
        data = get_response.data

        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        self.assertEqual(data['name'], 'cardio class')

        patch_response = self.client.patch(reverse(
            'core:gym_class_api:gymclass_details',
            kwargs={'pk': self.gym_class.id}),
                                           data={
                                               'name': 'cardio class update',
                                               'location': 'New York'
                                           })
        patch_data = patch_response.data
        self.assertEqual(patch_response.status_code, status.HTTP_200_OK)
        self.assertEqual(patch_data['name'], 'cardio class update')

    def test_valid_delete_class(self) -> None:
        response = self.client.delete(
            reverse('core:gym_class_api:gymclass_delete',
                    kwargs={'pk': self.gym_class.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_class(self) -> None:
        response = self.client.delete(
            reverse('core:gym_class_api:gymclass_delete', kwargs={'pk': 20}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_workout_categories(self) -> None:
        response = self.client.get(reverse('core:gym_class_api:workout_categories'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        workout_categories = WorkoutCategorySerializer(WorkoutCategory.objects.all(), many=True)
        self.assertEqual(response.data, workout_categories.data)

    def test_valid_trainer_classes_list(self) -> None:
        response = self.client.get(reverse('core:gym_class_api:trainer_classes', kwargs={'trainer_pk': self.trainer.pk}))

        trainer_classes = GymClassListSerializer(GymClass.objects.filter(trainer_id=self.trainer.pk), many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, trainer_classes.data)