import decimal
import random
from os import path
from time import sleep
from django.core.mail import send_mail, EmailMessage
from qrcode import make
from electronics import settings
from .settings import EMAIL_HOST_USER
from entities.models import Entity, EntityType, Address, Contact
from products.models import Product
from users.models import User, UserAPIKey


def increase_debt():
    entities = Entity.objects.exclude(type__name='factory')
    for entity in entities:
        entity.debt = entity.debt + decimal.Decimal(
            random.randrange(500.00, 50000.00)
        ) / 100
        entity.save()


def decrease_debt():
    entities = Entity.objects.exclude(type__name='factory')
    for entity in entities:
        amount_to_decrease = decimal.Decimal(
            random.randrange(10000.00, 1000000.00)
        ) / 100
        entity.debt = entity.debt - amount_to_decrease \
            if entity.debt >= amount_to_decrease\
            else 0
        entity.save()


def make_debt_zero(entities_id):
    for entity_id in entities_id:
        entity = Entity.objects.get(pk=entity_id)
        entity.debt = 0.00
        entity.save()


def send_qr_email(email, new_data, entity_name):
    img = make(new_data)
    img_name = 'qr' + entity_name + '.png'
    img.save(settings.MEDIA_ROOT / img_name)
    file_path = path.relpath("media/" + img_name)
    sleep(10)
    mail = EmailMessage(
        subject="QR CODE",
        body=f"Please find below QR Code for company {entity_name}",
        from_email=EMAIL_HOST_USER,
        to=[email],
    )
    mail.content_subtype = 'html'
    mail.attach_file(file_path)
    mail.send()


def send_api_key(email, key):
    subject = "Registration confirmation"
    message = f"You have been registered successfully!\n" \
              f"Please find here below your API KEY.\n" \
              f"Please keep it in secret and don't show it to any persons.\n" \
              f"API KEY: {key}"
    email_from = EMAIL_HOST_USER
    recipient_list = [email]
    print(message)
    send_mail(
        subject, message, email_from,
        recipient_list, fail_silently=False
    )


def populate_db_with_data():
    # entity types
    list_of_types = [
        {'name': 'factory', 'level': 1},
        {'name': 'distributor', 'level': 2},
        {'name': 'dealer center', 'level': 3},
        {'name': 'large retail chain', 'level': 4},
        {'name': 'entrepreneur', 'level': 5}
    ]

    for entity_type in list_of_types:
        entity_type_db = EntityType.objects.filter(name=entity_type['name'])
        if entity_type_db:
            continue
        EntityType.objects.create(**entity_type)

    # products
    products = {
        'names':
            [
                'vacuum cleaner', 'washing machine', 'refrigerator',
                'drying machine', 'coffee machine', 'microwave oven',
                'home theatre'
            ],
        'models':
            [
                'samsung', 'philips', 'LG', 'siemens', 'bosch', 'electrolux', 'AEG'
            ]
    }

    for name in products['names']:
        for model in products['models']:
            product_name = f'{name} {model}'
            launch_date = f'2022-{random.randrange(1, 10)}-{random.randrange(1, 28)}'
            product_id_db = Product.objects.filter(name=product_name)
            if product_id_db:
                continue
            Product.objects.create(
                name=product_name,
                model=model,
                launch_date=launch_date
            )

    # entities
    addresses = [
        {
            'country': 'Belarus',
            'city': [
                'Minsk', 'Grodno', 'Gomel', 'Brest', 'Vitebsk', 'Mogilev'
            ],
            'street': [
                'Gorkogo', 'Pobedy', 'Vostochnaya', 'Suvorova', 'Tsentralnaya',
                'Sovetskaya', 'Moskovskaya', 'Dzerzhinskogo', 'Pushkina'
            ],
            'building': [
                '10', '30', '41C', '2', '12', '100',
                '98', '56', '39', '73', '121', '23', '12'
            ]
        },
        {
            'country': 'Russia',
            'city': ['Moscow', 'Samara', 'Kranodar', 'Voronezh'],
            'street': [
                'Gorkogo', 'Pobedy', 'Vostochnaya', 'Suvorova', 'Tsentralnaya',
                'Sovetskaya', 'Moskovskaya', 'Dzerzhinskogo', 'Pushkina'
            ],
            'building': [
                '11', '130', '41', '25', '127', '11', '9',
                '54', '39B', '63', '121', '23', '12'
            ]
         }
    ]

    for i in range(3):
        type = EntityType.objects.get(name='factory')
        type_name = type.name
        country = addresses[0]['country']
        len_city_list = len(addresses[0]['city'])
        city = addresses[0]['city'][random.randrange(0, len_city_list)]
        len_street_list = len(addresses[0]['street'])
        street = addresses[0]['street'][random.randrange(0, len_street_list)]
        len_building_list = len(addresses[0]['building'])
        building = addresses[0]['building'][random.randrange(
            0, len_building_list
        )]
        address_data = {
            'country': country,
            'city': city,
            'street': street,
            'building': building
        }
        name = f'Electronics {type_name} {city} {i}'
        entity_in_db = Entity.objects.filter(name=name)
        if entity_in_db:
            continue
        email = f'electronics_{type_name.replace(" ", "_")}@' \
                f'electronics-{city.lower()}{i}.com'
        address = Address.objects.create(**address_data)
        contact = Contact.objects.create(email=email, address_id=address.id)
        factory_data = {'name': name, 'type': type}
        entity = Entity.objects.create(**factory_data, contact_id=address.id)
        products = random.choices(Product.objects.all(), k=30)
        for product in products:
            entity.products.add(product)

    for i in range(30):
        types = EntityType.objects.exclude(name='factory')
        type = random.choice(types)
        type_name = type.name
        country = addresses[0]['country']
        len_city_list = len(addresses[0]['city'])
        city = addresses[0]['city'][random.randrange(0, len_city_list)]
        len_street_list = len(addresses[0]['street'])
        street = addresses[0]['street'][random.randrange(0, len_street_list)]
        len_building_list = len(addresses[0]['building'])
        building = addresses[0]['building'][random.randrange(
            0, len_building_list
        )]
        address_data = {
            'country': country,
            'city': city,
            'street': street,
            'building': building
        }
        name = f'Electronics {type_name} {city} {i}'
        entity_in_db = Entity.objects.filter(name=name)
        if entity_in_db:
            continue
        email = f'electronics_{type_name.replace(" ", "_")}@' \
                f'electronics-{city.lower()}{i}.com'
        suppliers = Entity.objects.exclude(type__level__gte=type.level)
        supplier = random.choice(suppliers)
        address = Address.objects.create(**address_data)
        contact = Contact.objects.create(email=email, address_id=address.id)
        entity_data = {'name': name, 'type': type}
        entity = Entity.objects.create(
            **entity_data,
            contact_id=address.id,
            supplier=supplier
        )
        products = random.choices(Product.objects.all(), k=30)
        for product in products:
            entity.products.add(product)

    for i in range(10):
        types = EntityType.objects.exclude(name='factory')
        type = random.choice(types)
        type_name = type.name
        country = addresses[1]['country']
        len_city_list = len(addresses[1]['city'])
        city = addresses[1]['city'][random.randrange(0, len_city_list)]
        len_street_list = len(addresses[1]['street'])
        street = addresses[1]['street'][random.randrange(0, len_street_list)]
        len_building_list = len(addresses[1]['building'])
        building = addresses[1]['building'][random.randrange(
            0, len_building_list
        )]
        address_data = {
            'country': country,
            'city': city,
            'street': street,
            'building': building
        }
        name = f'Electronics {type_name} {city} {i}'
        entity_in_db = Entity.objects.filter(name=name)
        if entity_in_db:
            continue
        email = f'electronics_{type_name.replace(" ", "_")}@' \
                f'electronics-{city.lower()}{i}.com'
        suppliers = Entity.objects.exclude(type__level__gte=type.level)
        supplier = random.choice(suppliers)
        address = Address.objects.create(**address_data)
        contact = Contact.objects.create(email=email, address_id=address.id)
        entity_data = {'name': name, 'type': type}
        entity = Entity.objects.create(
            **entity_data,
            contact_id=address.id,
            supplier=supplier
        )
        for product in products:
            entity.products.add(product)

    # create users and api_key
    entities = Entity.objects.all()
    for i in range(1, 100):
        entity = random.choice(entities)
        username = f'alex{i}'
        email = f'{username}@{entity.contact.email.split("@")[1]}'
        password = 12345
        user_in_db = User.objects.filter(username=username)
        if user_in_db:
            continue
        user = User.objects.create(
            username=username,
            email=email,
            password=password,
            entity=entity
        )
        if user:
            api_key, key = UserAPIKey.objects.create_key(user=user, name='electronics')
            print(key)
