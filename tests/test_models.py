from django.test import TestCase
from restaurant.models import MenuItem

class MenuItemTest(TestCase):
    def test_get_item(self):
        item = MenuItem.objects.create(
            title="Cheeseburguer",
            price = 10.9,
            inventory = 3
        )
        self.assertEqual(str(item), "Cheeseburguer : 10.9")
    