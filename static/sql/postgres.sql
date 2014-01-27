CREATE TABLE accounts (
	ID INT NOT NULL PRIMARY KEY,
	Code VARCHAR(255) NOT NULL,
	Description VARCHAR(255) NOT NULL,
	Type INT NOT NULL,
	Deleted INT NOT NULL
);
CREATE UNIQUE INDEX IX_AccountsCode ON accounts (Code);

CREATE TABLE trx (
	ID INT NOT NULL PRIMARY KEY,
	Date LONG NOT NULL,
	Description VARCHAR(255) NULL,
	Reconciled INT NOT NULL,
	Deleted INT NOT NULL,
	Amount DOUBLE NOT NULL,
	SourceAccountID INT NOT NULL,
	DestinationAccountID INT NOT NULL
);
CREATE INDEX IX_trxSource ON trx (SourceAccountID);
CREATE INDEX IX_trxDest ON trx (DestinationAccountID);

