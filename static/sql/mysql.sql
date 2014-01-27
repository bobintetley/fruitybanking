CREATE DATABASE fruitybanking;
USE fruitybanking;

CREATE TABLE accounts (
	ID int(11) NOT NULL default 0,
	Code varchar(255) NOT NULL default '',
	Description varchar(255) NOT NULL default '',
	Type tinyint(4) NOT NULL default 0,
	Deleted tinyint NOT NULL default 0,
	PRIMARY KEY  (ID),
	UNIQUE KEY IX_AccountsCode (Code)
) Type=MyISAM;

CREATE TABLE trx (
	ID int(11) NOT NULL default 0,
	Date int(11) NOT NULL,
	Description varchar(255) NULL,
	Reconciled tinyint NOT NULL default 0,
	Deleted tinyint NOT NULL default 0,
	Amount double NOT NULL default 0,
	SourceAccountID int(11) NOT NULL,
	DestinationAccountID int(11) NOT NULL,
	PRIMARY KEY  (ID),
	KEY IX_trxSource (SourceAccountID),
	KEY IX_trxDest (DestinationAccountID)
) Type=MyISAM;

