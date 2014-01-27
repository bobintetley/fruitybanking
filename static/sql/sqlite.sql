CREATE TABLE accounts (
	ID INTEGER NOT NULL PRIMARY KEY,
	Code VARCHAR(255) NOT NULL,
	Description VARCHAR(255) NOT NULL,
	Type TINYINT NOT NULL,
	Deleted TINYINT NOT NULL
);
CREATE UNIQUE INDEX IX_AccountsCode ON accounts (Code);

CREATE TABLE trx (
	ID INTEGER NOT NULL PRIMARY KEY,
	Date LONG NOT NULL,
	Description VARCHAR(255) NULL,
	Reconciled TINYINT NOT NULL,
	Deleted TINYINT NOT NULL,
	Amount DOUBLE NOT NULL,
	SourceAccountID INTEGER NOT NULL,
	DestinationAccountID INTEGER NOT NULL
);
CREATE INDEX IX_trxSource ON trx (SourceAccountID);
CREATE INDEX IX_trxDest ON trx (DestinationAccountID);

