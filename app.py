from load_data import LoaderAndParser
from api import API
from flask import Flask
from flask import render_template
from dao import Dao


app = Flask(__name__)
state = "ServerOn"

@app.route("/")
def get_home():
    return render_template("home.html")

@app.route("/api-result")
def get_api_result():
    return render_template("api_result.html")

@app.route("/api-documentation")
def get_api_documentation():
    return render_template("documentation.html")

@app.route("/tripplan/days/<string:days>/between/startTime/<string:startTime>/and/endTime/<string:endTime>")
def get_api_result_window(days, startTime, endTime):
    api = API(days, startTime, endTime)
    return api.returnJSONObject()



if __name__ == "__main__" :

    if state == "ServerOn":
        app.run(host='0.0.0.0',port=5000)

    elif state == "LoadData":
        lp = LoaderAndParser()

        # 관광지 api, 음식점 api 호출 시, 얻은 xml 데이터 원본 불러오기
        raw_data_tour = lp.load_all_raw_data_from_api("tour")
        raw_data_food = lp.load_all_raw_data_from_api("food")

        # 관광지 api, 음식점 api 를 통해 불러온 데이터 가공 처리
        name_list1, addr_list1, lat_list1, lng_list1, desc_list1, section_id_list1 = lp.parse_xml_string(raw_data_tour)
        name_list2, addr_list2, lat_list2, lng_list2, desc_list2, section_id_list2 = lp.parse_xml_string(raw_data_food)

        dao = Dao()

        # 가공 처리한 데이터를 DB에 저장
        dao.insert_data_list_to_table('attractions', name_list1, addr_list1, lat_list1, lng_list1, desc_list1, section_id_list1)
        dao.insert_data_list_to_table('restaurant', name_list2, addr_list2, lat_list2, lng_list2, desc_list2, section_id_list2)

        # 관광지 또는 음식점에서 인접 section_center 까지의 이동 거리, 시간 DB에 저장
        dao.insert_data_to_attractions_near_section()
        dao.insert_data_to_restaurant_near_section()