import pymysql
import json
import requests

class Dao :

    connection = None

    def __init__(self):
        self.connection = pymysql.connect(host='0.0.0.0', port=3306, user='root', passwd='humanH34#@', db='tripplan',
                                     charset='utf8')




    # func 1 : 현재 테이블 tablename의 id 컬럼에 들어가 있는 값 중 가장 큰 id 값 반환
    def select_table_max_id(self, tablename):

        self.connection.ping(True)

        cursor = self.connection.cursor()

        sql = "select MAX(id) from tripplan.{};".format(tablename)

        cursor.execute(sql)

        max_id = cursor.fetchone()[0]

        if max_id is None:
            max_id = 0

        cursor.close()

        return max_id


    # func 2 : 테이블 tablename (attractions || restaurant) 에 row 1줄 추가
    def insert_data_to_table(self, tablename, name, addr, lat, lng, desc, section_id):
        current_id = self.select_table_max_id(tablename) + 1

        self.connection.ping(True)

        cursor = self.connection.cursor()

        sql = 'INSERT INTO {}(id, name, addr, lat, lng, description, section_id)' \
              'VALUES({},"{}","{}",{},{},"{}",{});'.format(tablename, current_id, name, addr, lat, lng, desc, section_id)

        cursor.execute(sql)

        cursor.close()


    # func 3 : 테이블 tablename (attractions || restaurant) 에 list로 받은 data 전부 추가
    def insert_data_list_to_table(self, tablename, name_list, addr_list, lat_list, lng_list, desc_list, section_id_list):

        for i in range(0,len(name_list)):
            self.insert_data_to_table(tablename, name_list[i], addr_list[i], lat_list[i], lng_list[i],
                                      desc_list[i], section_id_list[i])

        self.connection.commit()

    # func 4 : 테이블 attractions_near_section 에 인접 section의 center 와 현재 관광지(attraction) 까지의 이동 거리와 시간 입력
    def insert_data_to_attractions_near_section(self):
        self.connection.ping(True)

        cursor_select = self.connection.cursor()

        sql_select = 'select att_ne.attraction_id, att_ne.attraction_section_id, att_ne.attraction_lat, att_ne.attraction_lng, att_ne.near_section_id, s.section_center_lat, s.section_center_lng ' \
                     'from section s,(select att.id as attraction_id, att.section_id as attraction_section_id, att.lat as attraction_lat, att.lng as attraction_lng, ne.near_section_id as near_section_id from attractions att , near_section ne where att.section_id = ne.section_id)' \
                     ' att_ne where s.section_id = att_ne.near_section_id ;'

        cursor_select.execute(sql_select)


        while True:
            row = cursor_select.fetchone()
            if row is None:
                break
            # row[0] : attraction_id
            # row[1] : attraction_section_id
            # row[2] : attraction_lat
            # row[3] : attraction_lng
            # row[4] : near_section_id
            # row[5] : section_center_lat
            # row[6] : section_center_lng

            cursor_duplicate_check = self.connection.cursor()
            sql_duplicate_check = 'select * from attractions_near_section;'
            cursor_duplicate_check.execute(sql_duplicate_check)

            duplicate_check = False

            while True:
                row_duplicate_check = cursor_duplicate_check.fetchone()
                if row_duplicate_check is None:
                    break
                if (row_duplicate_check[0]==row[0]) and (row_duplicate_check[2]== row[4]):
                    duplicate_check = True
                    break

            if (not duplicate_check) :
                headers = {
                    'X-NCP-APIGW-API-KEY-ID': 'rpqkw9qi0l',
                    'X-NCP-APIGW-API-KEY': 'VayHSWv7FXwMGnsIwMRdK7tnGmLu4rO1NUhhsofF',
                }

                start = str(row[3]) + ',' + str(row[2])
                goal = str(row[6]) + ',' + str(row[5])

                params = (
                    ('start', start),
                    ('goal', goal),
                    ('option', 'trafast'),
                )

                response = requests.get('https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving', headers=headers, params=params)

                jo = json.loads(response.text)

                distance = int(jo['route']['trafast'][0]['summary']['distance'])
                duration = int(jo['route']['trafast'][0]['summary']['duration'])

                cursor_insert = self.connection.cursor()

                sql_insert = 'INSERT INTO attractions_near_section(attraction_id,this_section_id,near_section_id,distance,duration) ' \
                             'VALUES({},{},{},{},{});'.format(row[0],row[1],row[4],distance,duration)

                cursor_insert.execute(sql_insert)

                self.connection.commit()

    # func 5 : 테이블 restaurant_near_section 에 인접 section의 center 와 현재 음식점(restaurant) 까지의 이동 거리와 시간 입력
    def insert_data_to_restaurant_near_section(self):
        self.connection.ping(True)

        cursor_select = self.connection.cursor()

        sql_select = 'select restaurant_ne.restaurant_id, restaurant_ne.restaurant_section_id, restaurant_ne.restaurant_lat, restaurant_ne.restaurant_lng, restaurant_ne.near_section_id, s.section_center_lat, s.section_center_lng ' \
                     'from section s,(select res.id as restaurant_id, res.section_id as restaurant_section_id, res.lat as restaurant_lat, res.lng as restaurant_lng, ne.near_section_id as near_section_id from restaurant res , near_section ne where res.section_id = ne.section_id)' \
                     ' restaurant_ne where s.section_id = restaurant_ne.near_section_id ;'

        cursor_select.execute(sql_select)

        while True:
            row = cursor_select.fetchone()
            if row is None:
                break
            # row[0] : restaurant_id
            # row[1] : restaurant_section_id
            # row[2] : restaurant_lat
            # row[3] : restaurant_lng
            # row[4] : near_section_id
            # row[5] : section_center_lat
            # row[6] : section_center_lng

            cursor_duplicate_check = self.connection.cursor()
            sql_duplicate_check = 'select * from restaurant_near_section;'
            cursor_duplicate_check.execute(sql_duplicate_check)

            duplicate_check = False

            while True:
                row_duplicate_check = cursor_duplicate_check.fetchone()
                if row_duplicate_check is None:
                    break
                if (row_duplicate_check[0] == row[0]) and (row_duplicate_check[2] == row[4]):
                    duplicate_check = True
                    break

            if (not duplicate_check):
                headers = {
                    'X-NCP-APIGW-API-KEY-ID': 'rpqkw9qi0l',
                    'X-NCP-APIGW-API-KEY': 'VayHSWv7FXwMGnsIwMRdK7tnGmLu4rO1NUhhsofF',
                }

                start = str(row[3]) + ',' + str(row[2])
                goal = str(row[6]) + ',' + str(row[5])

                params = (
                    ('start', start),
                    ('goal', goal),
                    ('option', 'trafast'),
                )

                response = requests.get('https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving',
                                        headers=headers, params=params)

                jo = json.loads(response.text)

                distance = int(jo['route']['trafast'][0]['summary']['distance'])
                duration = int(jo['route']['trafast'][0]['summary']['duration'])

                cursor_insert = self.connection.cursor()

                sql_insert = 'INSERT INTO restaurant_near_section(restaurant_id,this_section_id,near_section_id,distance,duration) ' \
                             'VALUES({},{},{},{},{});'.format(row[0], row[1], row[4], distance, duration)

                cursor_insert.execute(sql_insert)

                self.connection.commit()