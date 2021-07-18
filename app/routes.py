from app import app, db
from models import Product, serialize
from flask import jsonify, request, make_response
from sqlalchemy import exc

PRODUCTS_PER_PAGE = 10


@app.route('/products', methods=['POST'])
def create_product():
    params = request.json
    if params and ('SKU' in params) and ('name' in params) and ('type_id' in params) and ('price' in params):
        p = Product(SKU=params['SKU'], name=params['name'], type_id=params['type_id'], price=params['price'])
        try:
            db.session.add(p)
            db.session.flush()
            db.session.refresh(p)
            db.session.commit()
            return jsonify({'id': p.id}), 201
        except exc.SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return make_response(jsonify({'Error': error}), 400)
    else:
        return make_response(jsonify({'Error': 'Not all parameters present'}), 400)


def edit_product(is_by_id, input_params, supported_params, id_or_sku):
    if input_params:
        try:
            if is_by_id:
                p = Product.query.get(id_or_sku)
            else:
                p = Product.query.filter_by(SKU=id_or_sku).first()

            if p is None:
                return make_response(jsonify({'Error': 'Product with specified id/SKU is not found'}), 404)
            else:
                for param in supported_params:
                    if param in input_params:
                        setattr(p, param, input_params[param])
                db.session.commit()
                if is_by_id:
                    return jsonify(serialize(Product.query.get(id)))
                else:
                    return jsonify(serialize(Product.query.filter_by(SKU=id_or_sku).first()))
        except exc.SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return make_response(jsonify({'Error': error}), 400)
    else:
        return make_response(jsonify({'Error': 'Empty parameters data'}), 400)


@app.route('/products/<int:id>', methods=['PUT'])
def edit_product_by_id(id):
    return edit_product(True, request.json, ['SKU', 'name', 'type_id', 'price'], id)


@app.route('/products/<string:sku>', methods=['PUT'])
def edit_product_by_sku(sku):
    return edit_product(False, request.json, ['name', 'type_id', 'price'], sku)


def delete_product(is_by_id, id_or_sku):
    try:
        if is_by_id:
            p = Product.query.get(id_or_sku)
        else:
            p = Product.query.filter_by(SKU=id_or_sku).first()

        if p is None:
            return make_response(jsonify({'Error': 'Product with specified id/SKU is not found'}), 404)
        else:
            db.session.delete(p)
            db.session.commit()
            return jsonify({'Result': 'Product successfully deleted'})
    except exc.SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return make_response(jsonify({'Error': error}), 400)


@app.route('/products/<int:id>', methods=['DELETE'])
def delete_product_by_id(id):
    return delete_product(True, id)


@app.route('/products/<string:sku>', methods=['DELETE'])
def delete_product_by_sku(sku):
    return delete_product(False, sku)


def get_product(p, param_type):
    if p is None:
        return make_response(jsonify({'Error': 'Product with specified ' + param_type + ' is not found'}), 404)
    else:
        return jsonify(serialize(p))


@app.route('/products/<int:id>', methods=['GET'])
def get_product_by_id(id):
    p = Product.query.get(id)
    return get_product(p, 'id')


@app.route('/products/<string:sku>', methods=['GET'])
def get_product_by_sku(sku):
    p = Product.query.filter_by(SKU=sku).first()
    return get_product(p, 'SKU')


@app.route('/products', methods=['GET'])
def get_products_page():
    page = request.args.get('page', type=int, default=1)
    type_id = request.args.get('type_id', type=int, default=0)
    min_price = request.args.get('min_price', type=float, default=0.0)
    max_price = request.args.get('max_price', type=float, default=0.0)

    are_filters_used = type_id != 0 or min_price != 0 or max_price != 0

    if are_filters_used:
        filtered_products = Product.query
        if type_id != 0:
            filtered_products = filtered_products.filter(Product.type_id == type_id)
        if min_price != 0:
            filtered_products = filtered_products.filter(Product.price >= min_price)
        if max_price != 0:
            filtered_products = filtered_products.filter(Product.price <= max_price)
        filtered_products = filtered_products.paginate(page, PRODUCTS_PER_PAGE).items
        return jsonify([serialize(product) for product in filtered_products])
    else:
        products = Product.query.paginate(page, PRODUCTS_PER_PAGE).items
        return jsonify([serialize(product) for product in products])

