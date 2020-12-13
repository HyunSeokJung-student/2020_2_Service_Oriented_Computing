import pymysql

connection = pymysql.connect(host='0.0.0.0', port=3306, user='root', passwd='humanH34#@', db='tripplan', charset='utf8')

cursor = connection.cursor()

sql = "SELECT 1;"

cursor.execute(sql)

connection.close()