SELECT db_table FROM us.us_key GROUP BY db_table ORDER BY db_table;
SELECT count(*) AS shape FROM qnia.qnia_key;
SELECT min(start) AS earliest FROM qnia.qnia_key;
SELECT count(*) AS shape FROM mei.mei_key;
SELECT min(start) AS earliest FROM mei.mei_key;
SELECT count(*) AS shape FROM gerfin.gerfin_key;
SELECT min(start) AS earliest FROM gerfin.gerfin_key;
SELECT count(*) AS shape FROM gerfin.db_d_0001;
SELECT count(*) AS shape FROM forex.forex_key;
SELECT min(start) AS earliest FROM forex.forex_key;
SELECT count(*) AS shape FROM us.us_key;
SELECT min(start) AS earliest FROM us.us_key;
SELECT min(start) AS earliest FROM us.us_key WHERE freq='W';
SELECT count(*) AS shape FROM intline.intline_key;
SELECT min(start) AS earliest FROM intline.intline_key;
SELECT min(start) AS earliest FROM intline.intline_key WHERE freq='W';
SELECT count(*) AS shape FROM asia.asia_key;
SELECT min(start) AS earliest FROM asia.asia_key;
SELECT min(start) AS earliest FROM asia.asia_key WHERE freq='W';
SELECT * FROM qnia.qnia_key;
SELECT * FROM mei.mei_key;
SELECT * FROM gerfin.gerfin_key;
SELECT * FROM forex.forex_key;
SELECT * FROM us.us_key;
SELECT * FROM intline.intline_key;
SELECT * FROM asia.asia_key WHERE name='M158MHLEI1.M';
DESC qnia.qnia_key;

/*backup*/
/*source C:/Users/user/Desktop/MEI202201.sql;*/