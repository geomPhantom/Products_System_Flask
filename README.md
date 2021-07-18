# Products System (Flask)

Simple product management system for e-shop – RESTful API providing CRUD operations, based on Flask framework.

Each **product** has 5 required (non-null) parameters:

1. **id** - primary key (integer)
2. **SKU** – another unique identifier (string, max 16 length)
3. **name** (string, max 120 length)
4. **type_id** – product type id (integer, foreign key – referencing id in Types table)
5. **price** (float)

Additional table represents types of products (id -> name).

It is important to note that SKU is expected to contain at least one letter.

API provides methods to create, get, edit and delete products. All methods, if not stated otherwise, accept and return JSON data.

## API details

### 1. Create product
### ``` POST /products```
Creates product.

**Input parameters:**

1. **`SKU`** (string, **required**)
2. **`name`** (string, **required**)
3. **`type_id`** (int, **required**)
4. **`price`** (float, **required**)

On success product is added into DB, method returns **`id`** of created product. Otherwise, returns 400 HTTP status code.

### 2. Edit product
Depending on a type of the URL parameter, method provides ability to edit/update the product using **`id`** or **`SKU`**.
### ```PUT /products/<int:id>```

Edit the product using **`id`**.

**Input parameters:**

1. **`id`** (integer, **required**, URL parameter)
2. **`SKU`** (string, optional)
3. **`name`** (string, optional)
4. **`type_id`** (int, optional)
5. **`price`** (float, optional)

### ```PUT /products/<string:SKU>```

Edit the product using **`SKU`**.

**Input parameters:**

1. **`SKU`** (string, **required**, URL parameter)
2. **`name`** (string, optional)
3. **`type_id`** (int, optional)
4. **`price`** (float, optional)

All irrelevant parameters are ignored. 

On successful call, both methods **return** updated product in the following **JSON** format:
```json
{
   "SKU": "123PTD",
   "id": 5,
   "name": "Final Cut Pro X",
   "price": 2999.0,
   "type_id": 1
}
```

If product is not found, methods return corresponding error (404 HTTP status). If invalid parameters are sent, 400 HTTP status code is returned.

### 3. Delete product

Depending on a type of the URL parameter, method provides ability to delete the product using **`id`** or **`SKU`**.
### ```DELETE /products/<int:id>```

Delete the product using **`id`**.

**Input parameters:**

- **`id`** (integer, **required**, URL parameter)


### ```DELETE /products/<string:SKU>```

Delete the product using **`SKU`**.

**Input parameters:**

- **`SKU`** (string, **required**, URL parameter)

On successful call, both methods **return** the following **JSON**:
```json
{
   "Result": "Product successfully deleted"
}
```

If product is not found, methods return corresponding error (404 HTTP status).

### 4. Get product

Depending on a type of the URL parameter, method provides ability to get the product using **`id`** or **`SKU`**.
### ```GET /products/<int:id>```

Get the product using **`id`**.

**Input parameters:**

- **`id`** (integer, **required**, URL parameter)


### ```GET /products/<string:SKU>```

Get the product using **`SKU`**.

**Input parameters:**

- **`SKU`** (string, **required**, URL parameter)

On successful call, both methods **return** the product in the **JSON** format (see "Edit product" section)

If product is not found, methods return corresponding error (404 HTTP status).

### 5. Get products (+ filter)

### ``` GET /products```

Method returns list of products, satisfying filter parameters (if present).

**Input parameters:**

1. **`page`** (integer, optional, URL parameter, default=1)
2. **`type_id`** (integer, optional, URL parameter)
3. **`min_price`** (float, optional, URL parameter)
4. **`max_price`** (float, optional, URL parameter)

Method returns 10 (= `PRODUCTS_PER_PAGE`) products per page. 

Products can be filtered by `type_id` and price range [`min_price`, `max_price`]. If no products satisfy criteria, then empty list is returned (except cases when `page` parameter is not 1 and no items are found, see [SQLAlchemy paginate method](https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/#flask_sqlalchemy.BaseQuery.paginate)).

Example of list returned:
```json
[
   {
      "SKU": "S34QRD",
      "id": 1,
      "name": "RE: Village",
      "price": 1200.0,
      "type_id": 1
   },
   {
      "SKU": "SZS",
      "id": 2,
      "name": "App name",
      "price": 333.0,
      "type_id": 2
   }
]
```

## Testing

In order to run the server (inside a Docker container) one has to clone this repository and use `docker-compose` to build the image and execute the container, using following commands:
```bash
git clone https://github.com/geomPhantom/Products_System_Flask.git
cd Products_System_Flask
docker-compose up
```
