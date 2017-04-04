
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
	PRIMARY KEY (id),
	FOREIGN KEY(kit_type_id) REFERENCES kits.kit_types (id)
);
