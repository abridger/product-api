# Product API

A small API built using Django and the Django REST Framework to import XML product files, and make a subset of the data available as a small RESTful API.

## Product files
The XML files in the `fixtures` directory represent data about products. The data is split into three main sections:
* `Identity`: Identity numbers for the product, the markets that it is available in, the name of the manufacturer and the title of the product.
* `Assets`: a list of product imags, with a URL linking to the image file.
* `Data`: richer details about the product, including the product description, a list of categories, nutritional information, allergy advice, the address of the manufacturer, as well as instructions from the packet, a list of ingredients and a physical specification of the packaging.


## Requrements
* `Docker`
* `Docker Compose`


## Project structure
* `app`: The main Django project settings
* `core`: Container app for core settings and shared functionality (eg. custom user model)
* `fixtures`: A directory of XML files representing product details
* `products`: The app for handling products - both importing these through a management task, providing the model for managing products, and the views and serializers for making these available on the REST API.
  * `models`: Contains the product model for storing and managing products
  * `tasks`: Utilities for processing and importing products
  * `views`: The logic for providing views to access product details


## Product imports
There are run automatically as part of the startup script (`startup.sh`). The product import task is wrapper in a Django management task so that it can easily be run through the Django management script (`python manage.py import_products`). The XML files for these are stored in the `fixtures` directory - currently, all files in this directory will be read and parsed as XML in order to create the products.

Not all product information is imported, but a small subset:
* The gtin ID number
* The brand/manufacturer name
* The description
* The categories
* The energy information
* The title
* The update timestamp of the product information


## Running the API
```bash
docker-compose up --build web
```

When the API is running, the Docker container should be bound to `localhost` port `80`.


## Running the tests
```bash
docker-compose up --build test
```

## Accessing the products
With the API running, these will be available on `/products/`. Individual products can be accessed at `/products/{PRODUCT_ID}/`. By default, all fields will be returned. To view only a subset of the available fields, you can specify a comma-separated list of fields in the query params. Eg. `/products/?fields=description`.


## Managing products
Once the API is running, products can be viewed and edited in the Django admin dashboard (`localhost/admin/`). This can be accessed using the following defaults:
* Username: `root`
* Password: `s!Q4awa65m5l34U7#RfYTJwd%0BNib`

These can be changed by updating the `ROOT_USERNAME` and `ROOT_PASSWORD` environment variables in the `docker-compose.yml` file.


## Future development
* Create related models - `categories`, `manufacturers` etc.
* Build out user models and introduce authentication
