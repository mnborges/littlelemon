Index View (With Littlelemon logo)
    - GET restaurant/menu/

Authentication
    - Create a new user
        - POST /auth/users/
        - Payload example:
        {
            "email": "rogue@email.com",
            "username": "rogue",
            "password": "littlelemon!123"
        }
    - Generate auth token
        - POST /auth/token/login/
        - Payload example
        {
            "username": "rogue",
            "password": "littlelemon!123"
        }

Menu API (No Authentication Required)
base path: /restaurant/menu/items/
    - List all menu items
        - GET /restaurant/menu/items/
    - Create a new menu item
        - POST /restaurant/menu/items/
        - Payload example:
            {
                "title": "Classic Cheeseburguer",
		        "price": 10.9,
		        "inventory": 2
            }
    - Detail a menu item
        - GET /restaurant/menu/items/<int:pk>/
    - Update a menu item
        - PUT/PATCH /restaurant/menu/items/<int:pk>/
        - Payload example:
            {
                "title": "Cheeseburguer Oldschool",
		        "price": 14.9,
		        "inventory": 1
            }
    - Delete a menu item
        - DELETE /restaurant/menu/items/<int:pk>/

Booking API (Authentication Required)
base path: /restaurant/booking/tables/
    - List all bookings
        - GET /restaurant/booking/tables/
    - Create a new booking
        - POST /restaurant/booking/tables/
        - Payload example:
            {
                "name": "Tiefling Wizard",
                "no_of_guests": 6,
                "bookingDate": "2023-09-15T12:00:03Z"
            }
    - Detail a booking
        - GET /restaurant/booking/tables/<int:pk>/
    - Update a booking
        - PUT/PATCH /restaurant/booking/tables/<int:pk>/
        - Payload example:
            {
                "name": "Half-Orc Barbarian",
                "no_of_guests": 10,
                "bookingDate": "2023-09-16T12:00:03Z"
            }
    - Delete a booking
        - DELETE /restaurant/booking/tables/<int:pk>/