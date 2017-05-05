
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


CREATE TABLE kits.order_states (
	id integer,
    name VARCHAR(128),
	description VARCHAR(256),
    type VARCHAR(20),
	PRIMARY KEY (id)
);


CREATE TABLE kits.orders
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    owner_id character varying(36) COLLATE pg_catalog."default",
    created_at timestamptz,
    modified_at timestamptz,
    modified_by character varying(256) COLLATE pg_catalog."default",
    delivery_id character varying(256) COLLATE pg_catalog."default",
    actual_state_id integer,
    PRIMARY KEY (id),
    FOREIGN KEY(actual_state_id) REFERENCES kits.order_states (id)
);


CREATE TABLE kits.order_movements (
	id UUID DEFAULT gen_random_uuid() NOT NULL,
	owner_id VARCHAR(36),
	created_at timestamptz,
    modified_at timestamptz,
	modified_by VARCHAR(256),
    state_id INTEGER,
	order_id UUID,
	PRIMARY KEY (id),
	FOREIGN KEY(state_id) REFERENCES kits.order_states (id),
	FOREIGN KEY(order_id) REFERENCES kits.orders (id)
);



CREATE TABLE kits.order_movements
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    owner_id character varying(36) COLLATE pg_catalog."default",
    created_at timestamptz,
    modified_at timestamptz,
    modified_by character varying(256) COLLATE pg_catalog."default",
    comments character varying(256) COLLATE pg_catalog."default",
    state_id integer,
    order_id uuid,
    CONSTRAINT order_movements_pkey PRIMARY KEY (id),
    CONSTRAINT order_movements_order_id_fkey FOREIGN KEY (order_id)
        REFERENCES kits.orders (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT order_movements_state_id_fkey FOREIGN KEY (state_id)
        REFERENCES kits.order_states (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
);

INSERT INTO kits.order_states(
	id, name, description, type)
	VALUES (1, 'Ready to ship', 'Order sent to shipStation', 'READY_TO_SHIP'),
    		(2, 'On Course', 'Delivery on course', 'ON_COURSE'),
    		(3, 'Delivered', 'Delivery ended', 'DELIVERED'),
    		(4, 'On Hold', 'Order awaiting for something', 'ON_HOLD'),
    		(5, 'Cancelled', 'Order cancelled', 'CANCELLED');