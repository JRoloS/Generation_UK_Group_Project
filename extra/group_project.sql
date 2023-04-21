-- Adminer 4.8.1 PostgreSQL 10.23 dump

DROP TABLE IF EXISTS "locations";
DROP SEQUENCE IF EXISTS location_location_id_seq;
CREATE SEQUENCE location_location_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."locations" (
    "location_id" integer DEFAULT nextval('location_location_id_seq') NOT NULL,
    "location_name" character varying(100) NOT NULL,
    CONSTRAINT "location_pkey" PRIMARY KEY ("location_id")
) WITH (oids = false);

INSERT INTO "locations" ("location_id", "location_name") VALUES
(1,	'Chesterfield'),
(2,	'Leeds');

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

INSERT INTO "orders" ("order_id", "date_time", "location_id", "transaction_total", "payment_type_id") VALUES
(1,	'2021-08-25 09:00:00',	1,	5.20,	2);

DROP TABLE IF EXISTS "orders_products";
CREATE TABLE "public"."orders_products" (
    "order_id" integer NOT NULL,
    "product_id" integer NOT NULL
) WITH (oids = false);

INSERT INTO "orders_products" ("order_id", "product_id") VALUES
(1,	1),
(1,	2);

DROP TABLE IF EXISTS "payment_types";
DROP SEQUENCE IF EXISTS payment_types_payment_id_seq;
CREATE SEQUENCE payment_types_payment_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."payment_types" (
    "payment_type_id" integer DEFAULT nextval('payment_types_payment_id_seq') NOT NULL,
    "payment_name" character varying(10) NOT NULL,
    CONSTRAINT "payment_types_pkey" PRIMARY KEY ("payment_type_id")
) WITH (oids = false);

INSERT INTO "payment_types" ("payment_type_id", "payment_name") VALUES
(1,	'CASH'),
(2,	'CARD');

DROP TABLE IF EXISTS "products";
DROP SEQUENCE IF EXISTS products_product_id_seq;
CREATE SEQUENCE products_product_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "public"."products" (
    "product_id" integer DEFAULT nextval('products_product_id_seq') NOT NULL,
    "product_name" character varying(100) NOT NULL,
    "product_price" numeric(10,2) NOT NULL,
    CONSTRAINT "products_pkey" PRIMARY KEY ("product_id")
) WITH (oids = false);

INSERT INTO "products" ("product_id", "product_name", "product_price") VALUES
(1,	'Regular Flavoured Iced Latte - Hazlenut',	2.75),
(2,	'Large Latte',	2.45);

ALTER TABLE ONLY "public"."orders" ADD CONSTRAINT "orders_location_id_fkey" FOREIGN KEY (location_id) REFERENCES locations(location_id) NOT DEFERRABLE;
ALTER TABLE ONLY "public"."orders" ADD CONSTRAINT "orders_payment_type_id_fkey" FOREIGN KEY (payment_type_id) REFERENCES payment_types(payment_type_id) NOT DEFERRABLE;

ALTER TABLE ONLY "public"."orders_products" ADD CONSTRAINT "orders_products_order_id_fkey" FOREIGN KEY (order_id) REFERENCES orders(order_id) NOT DEFERRABLE;
ALTER TABLE ONLY "public"."orders_products" ADD CONSTRAINT "orders_products_product_id_fkey" FOREIGN KEY (product_id) REFERENCES products(product_id) NOT DEFERRABLE;

-- 2023-04-21 09:49:42.377654+00
