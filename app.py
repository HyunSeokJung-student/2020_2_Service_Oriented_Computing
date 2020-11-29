from load_data import LoaderAndParser
from dao import Dao
from flask import Flask
from flask import render_template



app = Flask(__name__)
state = "ServerOn"

@app.route("/")
def get_home():
    return render_template("home.html")
    # return render_template("home.html")

@app.route("/api-result")
def get_api_result():
    return render_template("api_result.html")

@app.route("/api-documentation")
def get_api_documentation():
    return render_template("documentation.html")

@app.route("/tripplan/days/<string:days>/startTime/<string:startTime>/endTime/<string:endTime>")
def get_api_result_window(days, startTime, endTime):
    return "<h1>days: %s<h1><br>" % days + "<h1>startTime: %s<h1><br>" % startTime\
           + "<h1>endTime: %s<h1>" % endTime



if __name__ == "__main__" :

    if state == "ServerOn":
        app.run(host='0.0.0.0',port=8000)

    elif state == "LoadData":
        lp = LoaderAndParser()
        raw_data_tour = lp.load_all_raw_data_from_api("tour")
        raw_data_food = lp.load_all_raw_data_from_api("food")

        name_list1, addr_list1, lat_list1, lng_list1, desc_list1 = lp.parse_xml_string(raw_data_tour)
        name_list2, addr_list2, lat_list2, lng_list2, desc_list2 = lp.parse_xml_string(raw_data_food)

        dao = Dao()
        dao.insert_data_list_to_table('attractions',name_list1, addr_list1, lat_list1, lng_list1, desc_list1)
        dao.insert_data_list_to_table('restaurant', name_list2, addr_list2, lat_list2, lng_list2, desc_list2)