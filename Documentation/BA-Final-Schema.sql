-- Adminer 4.8.1 PostgreSQL 10.23 dump

DROP TABLE IF EXISTS "locations";
DROP SEQUENCE IF EXISTS locations_location_id_seq;
CREATE SEQUENCE locations_location_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."locations" (
    "location_id" integer DEFAULT nextval('locations_location_id_seq') NOT NULL,
    "location_name" character varying(100) NOT NULL,
    CONSTRAINT "locations_pkey" PRIMARY KEY ("location_id")
) WITH (oids = false);


DROP TABLE IF EXISTS "orders";
DROP SEQUENCE IF EXISTS orders_order_id_seq;
CREATE SEQUENCE orders_order_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."orders" (
    "order_id" integer DEFAULT nextval('orders_order_id_seq') NOT NULL,
    "date_time" timestamp NOT NULL,
    "location_id" integer NOT NULL,
    "transaction_total" numeric(10,2) NOT NULL,
    "payment_type_id" integer NOT NULL,
    CONSTRAINT "orders_pkey" PRIMARY KEY ("order_id")
) WITH (oids = false);


DROP TABLE IF EXISTS "orders_products";
CREATE TABLE "public"."orders_products" (
    "order_id" integer NOT NULL,
    "product_id" integer NOT NULL,
    "product_price" numeric(10,2)
) WITH (oids = false);


DROP TABLE IF EXISTS "payment_types";
DROP SEQUENCE IF EXISTS payment_types_payment_type_id_seq;
CREATE SEQUENCE payment_types_payment_type_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."payment_types" (
    "payment_type_id" integer DEFAULT nextval('payment_types_payment_type_id_seq') NOT NULL,
    "payment_name" character varying(10),
    CONSTRAINT "payment_types_pkey" PRIMARY KEY ("payment_type_id")
) WITH (oids = false);


DROP TABLE IF EXISTS "products";
DROP SEQUENCE IF EXISTS products_product_id_seq;
CREATE SEQUENCE products_product_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."products" (
    "product_id" integer DEFAULT nextval('products_product_id_seq') NOT NULL,
    "product_name" character varying(100),
    CONSTRAINT "products_pkey" PRIMARY KEY ("product_id")
) WITH (oids = false);


ALTER TABLE ONLY "public"."orders" ADD CONSTRAINT "orders_location_id_fkey" FOREIGN KEY (location_id) REFERENCES locations(location_id) NOT DEFERRABLE;
ALTER TABLE ONLY "public"."orders" ADD CONSTRAINT "orders_payment_type_id_fkey" FOREIGN KEY (payment_type_id) REFERENCES payment_types(payment_type_id) NOT DEFERRABLE;

ALTER TABLE ONLY "public"."orders_products" ADD CONSTRAINT "orders_products_order_id_fkey" FOREIGN KEY (order_id) REFERENCES orders(order_id) NOT DEFERRABLE;
ALTER TABLE ONLY "public"."orders_products" ADD CONSTRAINT "orders_products_product_id_fkey" FOREIGN KEY (product_id) REFERENCES products(product_id) NOT DEFERRABLE;

-- 2023-05-05 09:54:45.382012+00
