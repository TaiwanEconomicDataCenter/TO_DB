SELECT db_table FROM us.us_key GROUP BY db_table ORDER BY db_table;
SELECT count(*) AS shape FROM qnia.qnia_key;
SELECT min(start) AS earliest FROM qnia.qnia_key;
SELECT max(last) FROM qnia.qnia_key WHERE freq='Q';
SELECT count(*) AS shape FROM mei.mei_key;
SELECT min(start) AS earliest FROM mei.mei_key;
SELECT max(last) FROM mei.mei_key WHERE freq='M';
SELECT count(*) AS shape FROM gerfin.gerfin_key;
SELECT min(start) AS earliest FROM gerfin.gerfin_key;
SELECT max(last) FROM gerfin.gerfin_key;
SELECT count(*) AS shape FROM gerfin.db_d_0001;
SELECT count(*) AS shape FROM forex.forex_key;
SELECT min(start) AS earliest FROM forex.forex_key;
SELECT max(last) FROM forex.forex_key WHERE freq='W';
SELECT count(*) AS shape FROM us.us_key;
SELECT min(start) AS earliest FROM us.us_key;
SELECT min(start) AS earliest FROM us.us_key WHERE freq='W';
SELECT max(last) FROM us.us_key WHERE freq='W';
SELECT count(*) AS shape FROM intline.intline_key;
SELECT min(start) AS earliest FROM intline.intline_key;
SELECT max(last) FROM intline.intline_key WHERE freq='D';
/*SELECT min(start) AS earliest FROM intline.intline_key WHERE freq='W';*/
SELECT min(intline.intline_key.start) AS earliest FROM intline.intline_key 
LEFT JOIN asia.asia_key
ON intline.intline_key.name=asia.asia_key.name
WHERE asia.asia_key.databank is null AND intline.intline_key.freq='W';
SELECT count(*) AS shape FROM asia.asia_key;
SELECT min(start) AS earliest FROM asia.asia_key;
SELECT min(start) AS earliest FROM asia.asia_key WHERE freq='W';
SELECT max(last) FROM asia.asia_key WHERE freq='D';
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