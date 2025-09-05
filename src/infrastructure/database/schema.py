SCHEMA = """
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

DROP FUNCTION IF EXISTS add_product_to_order(uuid, uuid, integer);

CREATE OR REPLACE FUNCTION add_product_to_order(
    p_order_id   UUID,
    p_product_id UUID,
    p_quantity   INTEGER
) RETURNS INTEGER AS $$
DECLARE
    v_stock      INTEGER;
    v_order_item UUID;
BEGIN
    PERFORM 1 FROM orders WHERE id = p_order_id;
    IF NOT FOUND THEN
        RETURN 3;
    END IF;

    SELECT quantity INTO v_stock
    FROM products
    WHERE id = p_product_id
    FOR UPDATE;

    IF NOT FOUND THEN
        RETURN 4;
    END IF;

    IF v_stock < p_quantity THEN
        RETURN 0;
    END IF;

    SELECT id INTO v_order_item
    FROM order_items
    WHERE order_id = p_order_id
      AND product_id = p_product_id
    FOR UPDATE;

    IF FOUND THEN
        UPDATE order_items
        SET quantity = quantity + p_quantity
        WHERE id = v_order_item;

        UPDATE products
        SET quantity = quantity - p_quantity
        WHERE id = p_product_id;

        RETURN 1;
    ELSE
        INSERT INTO order_items (id, order_id, product_id, quantity)
        VALUES (uuid_generate_v4(), p_order_id, p_product_id, p_quantity);

        UPDATE products
        SET quantity = quantity - p_quantity
        WHERE id = p_product_id;

        RETURN 2;
    END IF;
END;
$$ LANGUAGE plpgsql;


CREATE TABLE IF NOT EXISTS categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    parent_id UUID REFERENCES categories(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 0,
    price NUMERIC(12,2) NOT NULL,
    category_id UUID REFERENCES categories(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS clients (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    address TEXT
);

CREATE TABLE IF NOT EXISTS orders (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    client_id UUID NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
    order_date TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS order_items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    order_id UUID NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    product_id UUID NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
    quantity INTEGER NOT NULL CHECK (quantity > 0)
);
"""
