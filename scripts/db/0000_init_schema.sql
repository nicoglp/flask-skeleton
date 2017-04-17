
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE SCHEMA IF NOT EXISTS kits;

CREATE TABLE kits.kit_type_tests (
	id UUID DEFAULT gen_random_uuid() NOT NULL,
	test VARCHAR(128),
	description TEXT,
	PRIMARY KEY (id)
);

CREATE TABLE kits.kit_type_others (
	id UUID DEFAULT gen_random_uuid() NOT NULL,
	text VARCHAR(128),
	description TEXT,
	PRIMARY KEY (id)
);

CREATE TABLE kits.kit_types (
	id UUID DEFAULT gen_random_uuid() NOT NULL,
	name VARCHAR(128),
	description TEXT,
	kit_type_test_id UUID,
	kit_type_other_id UUID,
	PRIMARY KEY (id),
	FOREIGN KEY(kit_type_test_id) REFERENCES kits.kit_type_tests (id),
	FOREIGN KEY(kit_type_other_id) REFERENCES kits.kit_type_others (id)
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