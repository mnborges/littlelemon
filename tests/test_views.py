from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory
from django.urls import reverse
from restaurant.models import MenuItem
from restaurant.views import MenuItemView, SingleMenuItemView

class MenuViewTest(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.user = AnonymousUser()
        for i in range(3):
            MenuItem.objects.create(
                id=i+1,
                title=f"Cheeseburger {i+1}",
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
                'title' : 'Cheeseburger 1',
                'price' : '8.50',
                'inventory': 1
            },
            {
                'id' : 2,
                'title' : 'Cheeseburger 2',
                'price' : '9.00',
                'inventory': 2
            },
            {
                'id' : 3,
                'title' : 'Cheeseburger 3',
                'price' : '9.50',
                'inventory': 3
            }
        ])
        
    def test_create(self):
        new_menuitem = {
            'title' : 'Tortilla',
            'price' : 4.5,
            'inventory' : 8,
        }
        request = self.factory.post(reverse('menu-items'), data=new_menuitem)
        request.user = self.user
        response = MenuItemView.as_view()(request)
        response.render()
        self.assertEqual(response.status_code, 201)
        self.assertTrue(MenuItem.objects.filter(
            title='Tortilla',
            price=4.5,
            inventory=8,
        ).exists())
        
    def test_getitem(self):
        menuitem_id = 1
        request = self.factory.get(reverse('menu-single-item', args=[menuitem_id]))
        request.user = self.user
        response = SingleMenuItemView.as_view()(request, pk=menuitem_id)
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, 
            {
                'id' : 1,
                'title' : 'Cheeseburger 1',
                'price' : '8.50',
                'inventory': 1
            }
        )
        
    def test_update_item(self):
        menuitem_id = 1
        new_menuitem_data = {
            'title' : 'Tortilla 2',
            'price' : 5,
            'inventory' : 9
        }
        request = self.factory.put(reverse('menu-single-item', args=[menuitem_id]), 
                                   data=new_menuitem_data, content_type='application/json')
        request.user = self.user
        response = SingleMenuItemView.as_view()(request, pk=menuitem_id)
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, 
            {
                'id' : 1,
                'title' : 'Tortilla 2',
                'price' : '5.00',
                'inventory': 9
            }
        )
        
    def test_partially_update_item(self):
        menuitem_id = 1
        new_menuitem_data = {
            'inventory' : 99
        }
        request = self.factory.patch(reverse('menu-single-item', args=[menuitem_id]), 
                                     data=new_menuitem_data, content_type='application/json')
        request.user = self.user
        response = SingleMenuItemView.as_view()(request, pk=menuitem_id)
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, 
            {
                'id' : 1,
                'title' : 'Cheeseburger 1',
                'price' : '8.50',
                'inventory': 99
            }
        )
        
    def test_delete_item(self):
        menuitem_id = 1
        request = self.factory.delete(reverse('menu-single-item', args=[menuitem_id]))
        request.user = self.user
        response = SingleMenuItemView.as_view()(request, pk=menuitem_id)
        response.render()
        self.assertEqual(response.status_code, 204)
        self.assertFalse(MenuItem.objects.filter(pk=menuitem_id).exists())
        
        