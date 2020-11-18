import pymysql

class Dao :

    connection = pymysql.connect(host='localhost', port=3306, user='root', passwd='', db='tripplan', charset='utf8')

    def __init__(self):
        pass


    # func 1 : 현재 테이블 tablename의 id 컬럼에 들어가 있는 값 중 가장 큰 id 값 반환
    def select_table_max_id(self, tablename):

        cursor = self.connection.cursor()

        sql = "select MAX(id) from tripplan.{};".format(tablename)
        cursor.execute(sql)

        max_id = cursor.fetchone()[0]

        if max_id is None:
            max_id = -1

        cursor.close()

        return max_id


    # func 2 : 테이블 tablename에 row 1줄 추가
    def insert_data_to_table(self, tablename, name, addr, lat, lng, desc):
        current_id = self.select_table_max_id(tablename) + 1

        cursor = self.connection.cursor()

        sql = 'INSERT INTO {}(id, name, addr, lat, lng, description)' \
              'VALUES({},"{}","{}",{},{},"{}");'.format(tablename, current_id, name, addr, lat, lng, desc)

        cursor.execute(sql)

        cursor.close()


    # func 3 : 테이블 tablename에 list로 받은 data 전부 추가
    def insert_data_list_to_table(self, tablename, name_list, addr_list, lat_list, lng_list, desc_list):

        for i in range(0,len(name_list)):
            self.insert_data_to_table(tablename, name_list[i], addr_list[i], lat_list[i], lng_list[i], desc_list[i])

        self.connection.commit()