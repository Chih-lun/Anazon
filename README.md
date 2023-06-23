# Anazon

# What is Anazon

Anazon is a versatile e-commerce platform offering a wide range of products to fulfill your shopping desires. From luxurious fragrances to stylish furniture, cutting-edge smartphones to trendy sunglasses, Anazon has everything you need to enhance your lifestyle.

# How to start Anazon

## Install required package

1. cd anazon
2. pip install -r requirements.txt

## Configure environment variables. Package dotenv will load all them

1. cd anazon
2. touch .env
3. Add SECRET_KEY, DEBUG, STRIPE_API_KEY, STRIPE_ENDPOINT_SECRET

## Open stripe cli to listen stripe event

1. download stripe cli from https://stripe.com/docs/stripe-cli
2. stripe login
3. stripe listen --forward-to localhost:8000/stripe_webhook/

## Start Anazon

1. cd anazon
2. python manage.py runserver

# Features

## Index

![Alt text](images/image.png)

## Product

- Display products with tags as filter
  ![Alt text](images/image-1.png)

- Categories on navbar dropdown

![Alt text](images/image-2.png)

- Product details

![Alt text](images/image-3.png)

- Search product

![Alt text](images/image-4.png)

## Login

![Alt text](images/image-5.png)

## Register

![Alt text](images/image-6.png)

## Cart

- Dropdown cart

![Alt text](images/image-7.png)

- Cart detail

![Alt text](images/image-8.png)

## Checkout

- Confirmation and shipping information

![Alt text](images/image-9.png)

- Payment

![Alt text](images/image-10.png)

- Success

![Alt text](images/image-11.png)

## Order

- Summary

![Alt text](images/image-12.png)

- Order detail for items

![Alt text](images/image-13.png)

## RWD

![Alt text](images/image-14.png)

# Technologies Used

- Programming Languages: Python
- Framework: Django
- Front-end Technologies: HTML, CSS, JavaScript
- Database: SQLite
- Version Control: Git
