CREATE TABLE accounts (
	id INTEGER NOT NULL PRIMARY KEY,
	code VARCHAR(255) NOT NULL,
	description VARCHAR(255) NOT NULL,
	type TINYINT NOT NULL,
	deleted TINYINT NOT NULL
);
CREATE UNIQUE INDEX IX_AccountsCode ON accounts (code);

CREATE TABLE trx (
	id INTEGER NOT NULL PRIMARY KEY,
	date LONG NOT NULL,
	description VARCHAR(255) NULL,
	reconciled TINYINT NOT NULL,
	deleted TINYINT NOT NULL,
	amount DOUBLE NOT NULL,
	sourceaccountid INTEGER NOT NULL,
	destinationaccountid INTEGER NOT NULL
);
CREATE INDEX IX_trxSource ON trx (sourceaccountid);
CREATE INDEX IX_trxDest ON trx (destinationaccountid);

