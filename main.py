import pymongo
from flask import Flask, render_template
import folium
from folium.plugins import FastMarkerCluster
from folium import plugins
from collections import Counter

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["College"]
collection = db["test 3"]

cursor = collection.find()

app = Flask(__name__)


def get_map():
    map_data = []
    college_districts = []
    for document in cursor:
        map_data.append({"college name": document['Name'],
                         "coordinate": document['Location'],
                         "latitude": float(document['Location'].split(",")[0]),
                         "longitude": float(document['Location'].split(",")[1])})
        college_districts.append(document["District"])

    m = folium.Map(location=[32.084206, 77.571167], zoom_start=8)
    minimap = plugins.MiniMap()
    m.add_child(minimap)

    folium.TileLayer('OpenStreetMap').add_to(m)
    folium.TileLayer('Stamen Terrain').add_to(m)
    folium.TileLayer('Stamen Toner').add_to(m)
    folium.TileLayer('Stamen Water color').add_to(m)
    folium.TileLayer('cartodbpositron').add_to(m)
    folium.TileLayer('cartodbdark_matter').add_to(m)

    college_list = []
    coord_list = []
    for data in map_data:
        coord_list.append([data['latitude'], data['longitude']])
        college_list.append(data['college name'])
    FastMarkerCluster(data=coord_list, popup=college_list).add_to(m)

    folium.LayerControl(position='bottomleft').add_to(m)

    m.save('templates/college_map.html')

    def calculate_top_districts(college_district):
        district_counts = Counter(college_district)
        top_district = [district for district, _ in district_counts.most_common(3)]
        return top_district

    top_districts = calculate_top_districts(college_districts)
    return top_districts


def get_district_data(district_name):
    district_data_list = []
    for document in cursor:
        if document['District'] == district_name:
            district_data_list.append({
                "college_name": document['Name'],
                "image": document['Image'],
                "link": document['Link'],
                "course": document['Course']
            })
    return district_data_list


def get_all():
    all_district_datas = []
    for document in cursor:
        all_district_datas.append({"college_name": document['Name'],
                                   "image": document['Image'],
                                   "link": document['Link'],
                                   "course": document['Course']})
    return all_district_datas


def get_government():
    get_government_district_data = []
    for document in cursor:
        if "Govt" in document['Name'] or "Government" in document['Name']:
            get_government_district_data.append({"college_name": document['Name'],
                                                 "image": document['Image'],
                                                 "link": document['Link'],
                                                 "course": document['Course']})
    return get_government_district_data


def get_private():
    get_private_district_data = []
    for document in cursor:
        if "Pvt" in document['Name'] or "Private" in document['Name']:
            get_private_district_data.append({"college_name": document['Name'],
                                              "image": document['Image'],
                                              "link": document['Link'],
                                              "course": document['Course']})
    return get_private_district_data


def get_other():
    get_other_district_data = []
    for document in cursor:
        if "Pvt" not in document['Name'] and "Private" not in document['Name'] and "Govt" not in document['Name'] \
                and "Government" not in document['Name']:
            get_other_district_data.append({"college_name": document['Name'],
                                            "image": document['Image'],
                                            "link": document['Link'],
                                            "course": document['Course']})
    return get_other_district_data


@app.route('/')
def home():
    top_districts = get_map()
    return render_template('home.html', top_districts=top_districts)


@app.route('/map')
def print_map():
    return render_template('college_map.html')


@app.route('/district/<district_name>')
def district_data(district_name):
    send_district_data = get_district_data(district_name)
    for college in send_district_data:
        college['course'] = eval(college['course'])

    send_course_data = []
    for college in send_district_data:
        courses = college.get('course', [])
        send_course_data.extend(courses)
    print(send_district_data)
    print(send_course_data)
    cursor.rewind()
    return render_template('tiles.html', district_web_dataa=send_district_data, course_web_data=send_course_data)


@app.route('/all')
def all_district_data():
    send_district_data = get_all()
    for college in send_district_data:
        college['course'] = eval(college['course'])

    send_course_data = []
    for college in send_district_data:
        courses = college['course']
        send_course_data.extend(courses)

    cursor.rewind()
    return render_template('tiles.html', district_web_dataa=send_district_data, course_web_data=send_course_data)


@app.route('/government')
def government_district_data():
    send_district_data = get_government()
    for college in send_district_data:
        college['course'] = eval(college['course'])

    send_course_data = []
    for college in send_district_data:
        courses = college['course']
        send_course_data.extend(courses)

    cursor.rewind()
    return render_template('tiles.html', district_web_dataa=send_district_data, course_web_data=send_course_data)


@app.route('/private')
def private_district_data():
    send_district_data = get_private()
    for college in send_district_data:
        college['course'] = eval(college['course'])

    send_course_data = []
    for college in send_district_data:
        courses = college['course']
        send_course_data.extend(courses)

    cursor.rewind()
    return render_template('tiles.html', district_web_dataa=send_district_data, course_web_data=send_course_data)


@app.route('/other')
def other_district_data():
    send_district_data = get_other()
    for college in send_district_data:
        college['course'] = eval(college['course'])

    send_course_data = []
    for college in send_district_data:
        courses = college['course']
        send_course_data.extend(courses)

    cursor.rewind()
    return render_template('tiles.html', district_web_dataa=send_district_data, course_web_data=send_course_data)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == '__main__':
    app.run(debug=True)
