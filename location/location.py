import pandas as pd
from haversine import haversine
from flask import Blueprint, render_template, request, session
import datetime
from werkzeug.utils import secure_filename


location_blue = Blueprint('location_blue', __name__)

@location_blue.route('/location', defaults={'latitude' : 37.5796653058195, 'longitude' : 126.998962996348, 'id' : 1})
@location_blue.route('/location/latitude=<latitude>', defaults={'longitude' : 126.998962996348, 'id' : 1})
@location_blue.route('/location/latitude=<latitude>/longitude=<longitude>/<id>')
def location(latitude, longitude, id) :
    latitude = float(latitude)
    longitude = float(longitude)

    location = (latitude, longitude)

    # 원래는 데이터를 db에 쌓아서 쿼리문으로 가져왔었는데, 동접자가 많아져서 서버비.. 때문에 csv로 바꿨습니당..
    df = pd.read_csv('./data/data.csv')
    result = []
    for index in range(1,len(df)) :
        tmp = {}
        
        data = df['latitude'][index], df['longitude'][index]
        
        if haversine(location, data) < 5 :
            
            tmp['place_1'] = df['place-info1'][index]
            tmp['place_2'] = df['place-info2'][index]
            tmp['movearound_date'] = df['movearound_date'][index]
            tmp['km'] = haversine(location, data)
            result.append(tmp)
    
    if result == [] :
        html = render_template('location_out.html', score = 0)
        return html
    result = sorted(result, key = lambda x : x['km'])
    df2 = pd.DataFrame(result)
    
    
    
    data = df2[df2['movearound_date']!= 'NaN/NaN']
    data['movearound_date'] = pd.to_datetime('2020/'+data['movearound_date'])
    
    result2 = data.groupby('movearound_date').count()['place_1'][-7:].reset_index()
    result2.rename(columns={'place_1':'count'}, inplace=True)
    today = datetime.date.today()  
    day = {today.strftime("%Y-%m-%d"):0, (today - datetime.timedelta(1)).strftime("%Y-%m-%d") : 0, (today - datetime.timedelta(2)).strftime("%Y-%m-%d") : 0, (today - datetime.timedelta(3)).strftime("%Y-%m-%d") : 0, (today - datetime.timedelta(4)).strftime("%Y-%m-%d") : 0, (today - datetime.timedelta(5)).strftime("%Y-%m-%d") : 0, (today - datetime.timedelta(6)).strftime("%Y-%m-%d") : 0}
    
    day_list = list(result2['movearound_date'])
    day_list = str(day_list)
    for row in day :
        if row in day_list :
            day[row] = result2[result2['movearound_date'] == row]['count'].values[0]
    day = pd.DataFrame({'movearound_date':list(day.keys()), 'count':list(day.values())})
    km_data = {'1km':0,'2km':0,'3km':0,'4km':0,'5km':0}
    for i in range(len(result)) :
        
        if result[i]['km'] < 1 :
            km_data['1km'] = km_data['1km'] + 1
        elif result[i]['km'] < 2 :
            km_data['2km'] = km_data['2km'] + 1
        elif result[i]['km'] < 3 :
            km_data['3km'] = km_data['3km'] + 1
        elif result[i]['km'] < 4 :
            km_data['4km'] = km_data['4km'] + 1
        elif result[i]['km'] < 5 :
            km_data['5km'] = km_data['5km'] + 1

    score = km_data['1km'] + km_data['2km'] + km_data['3km'] + km_data['4km'] + km_data['5km']
    
    score = (km_data['1km']*10 + km_data['2km']*8 + km_data['3km']*6 + km_data['4km']*4 + km_data['5km']*2)/len(df)
    
    score = int(score * 200)
    if score > 100 :
        score = 100
    html = render_template('location.html', info = result, day = day, km_data = km_data, id=id, score = score)
    return html

@location_blue.route('/map')
def map() :
    # 원래는 데이터를 db에 쌓아서 쿼리문으로 가져왔었는데, 동접자가 많아져서 서버비.. 때문에 csv로 바꿨습니당..
    df = pd.read_csv('./data/data.csv')
    df =  df.dropna(axis=0)
    
    lat = list(df['latitude'])
    lon = list(df['longitude'])
    movearound_date = list(df['movearound_date'])
    place_info1 = list(df['place-info1'])
    place_info2 = list(df['place-info2'])
    number = list(df['number'])
    html = render_template('map.html', df = df, lat=lat, lon=lon, movearound_date=movearound_date, place_info1=place_info1, place_info2=place_info2, number=number)
    return html


@location_blue.route('/upload_kmlam')
def load_file():

    html = render_template('upload.html')
    
    return html

@location_blue.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save("./data/" + secure_filename(f.filename))
      return 'file uploaded successfully'

@location_blue.route('/protection')
def protection() :

    location = ['경기 과천시 별양상가3로 11', '포천시 선단동 461-1', '경기 남양주시 다산지금로16번길 87', '경기 하남시 서하남로48번길 26', '경기 이천시 중리동 460-8', '경기 김포시 사우동 253-3',
    '경기 파주시 금촌동 932-28', '의정부시 평화로 224', '평택시 평택4로 39 쌍용대신빌딩 (4층)', '안산시 단원구 안산천서로9 우진빌딩 6층',
    '부천시 원미구 중동로 254번길 36 하이베라스빌딩 7층', '성남시 중원구 원터로105번길28 요한지파성남시온교회', '용인시 기흥구 강남로7 아트프라자(7,8층)',
    '용인시 기흥구 중부대로659(2층) 새소망교회']
    lat = [37.4263066568637, 37.8514986070217, 37.6078231337976, 37.51481751883757, 37.2756922564162, 37.6165950921068, 
    37.7598591601887, 37.71201, 36.991663, 37.317264,
    37.501987, 37.43485, 37.271261, 
    37.363673]
    lon = [126.991851977305, 127.163010025217, 127.170669442862, 127.14965162502159, 127.446505995535, 126.715720831408, 
    126.769391463719, 127.04819, 127.100196, 126.842298,
    126.771066, 127.139706, 127.126543, 
    127.116545]


    html = render_template('protection.html', location=location, lat=lat, lon=lon)
    
    return html