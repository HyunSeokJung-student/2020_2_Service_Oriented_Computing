import requests
import re
import xml.etree.ElementTree as ET



class LoaderAndParser :


    def __init__(self):
        pass


    # func 1 : 데이터 API에서 불러오기
    def load_all_raw_data_from_api(self, mode):
        req_item_list_url ="http://tour.chungnam.go.kr/_prog/openapi/?func="

        # API 파라미터를 위해 첫번째 아이템 번호, 마지막 아이템 번호 설정
        first_item_num = 1
        last_item_num = self.get_total_item_cnt(mode)

        # 데이터 요청 url
        req_item_list_url = req_item_list_url + mode \
                            + "&start=" + str(first_item_num) + "&end=" + str(last_item_num)

        req = requests.get(req_item_list_url)

        return req.text


    # func 2 : 아이템 전체 수 구하기
    def get_total_item_cnt(self, mode):
        item_cnt_url = ""

        # 데이터 불러오기 위한 API 파라미터 값 결정 : 총 데이터(아이템) 수
        # 1. 관광 명소 데이터 전체 수
        if mode == "tour":
            item_cnt_url = "http://tour.chungnam.go.kr/_prog/openapi/?func=tour&mode=getCnt"
        # 2. 음식점 데이터 전체 수
        elif mode == "food":
            item_cnt_url = "http://tour.chungnam.go.kr/_prog/openapi/?func=food&mode=getCnt"
        # 3. 그 외
        else:
            return "Error : value of \"mode\" is not corrected!!"

        req_item_cnt = requests.get(item_cnt_url)
        item_cnt = int(re.sub('<.+?>', '', req_item_cnt.text, 0, re.I|re.S))

        return item_cnt


    # func 3 : String으로 읽어온 데이터를 DB에 넣을 수 있게 컬럼별로 리스트에 저장
    def parse_xml_string(self, raw_data):

        essential_data = self.remove_particular_tag_char(raw_data)

        parser = ET.XMLParser(encoding="utf-8")

        string = ET.fromstring(essential_data, parser=parser)
        tree = ET.ElementTree(string)
        root = tree.getroot()

        item_list = root.findall('item')

        name_list = []
        addr_list = []
        lat_list = []
        lng_list = []
        desc_list = []

        for item in item_list:
            item_name = item.find('nm').text
            item_addr = item.find('addr').text
            item_lat = item.find('lat').text
            item_lng = item.find('lng').text
            item_desc = item.find('desc').text

            # 비어 있는 값이 없는 데이터만 취급 ( 총 544개 중 542개 처리 )
            if(item_name is not None and item_addr is not None and item_lat is not None and item_lng is not None and item_desc is not None):
                name_list.append(str(item_name).replace(" 사진X","").replace(" 사진x",""))
                addr_list.append(str(item_addr))
                lat_list.append(float(item_lat))
                lng_list.append(float(item_lng))
                desc_list.append(re.sub(pattern='<[^/]*>', repl='', string=str(item.find('desc').text)).replace("\"","'"))

        return name_list, addr_list, lat_list, lng_list, desc_list


    # func 4 : 일부 특정 태그, 문자 제거
    def remove_particular_tag_char(self, raw_data):

        removed_char_data = raw_data.replace("", "")
        removed_char_data = removed_char_data.replace(" ", "")
        removed_char_data = removed_char_data.replace("&nbsp;", "")
        removed_char_data = removed_char_data.replace("<div>","").replace("</div>","")
        removed_char_data = removed_char_data.replace("<p>", "").replace("</p>", "")
        removed_char_data = removed_char_data.replace("<br>", "")

        result = removed_char_data

        return result