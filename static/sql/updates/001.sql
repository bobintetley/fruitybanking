
-- Add vat flag
ALTER TABLE trx ADD COLUMN vat INTEGER;
UPDATE trx SET vat = 0;

