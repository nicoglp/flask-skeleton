
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE SCHEMA IF NOT EXISTS kits;

CREATE TABLE kits.kit_types (
	id UUID DEFAULT gen_random_uuid() NOT NULL,
	name VARCHAR(128),
	description TEXT,
	PRIMARY KEY (id)
);

CREATE TABLE kits.kits (
	id UUID DEFAULT gen_random_uuid() NOT NULL,
	owner_id VARCHAR(36),
	created_at TIMESTAMP WITHOUT TIME ZONE,
	modified_at TIMESTAMP WITHOUT TIME ZONE,
	modified_by VARCHAR(256),
    kit_type_id UUID,
	barcode VARCHAR(32),
	registered TIMESTAMP WITHOUT TIME ZONE,
	delivery_status VARCHAR(32),
	order_id UUID,
	PRIMARY KEY (id),
	FOREIGN KEY(kit_type_id) REFERENCES kits.kit_types (id)
);

CREATE TABLE kits.orders
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    owner_id character varying(36) COLLATE pg_catalog."default",
    created_at timestamp without time zone,
    modified_at timestamp without time zone,
    modified_by character varying(256) COLLATE pg_catalog."default",
    delivery_id character varying(256) COLLATE pg_catalog."default",
    actual_state_id UUID,
    CONSTRAINT orders_pkey PRIMARY KEY (id)
);

CREATE TABLE kits.order_states (
	id uuid NOT NULL DEFAULT gen_random_uuid(),
    name VARCHAR(128),
	description VARCHAR(256),
    type VARCHAR(20),
	PRIMARY KEY (id)
);

CREATE TABLE kits.order_movements (
	id UUID DEFAULT gen_random_uuid() NOT NULL,
	owner_id VARCHAR(36),
	created_at TIMESTAMP WITHOUT TIME ZONE,
	modified_at TIMESTAMP WITHOUT TIME ZONE,
	modified_by VARCHAR(256),
    comments VARCHAR(256),
    state_id UUID,
	order_id UUID,
	PRIMARY KEY (id),
	FOREIGN KEY(state_id) REFERENCES kits.order_states (id),
	FOREIGN KEY(order_id) REFERENCES kits.orders (id)
);