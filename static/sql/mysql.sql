CREATE DATABASE fruitybanking;
USE fruitybanking;

CREATE TABLE accounts (
	id int(11) NOT NULL default 0,
	code varchar(255) NOT NULL default '',
	description varchar(255) NOT NULL default '',
	type tinyint(4) NOT NULL default 0,
	deleted tinyint NOT NULL default 0,
	PRIMARY KEY  (id),
	UNIQUE KEY IX_AccountsCode (code)
);

CREATE TABLE trx (
	id int(11) NOT NULL default 0,
	date int(11) NOT NULL,
	description varchar(255) NULL,
	reconciled tinyint NOT NULL default 0,
    vat tinyint NOT NULL default 0,
	deleted tinyint NOT NULL default 0,
	amount integer NOT NULL default 0,
	sourceaccountid int(11) NOT NULL,
	destinationaccountid int(11) NOT NULL,
	PRIMARY KEY  (id),
	KEY IX_trxSource (sourceaccountid),
	KEY IX_trxDest (destinationaccountid)
);

