from django.test import TestCase
from ImgUr.models import Subscriber

class IndexTestCase(TestCase):
    def test_index_status(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_add_subscriber(self):
        reg_data = {
            'name': "Andrey",
            'email': '1@1.com',
        }
        self.assertEqual(Subscriber.objects.count(), 0)
        response = self.client.post('/', data=reg_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Subscriber.objects.count(), 1)
        subscriber = Subscriber.objects.first()
        self.assertEqual(subscriber.name, "Andrey")
        self.assertEqual(subscriber.email, "1@1.com")

    def test_unsubscribe_status_without_email(self):
        response = self.client.get('/unsubscribe/')
        self.assertEqual(response.status_code, 400)

    def test_unsubscribe_status(self):
        response = self.client.get('/unsubscribe/', data={'email': "1@1.com"},
                                   follow=True)
        self.assertEqual(response.status_code, 200)
