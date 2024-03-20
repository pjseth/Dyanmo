import csv, sqlite3, pandas

name = "road_section_data"
db_name = name+".db"
csv_name = name+".csv"

con = sqlite3.connect(db_name) # change to 'sqlite:///your_filename.db'
cur = con.cursor()
cur.execute("CREATE TABLE t (col1, col2, col3, col4);") # use your column names here

with open(csv_name,'r') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['\ufeffNode'], i['Type'],i['x'],i['y']) for i in dr]

cur.executemany("INSERT INTO t (col1, col2, col3, col4) VALUES (?, ?, ?, ?);", to_db)
con.commit()
con.close()

#df = pandas.read_csv('simplified_diagram_data.csv')
#df.to_sql("simplified_diagram.db", conn, if_exists='append', index=False)