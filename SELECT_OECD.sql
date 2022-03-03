USE qnia;
CREATE view qnia_info AS
SELECT databank, name, db_table, db_code, desc_e, desc_c, freq, start, last, unit, name_ord, snl, book, form_e, form_c 
FROM qnia_key;

SELECT * FROM qnia_info LIMIT 0, 20;
SELECT * FROM qnia_info ORDER BY book DESC LIMIT 0, 20;
SELECT * FROM qnia_info ORDER BY form_e LIMIT 0, 20;
SELECT * FROM qnia_info ORDER BY name DESC LIMIT 0, 20;
SELECT * FROM qnia_info ORDER BY desc_e LIMIT 0, 20;
SELECT * FROM qnia_info ORDER BY freq LIMIT 0, 20;
SELECT count(*) AS size FROM qnia_info;

SELECT * FROM qnia_info WHERE name LIKE '%%' AND name LIKE '%%' OR start LIKE '%%' ORDER BY name DESC LIMIT 0, 20;
SELECT count(*) AS size FROM qnia_info  WHERE name LIKE '%%' AND name LIKE '%%' OR start LIKE '%%';

USE mei;
CREATE view mei_info AS
SELECT databank, name, db_table, db_code, desc_e, desc_c, freq, start, last, unit, name_ord, snl, book, form_e, form_c 
FROM mei_key;

SELECT * FROM mei_info LIMIT 20, 20;
SELECT count(*) AS size FROM mei_info;