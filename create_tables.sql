CREATE TABLE `association` (
	`proteins_id`	INTEGER,
	`diseases_id`	INTEGER,
	FOREIGN KEY(`proteins_id`) REFERENCES `proteins`(`id`),
	FOREIGN KEY(`diseases_id`) REFERENCES `diseases`(`id`)
);

CREATE TABLE `diseases` (
	`id`	INTEGER NOT NULL,
	`omim`	VARCHAR NOT NULL,
	PRIMARY KEY(`id`)
);

CREATE TABLE `proteins` (
	`id`	INTEGER NOT NULL,
	`uniprot_accession`	VARCHAR NOT NULL UNIQUE,
	`uniprot_name`	VARCHAR NOT NULL,
	PRIMARY KEY(`id`)
);
