# TripPlanAPI

import random
import pymysql
import json
import requests

from collections import OrderedDict

class API:

    connection = pymysql.connect(host='0.0.0.0', port=3306, user='root', passwd='humanH34#@', db='tripplan', charset='utf8')

    # variable declaration
    # 실패 0, 성공 1
    code = 1
    # error message & response success
    message = 'response success'
    # 여행 일 수
    days = 0
    # 여행 시작 시간
    startTime = 1100
    # 여행 종료 시간
    endTime = 2059
    # 여행 내 방문한 관광지 수
    totalAttractionsCnt = 0
    # 여행 내 방문한 음식점 수
    totalRestaurantsCnt = 0
    # 전체 이동 거리 (meters)
    totalDistance = 0
    # 전체 이동 시간 (milliseconds)
    totalMoveDuration = 0
    # 전체 관광 시간 (milliseconds)
    totalTourDuration = 0

    # Section, Direction, Attraction, Restaurant
    SDAR = [[0, 0, 0, 0],  # firstDay
            [0, 0, 0, 0],  # secondDay
            [0, 0, 0, 0]]  # thirdDay

    # id, name, lat, lng
    location = [  # firstDay
        [[0],  # Tour1
         [0],  # lunch
         [0],  # Tour2
         [0],  # Tour3
         [0],  # dinner
         [0]],  # Tour4
        # secondDay
        [[0],  # Tour1
         [0],  # lunch
         [0],  # Tour2
         [0],  # Tour3
         [0],  # dinner
         [0]],  # Tour4
        # thirdDay
        [[0],  # Tour1
         [0],  # lunch
         [0],  # Tour2
         [0],  # Tour3
         [0],  # dinner
         [0]]]  # Tour4

    # isStart, distance, duration, departureTime, arrivalTime
    moveInfo = [  # firstDay
        [[0],  # Tour1 - lunch
         [0],  # lunch - Tour2
         [0],  # Tour2 - Tour3
         [0],  # Tour3 - dinner
         [0]],  # dinner - Tour4
        # secondDay
        [[0],  # Tour1 - lunch
         [0],  # lunch - Tour2
         [0],  # Tour2 - Tour3
         [0],  # Tour3 - dinner
         [0]],  # dinner - Tour4
        # thirdDay
        [[0],  # Tour1 - lunch
         [0],  # lunch - Tour2
         [0],  # Tour2 - Tour3
         [0],  # Tour3 - dinner
         [0]]]  # dinner - Tour4

    def __init__(self, days, startTime, endTime):
        self.days = int(days)
        self.startTime = int(startTime)
        self.endTime = int(endTime)

        # Section, Direction, Attraction, Restaurant
        self.SDAR = [[0, 0, 0, 0],  # firstDay
                [0, 0, 0, 0],  # secondDay
                [0, 0, 0, 0]]  # thirdDay

        self.location = [  # firstDay
            [[0],  # Tour1
             [0],  # lunch
             [0],  # Tour2
             [0],  # Tour3
             [0],  # dinner
             [0]],  # Tour4
            # secondDay
            [[0],  # Tour1
             [0],  # lunch
             [0],  # Tour2
             [0],  # Tour3
             [0],  # dinner
             [0]],  # Tour4
            # thirdDay
            [[0],  # Tour1
             [0],  # lunch
             [0],  # Tour2
             [0],  # Tour3
             [0],  # dinner
             [0]]]  # Tour4

        self.moveInfo = [  # firstDay
            [[0],  # Tour1 - lunch
             [0],  # lunch - Tour2
             [0],  # Tour2 - Tour3
             [0],  # Tour3 - dinner
             [0]],  # dinner - Tour4
            # secondDay
            [[0],  # Tour1 - lunch
             [0],  # lunch - Tour2
             [0],  # Tour2 - Tour3
             [0],  # Tour3 - dinner
             [0]],  # dinner - Tour4
            # thirdDay
            [[0],  # Tour1 - lunch
             [0],  # lunch - Tour2
             [0],  # Tour2 - Tour3
             [0],  # Tour3 - dinner
             [0]]]  # dinner - Tour4


    def analyseInput(self):
        if ((self.days == 1) and (self.startTime >= self.endTime)):
            self.code = 0
            self.message = 'Input Form Error'
        elif ((self.startTime % 100 >= 60) and (self.startTime < 1100) and (self.startTime) >= 2000):
            self.code = 0
            self.message = 'StartTime Input Form Error'
        elif ((self.endTime % 100 >= 60) and (self.endTime < 1200) and (self.endTime >= 2100)):
            self.code = 0
            self.message = 'EndTime Input Form Error'
        else:
            if (self.days >= 3):
                self.SDAR[2][2] = 4
                self.SDAR[2][3] = 2
            if (self.days >= 2):
                self.SDAR[1][2] = 4
                self.SDAR[1][3] = 2

            if (self.startTime <= 1200):
                self.SDAR[0][2] += 1
            if (self.startTime <= 1330):
                self.SDAR[0][3] += 1
            if (self.startTime <= 1500):
                self.SDAR[0][2] += 1
            if (self.startTime <= 1700):
                self.SDAR[0][2] += 1
            if (self.startTime <= 1830):
                self.SDAR[0][3] += 1
            if (self.startTime < 2000):
                self.SDAR[0][2] += 1

            if (self.endTime < 2000):
                self.SDAR[self.days-1][2] -= 1
            if (self.endTime < 1830):
                self.SDAR[self.days-1][3] -= 1
            if (self.endTime < 1700):
                self.SDAR[self.days-1][2] -= 1
            if (self.endTime < 1500):
                self.SDAR[self.days-1][2] -= 1
            if (self.endTime < 1330):
                self.SDAR[self.days-1][3] -= 1

            if ((self.SDAR[0][2] <= 0) and (self.SDAR[0][3] <= 0)):
                self.code = 0
                self.message = 'TimeTable & Input mismatch Error'


    def decideDirection(self, today):
        while (True):
            self.SDAR[today][1] = random.randint(1, 4)

            # 이전 section으로 돌아가는 것 방지
            if (self.SDAR[today - 1][1] * self.SDAR[today][1] % 10 == 2):
                continue

            # rows

            # section 1, 2, 3
            if ((self.SDAR[today][0] - 1) // 3 == 0):
                # direction ↓
                if (self.SDAR[today][1] == 2):
                    break

            # section 4, 5, 6
            elif ((self.SDAR[today][0] - 1) // 3 == 1):
                # direction ↑
                if (self.SDAR[today][1] == 1):
                    break
                # direction ↓
                elif (self.SDAR[today][1] == 2):
                    break

            # section 7, 8, 9
            else:
                # direction ↑
                if (self.SDAR[today][1] == 1):
                    break

            # columns

            # section 1, 4, 7
            if ((self.SDAR[today][0] - 1) % 3 == 0):
                # direction →
                if (self.SDAR[today][1] == 4):
                    break

            # section 2, 5, 8
            elif ((self.SDAR[today][0] - 1) % 3 == 1):
                # direction ←
                if (self.SDAR[today][1] == 3):
                    break
                # direction →
                elif (self.SDAR[today][1] == 4):
                    break

            # section 3, 6, 9
            else:
                # direction ←
                if (self.SDAR[today][1] == 3):
                    break


    def decideNextSection(self, today):
        # direction ↑
        if (self.SDAR[today][1] == 1):
            return self.SDAR[today][0] - 3

        # direction ↓
        elif (self.SDAR[today][1] == 2):
            return self.SDAR[today][0] + 3

        # direction ←
        elif (self.SDAR[today][1] == 3):
            return self.SDAR[today][0] - 1

        # direction →
        else:
            return self.SDAR[today][0] + 1


    def isDirectionChanged(self, today):
        if (today == 0):
            return False
        else:
            if (self.SDAR[today - 1][1] == self.SDAR[today][1]):
                return False
            else:
                return True


    def selectAttractions(self, today, isDirectionChanged):
        extraNum = 2

        idList = []
        distanceList = []
        orderedDict = OrderedDict()
        attractionNum = self.SDAR[today][2]

        if (isDirectionChanged):
            attractionNum += extraNum

        cursor = self.connection.cursor()

        # Attractions table에서 attractionNum 개수 만큼 random으로 뽑아 idList에 저장
        sql = "select id from tripplan.attractions where section_id = {} order by RAND() limit {};".format(self.SDAR[today][0], attractionNum)
        cursor.execute(sql)

        for i in range(attractionNum):
            idList.extend(list(cursor.fetchone()))

        # idList에 해당하는 Attraction들과 nextSectionCenter와의 distance를 distanceList에 저장
        for i in range(attractionNum):
            sql = "select distance from tripplan.attractions_near_section where attraction_id = {} and near_section_id = {};".format(idList[i], self.decideNextSection(today))
            cursor.execute(sql)

            distanceList.extend(list(cursor.fetchone()))

        # distance 수치가 큰 순으로 (nextSectionCenter와의 거리가 먼 순으로) idList, distanceList 정렬
        orderedDict.update(zip(idList, distanceList))
        orderedDict = OrderedDict(sorted(orderedDict.items(), key=(lambda x: x[1]), reverse=True))

        idList = list(orderedDict.keys())
        distanceList = list(orderedDict.values())

        if (isDirectionChanged):
            for i in range(extraNum):
                del idList[0]
                del distanceList[0]

        # 당일치기 여행은 제외
        if (self.days == 1):
            # lunch
            if (self.startTime <= 1200):
                if (1 < len(idList)):
                    self.selectRestaurant(today, idList, distanceList, 1, 0, 1)
                else:
                    if (self.endTime >= 1330):
                        self.selectRestaurant(today, idList, distanceList, 1, 0, -1)
                    else:
                        idList.insert(len(idList), 0)
                        distanceList.insert(len(distanceList), 0)

                    idList.insert(len(idList), 0)
                    distanceList.insert(len(distanceList), 0)
            else:
                idList.insert(0, 0)
                distanceList.insert(0, 0)

                if (self.startTime <= 1330):
                    if (1 < len(idList)):
                        self.selectRestaurant(today, idList, distanceList, 1, -1, 1)
                    else:
                        self.selectRestaurant(today, idList, distanceList, 1, -1, -1)

                        idList.insert(len(idList), 0)
                        distanceList.insert(len(distanceList), 0)
                else:
                    idList.insert(0, 0)
                    distanceList.insert(0, 0)

            # dinner
            if (self.startTime <= 1500):
                if (4 < len(idList)):
                    self.selectRestaurant(today, idList, distanceList, 4, 3, 4)
                else:
                    if (3 < len(idList)):
                        if (self.endTime >= 1830):
                            self.selectRestaurant(today, idList, distanceList, 4, 3, -1)
                        else:
                            idList.insert(len(idList), 0)
                            distanceList.insert(len(distanceList), 0)
                    else:
                        idList.insert(len(idList), 0)
                        distanceList.insert(len(distanceList), 0)

                    idList.insert(len(idList), 0)
                    distanceList.insert(len(distanceList), 0)
            else:
                idList.insert(0, 0)
                distanceList.insert(0, 0)

                if (self.startTime <= 1700):
                    if (4 < len(idList)):
                        self.selectRestaurant(today, idList, distanceList, 4, 3, 4)
                    else:
                        if (self.endTime >= 1830):
                            self.selectRestaurant(today, idList, distanceList, 4, 3, -1)
                        else:
                            idList.insert(len(idList), 0)
                            distanceList.insert(len(distanceList), 0)

                    idList.insert(len(idList), 0)
                    distanceList.insert(len(distanceList), 0)
                else:
                    idList.insert(0, 0)
                    distanceList.insert(0, 0)

                    if (self.startTime <= 1830):
                        if (4 < len(idList)):
                            self.selectRestaurant(today, idList, distanceList, 4, -1, 4)
                        else:
                            self.selectRestaurant(today, idList, distanceList, 4, -1, -1)

                            idList.insert(len(idList), 0)
                            distanceList.insert(len(distanceList), 0)
                    else:
                        idList.insert(0, 0)
                        distanceList.insert(0, 0)

        else:
            # startDay
            if (today == 0):
                # lunch
                if (self.startTime <= 1200):
                    self.selectRestaurant(today, idList, distanceList, 1, 0, 1)
                else:
                    idList.insert(0, 0)
                    distanceList.insert(0, 0)

                    if (self.startTime <= 1330):
                        self.selectRestaurant(today, idList, distanceList, 1, -1, 1)
                    else:
                        idList.insert(0, 0)
                        distanceList.insert(0, 0)

                # dinner
                if (self.startTime <= 1500):
                    self.selectRestaurant(today, idList, distanceList, 4, 3, 4)
                else:
                    idList.insert(0, 0)
                    distanceList.insert(0, 0)

                    if (self.startTime <= 1700):
                        self.selectRestaurant(today, idList, distanceList, 4, 3, 4)
                    else:
                        idList.insert(0, 0)
                        distanceList.insert(0, 0)

                        if (self.startTime <= 1830):
                            self.selectRestaurant(today, idList, distanceList, 4, -1, 4)
                        else:
                            idList.insert(0, 0)
                            distanceList.insert(0, 0)

            # endDay
            elif (today == self.days-1):
                # dinner
                if (self.endTime >= 2000):
                    self.selectRestaurant(today, idList, distanceList, 3, 2, 3)
                else:
                    idList.insert(len(idList), 0)
                    distanceList.insert(len(distanceList), 0)

                    if (self.endTime >= 1830):
                        self.selectRestaurant(today, idList, distanceList, 3, 2, -1)
                    else:
                        idList.insert(len(idList), 0)
                        distanceList.insert(len(distanceList), 0)

                # lunch
                if (self.endTime >= 1700):
                    self.selectRestaurant(today, idList, distanceList, 1, 0, 1)
                else:
                    idList.insert(len(idList), 0)
                    distanceList.insert(len(distanceList), 0)

                    if (self.endTime >= 1500):
                        self.selectRestaurant(today, idList, distanceList, 1, 0, 1)
                    else:
                        idList.insert(len(idList), 0)
                        distanceList.insert(len(distanceList), 0)

                        if (self.endTime >= 1330):
                            self.selectRestaurant(today, idList, distanceList, 1, 0, -1)
                        else:
                            idList.insert(len(idList), 0)
                            distanceList.insert(len(distanceList), 0)

            # secondDay
            else:
                # lunch
                self.selectRestaurant(today, idList, distanceList, 1, 0, 1)
                # dinner
                self.selectRestaurant(today, idList, distanceList, 4, 3, 4)

        # 완성된 idList를 location ID값에 대입
        for i in range(6):
            self.location[today][i][0] = idList[i]

        for day in range(3):
            for i in range(6):
                if (self.location[day][i][0]):
                    if ((i == 1) or (i == 4)):
                        sql = "select name, lat, lng from tripplan.restaurant where id = {};".format(self.location[day][i][0])
                        cursor.execute(sql)
                    else:
                        sql = "select name, lat, lng from tripplan.attractions where id = {};".format(self.location[day][i][0])
                        cursor.execute(sql)

                    self.location[day][i].extend(list(cursor.fetchone()))

        cursor.close()


    def selectRestaurant(self, today, idList, distanceList, index, farIndex, closeIndex): # farIndex, closeIndex 中 emptyIndex = -1

        cursor = self.connection.cursor()

        far = distanceList[farIndex]
        close = distanceList[closeIndex]

        if (farIndex == -1):
            far = 199999
        if (closeIndex == -1):
            close = 10000

        sqlResult = None

        while (sqlResult == None):
            sql = "select restaurant_id, distance from tripplan.restaurant_near_section where (this_section_id = {}) and (near_section_id = {}) and (distance between {} and {}) order by RAND() limit 1;".format(self.SDAR[today][0], self.decideNextSection(today), close, far)
            cursor.execute(sql)

            far += 100
            close -= 100

            sqlResult = cursor.fetchone()

        idList.insert(index, list(sqlResult)[0])
        distanceList.insert(index, list(sqlResult)[1])

        cursor.close()


    def getDistance(self, startX, startY, goalX, goalY):
        headers = {
            'X-NCP-APIGW-API-KEY-ID': 'rpqkw9qi0l',
            'X-NCP-APIGW-API-KEY': 'VayHSWv7FXwMGnsIwMRdK7tnGmLu4rO1NUhhsofF',
        }

        start = startX + ',' + startY
        goal = goalX + ',' + goalY

        params = (
            ('start', start),
            ('goal', goal),
            ('option', 'trafast'),
        )

        response = requests.get('https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving',
                                headers=headers, params=params)

        JSONObject = json.loads(response.text)

        return JSONObject['route']['trafast'][0]['summary']['distance']


    def makeSummary(self):
        for day in range(3):    # days
            for i in range(6):  # location
                if (self.location[day][i][0]):
                    if ((i == 1) or (i == 4)):
                        self.totalRestaurantsCnt += 1
                    else:
                        self.totalAttractionsCnt += 1
            for i in range(5):  # moveInfo
                if (self.moveInfo[day][i][0]):
                    self.totalDistance += self.moveInfo[day][i][1]
                    self.totalMoveDuration += self.moveInfo[day][i][2]

        totalDuration = 0
        #if (self.days == 1):
        #    totalDuration += (self.endTime - self.startTime)
        #else:
        #    if (days == 2):
        #        totalDuration += 1000
        #    totalDuration += (2100 - self.startTime)
        #    totalDuration += (self.endTime - 1100)

        #self.totalTourDuration = totalDuration - self.totalMoveDuration
        # 시간으로 바꿔주기

        summary = {
            'days': self.days,
            'totalAttractionsCnt': self.totalAttractionsCnt,
            'totalRestaurantsCnt': self.totalRestaurantsCnt,
            'totalDistance': self.totalDistance,
            'totalMoveDuration': self.totalMoveDuration,
            'totalTourDuration': self.totalTourDuration
        }
        return summary


    def makeTripPlan(self):
        tripplan = []

        for today in range(self.days):
            dict = {
                'day': today + 1,
                'section': self.SDAR[today][0]
            }
            tripplan.append(dict)

        return tripplan


    def returnJSONObject(self):

        # Input analyse
        self.analyseInput()

        # response 뼈대
        response = {
            'code': self.code,
            'message': self.message
        }

        # Input에 문제가 없다면
        if (self.code):
            # 첫째 날 section 랜덤으로 결정
            self.SDAR[0][0] = random.randint(1, 9)

            # days만큼 반복
            for today in range(self.days):

                # direction 랜덤으로 결정
                self.decideDirection(today)

                if (today != 2):
                    # 정해진 direction을 바탕으로 다음 날 section 결정
                    self.SDAR[today + 1][0] = self.decideNextSection(today)

                # Attractions select
                self.selectAttractions(today, self.isDirectionChanged(today))

            # 최종 response
            response['result'] = {
                'summary': self.makeSummary(),
                'tripplan': self.makeTripPlan(),
                # test
                'test': self.location
            }

        JSONObject = json.dumps(response, ensure_ascii=False, indent=4, separators=(', ', ': '))

        return JSONObject