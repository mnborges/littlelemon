from django.contrib.auth.models import AnonymousUser, User
from django.test import TestCase, RequestFactory
from django.urls import reverse
from rest_framework.test import APIRequestFactory
from restaurant.models import MenuItem, Booking
from restaurant.views import MenuItemView, SingleMenuItemView, BookingViewSet

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
        
class BookingViewTest(TestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.user = User.objects.create(username='testing', password='littlelemon!123')
        for i in range(1,4):
            Booking.objects.create(
                id = i,
                name = f'Bard {i}',
                no_of_guests = i,
                bookingDate = f'2023-09-0{i}T00:00:00Z'
            )
            
    def test_getall(self):
        request = self.factory.get(reverse('reservation-list'))
        request.user = self.user
        response = BookingViewSet.as_view({'get':'list'})(request)
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, [
            {
                'id' : 1,
                'name' : 'Bard 1',
                'no_of_guests' : 1,
                'bookingDate': '2023-09-01T00:00:00Z'
            },
            {
                'id' : 2,
                'name' : 'Bard 2',
                'no_of_guests' : 2,
                'bookingDate': '2023-09-02T00:00:00Z'
            },
            {
                'id' : 3,
                'name' : 'Bard 3',
                'no_of_guests' : 3,
                'bookingDate': '2023-09-03T00:00:00Z'
            }
        ])
        
    def test_create(self):
        new_reservation = {
            'name' : 'Rogue',
            'no_of_guests' : 6,
            'bookingDate' : '2023-08-01T00:00:00Z',
        }
        request = self.factory.post(reverse('reservation-list'), data=new_reservation)
        request.user = self.user
        response = BookingViewSet.as_view({'post': 'create'})(request)
        response.render()
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Booking.objects.filter(
            name='Rogue',
            no_of_guests=6,
            bookingDate='2023-08-01T00:00:00Z',
        ).exists())
        
    def test_get_reservation(self):
        reservation_id = 1
        request = self.factory.get(reverse('reservation-detail', args=[reservation_id]))
        request.user = self.user
        response = BookingViewSet.as_view({'get':'retrieve'})(request, pk=reservation_id)
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, 
            {
                'id' : 1,
                'name' : 'Bard 1',
                'no_of_guests' : 1,
                'bookingDate': '2023-09-01T00:00:00Z'
            }
        )
        
    def test_update_reservation(self):
        reservation_id = 1
        new_reservation = {
            'name' : 'Rogue 2',
            'no_of_guests' : 7,
            'bookingDate' : '2023-08-02T00:00:00Z',
        }
        request = self.factory.put(reverse('reservation-detail', args=[reservation_id]), 
                                   data=new_reservation)
        request.user = self.user
        response = BookingViewSet.as_view({'put': 'update'})(request, pk=reservation_id)
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, 
            {
                'id' : 1,
                'name' : 'Rogue 2',
                'no_of_guests' : 7,
                'bookingDate': '2023-08-02T00:00:00Z'
            }
        )
        
    def test_partially_update_reservation(self):
        reservation_id = 1
        new_reservation = {
            'no_of_guests' : 99,
        }
        request = self.factory.patch(reverse('reservation-detail', args=[reservation_id]), 
                                     data=new_reservation)
        request.user = self.user
        response = BookingViewSet.as_view({'patch': 'partial_update'})(request, pk=reservation_id)
        response.render()
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, 
            {
                'id' : 1,
                'name' : 'Bard 1',
                'no_of_guests' : 99,
                'bookingDate': '2023-09-01T00:00:00Z'
            }
        )
        
    def test_delete_reservation(self):
        reservation_id = 1
        request = self.factory.delete(reverse('reservation-detail', args=[reservation_id]))
        request.user = self.user
        response = BookingViewSet.as_view({'delete':'destroy'})(request, pk=reservation_id)
        response.render()
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Booking.objects.filter(pk=reservation_id).exists())