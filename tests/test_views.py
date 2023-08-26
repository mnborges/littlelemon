from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse
from restaurant.models import MenuItem
from restaurant.views import MenuItemView

class MenuViewTest(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user = User.objects.create(
            username='testuser',
            password="littlelemon!123"
        )
        for i in range(3):
            MenuItem.objects.create(
                id=i+1,
                title=f"Cheeseburguer {i+1}",
                price=8.5 + .5*i,
                inventory=i+1
            )
    def test_getall(self):
        request = self.factory.get(reverse('menu-items'))
        request.user = self.user
        response = MenuItemView.as_view()(request)
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, [
            {
                'id' : 1,
                'title' : 'Cheeseburguer 1',
                'price' : '8.50',
                'inventory': 1
            },
            {
                'id' : 2,
                'title' : 'Cheeseburguer 2',
                'price' : '9.00',
                'inventory': 2
            },
            {
                'id' : 3,
                'title' : 'Cheeseburguer 3',
                'price' : '9.50',
                'inventory': 3
            }
        ])
        
        