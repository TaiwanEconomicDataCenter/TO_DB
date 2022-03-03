USE qnia;
CREATE view qnia_info AS
SELECT databank, name, db_table, db_code, desc_e, desc_c, freq, start, last, unit, name_ord, snl, book, form_e, form_c 
FROM qnia_key;
CREATE view qnia_count AS
SELECT count(*) AS size
FROM qnia_key;

SELECT * FROM qnia_info LIMIT 0, 20;
SELECT * FROM qnia_count;

USE mei;
CREATE view mei_info AS
SELECT databank, name, db_table, db_code, desc_e, desc_c, freq, start, last, unit, name_ord, snl, book, form_e, form_c 
FROM mei_key;
CREATE view mei_count AS
SELECT count(*) AS size
FROM mei_key;

SELECT * FROM mei_info LIMIT 20, 20;
SELECT * FROM mei_count;