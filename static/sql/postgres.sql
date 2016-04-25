CREATE TABLE accounts (
	id INTEGER NOT NULL PRIMARY KEY,
	code VARCHAR(255) NOT NULL,
	description VARCHAR(255) NOT NULL,
	type INTEGER NOT NULL,
	deleted INTEGER NOT NULL
);
CREATE UNIQUE INDEX IX_AccountsCode ON accounts (code);

CREATE TABLE trx (
	id INTEGER NOT NULL PRIMARY KEY,
	date INTEGER NOT NULL,
	description VARCHAR(255) NULL,
	reconciled INTEGER NOT NULL,
	deleted INTEGER NOT NULL,
	amount INTEGER NOT NULL,
	sourceaccountid INTEGER NOT NULL,
	destinationaccountid INTEGER NOT NULL
);
CREATE INDEX IX_trxSource ON trx (sourceaccountid);
CREATE INDEX IX_trxDest ON trx (destinationaccountid);

