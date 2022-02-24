USE qnia;
SELECT databank, name, db_table, db_code, desc_e, desc_c, freq, start, last, unit, name_ord, snl, book, form_e, form_c 
FROM qnia_key
LIMIT 0,20;

USE mei;
SELECT databank, name, db_table, db_code, desc_e, desc_c, freq, start, last, unit, name_ord, snl, book, form_e, form_c 
FROM mei_key
LIMIT 20,20;