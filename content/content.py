import os

services = [
    {
        "icon": "fa-plane-arrival",
        "title": "Airport Pickups",
        "description": "Enjoy timely airport pickup and drop-off services with comfortable vehicles and dependable drivers for local and visiting travelers."
    },
    {
        "icon": "fa-id-badge",
        "title": "Driver Hire",
        "description": "Hire a professional driver for business trips, city movements, family travel, events, or long-distance journeys across Uganda."
    },
    {
        "icon": "fa-ticket",
        "title": "Ticket Booking",
        "description": "Get support with ticket booking arrangements for selected travel needs, giving clients a smoother transport and travel planning experience."
    },
    {
        "icon": "fa-car-side",
        "title": "Car Rentals",
        "description": "Choose from our rental fleet for self-drive or chauffeur-supported travel, with options suitable for individuals, families, and groups."
    },
]

achievements = [
        {
            "icon": "car",
            "count": 212,
            "label": "Happy Clients",
        },
        {
            "icon": "bus",
            "count": 15,
            "label": "Cars Available",
        },
        {
            "icon": "truck",
            "count": 380,
            "label": "Total Trips Completed",
        },
    ]
vehicles = [
       
        {
            "icon": "fa-van-shuttle",
            "name": "Vans",
            "image": "home/images/showroom/Van.png",
            "image_url": os.getenv("CATEGORY_VANS_IMAGE_URL", "").strip(),
            "description": "Ideal for airport transfers, group travel, and family road trips.",
        },
        {
            "icon": "fa-car",
            "name": "Sedans",
            "image": "home/images/showroom/Sedan.png",
            "image_url": os.getenv("CATEGORY_SEDANS_IMAGE_URL", "").strip(),
            "description": "Comfortable city and business travel with everyday convenience.",
        },
        {
            "icon": "fa-truck-monster",
            "name": "SUVs",
            "image": "home/images/showroom/SUV.png",
            "image_url": os.getenv("CATEGORY_SUVS_IMAGE_URL", "").strip(),
            "description": "Spacious, confident handling for upcountry roads and longer journeys.",
        },
        {
            "icon": "fa-bus",
            "name": "Coasters",
            "image": "home/images/showroom/Coaster.png",
            "image_url": os.getenv("CATEGORY_COASTERS_IMAGE_URL", "").strip(),
            "description": "Best for tours, team travel, events, and larger group transport.",
        },
        
    ]
nav_links = [
    {"name": "Home", "url": "home:home"},
    {"name": "Cars", "url": "cars:car_list"},
    {"name": "Services", "url": "home:services"},
    {"name": "Contact Us", "url": "home:contact"},
    {
        "name": "About Us",
        "url": "home:about",
        "children": [
            {"name": "Our Story", "url": "home:our_story"},
            {"name": "Team", "url": "home:team"},
            {"name": "Careers", "url": "home:careers"},
        ]
    },
    # {"name": "FAQs", "url": "home:faqs"},
]

contact_info = {
    "location": {
        "header": "Shell, Najjera 1 Kilimani mall",
        "contact": "Shell, Najjera 1 Kilimani mall",
        "faqs": "Shell, Najjera 1 Kilimani mall",
    },
    "phone": {
        "header": "0749744516",
        "faqs": "0749744516",
        "support": {
            "display": "0749744516",
            "tel": "0749744516",
        },
        "whatsapp": {
            "display": "0751757306",
            "wa": "256751757306",
        },
    },
    "email": {
        "header": "daikotravelagency@gmail.com",
        "contact": "daikotravelagency@gmail.com",
        "faqs": "daikotravelagency@gmail.com",
        "support": "daikotravelagency@gmail.com",
    },
}
