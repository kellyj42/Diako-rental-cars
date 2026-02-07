services = [
            {
                "icon": "fa-phone-alt",
                "title": "Phone Reservation",
                "description": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Reprehenderit ipsam quasi quibusdam ipsa perferendis iusto?"
            },
            {
                "icon": "fa-money-bill-alt",
                "title": "Special Rates",
                "description": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Reprehenderit ipsam quasi quibusdam ipsa perferendis iusto?"
            },
            {
                "icon": "fa-road",
                "title": "One Way Rental",
                "description": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Reprehenderit ipsam quasi quibusdam ipsa perferendis iusto?"
            },
            {
                "icon": "fa-umbrella",
                "title": "Life Insurance",
                "description": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Reprehenderit ipsam quasi quibusdam ipsa perferendis iusto?"
            },
            {
                "icon": "fa-building",
                "title": "City to City",
                "description": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Reprehenderit ipsam quasi quibusdam ipsa perferendis iusto?"
            },
            {
                "icon": "fa-car-alt",
                "title": "Free Rides",
                "description": "Lorem ipsum dolor sit amet consectetur adipisicing elit. Reprehenderit ipsam quasi quibusdam ipsa perferendis iusto?"
            },
        ]
achievements = [
        {
            "icon": "fa-thumbs-up",
            "count": 829,
            "label": "Happy Clients",
        },
        {
            "icon": "fa-car",
            "count": 56,
            "label": "Cars Available",
        },
        {
            "icon": "fa-building",
            "count": 127,
            "label": "Service Centers",
        },
        {
            "icon": "fa-clock",
            "count": 589,
            "label": "Total Trips Completed",
        },
    ]
vehicles = [
        {
            "image": "home/images/car3.jpg",
            "name": "Mercedes Benz R3",
            "price": 99,
            "rating": 4.5,
            "seats": 4,
            "transmission": "AT/MT",
            "fuel": "Petrol",
            "year": 2015,
            "gear": "AUTO",
            "mileage": "27K",
        },
        
    ]
nav_links = [
    {"name": "Home", "url": "home:home"},
    {"name": "Services", "url": "home:services"},
    # {"name": "Contact Us", "url": "home:#vehicles"},
    {
        "name": "About Us",
        "url": "home:about",
        "children": [
            # {"name": "Our Story", "url": "home:our_story"},
            # {"name": "Team", "url": "home:team"},
            # {"name": "Careers", "url": "home:careers"},
        ]
    },
    # {"name": "FAQs", "url": "home:faqs"},
]