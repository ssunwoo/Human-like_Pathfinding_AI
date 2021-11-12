import googlemaps
from datetime import datetime
import osmnx as ox
import pandas as pd
import get_result
import folium
Google_API_Key = 'AIzaSyDzUjd36fINrZML2hKpkBj19cVLMYdB4r4'


def getLoc(addr):
    gmaps = googlemaps.Client(key = Google_API_Key)  
    geocode_result = gmaps.geocode(addr)   
    n_lat = geocode_result[0]['geometry']['location']['lat']
    n_lng = geocode_result[0]['geometry']['location']['lng']
    loc = {'lat':n_lat, 'lng':n_lng}
    return loc

def get_start_end_point():
    start_point= getLoc(input('출발지를 입력해주세요: '))
    #print(start_point)

    destination = getLoc(input('목적지를 입력해주세요: '))
    #print(destination)

    sta_lat_lon = (start_point['lat'], start_point['lng'])

    des_lat_lon = (destination['lat'], destination['lng'])
    print("출발지(위도, 경도) :",sta_lat_lon)
    print("도착지(위도, 경도) :",des_lat_lon)
    
    return sta_lat_lon, des_lat_lon
    

def get_nodes_to_bbox(sta_lat_lon):

    # (위도, 경도) 중심점으로 일정 간격(dist)으로 bbox를 형성한다.
    bbox = ox.utils_geo.bbox_from_point(sta_lat_lon, dist=1500, 
                                        project_utm=False, return_crs=False)
    
   
    # bbox를 기준으로 그래프 그리기
    G = ox.graph.graph_from_bbox(bbox[0], bbox[1], bbox[2], bbox[3], 
                                network_type='walk', 
                                simplify=True, 
                                retain_all=False, 
                                truncate_by_edge=False, 
                                clean_periphery=True, 
                                custom_filter=None)

    fig, ax = ox.plot_graph(G, node_color='b')

    # 노드들의 위도 경도를 리스트로 담아 csv 파일로 만들기
    node_lat_lon = []

    for node in G.nodes:
        node_lat_lon.append([G.nodes[node]['x'], G.nodes[node]['y']])

    node_name = []
    for node in G.nodes:
        node_name.append(node)

    # 노드의 ID와 경도, 위도를 담은 데이터 프레임 생성
    df = pd.DataFrame(node_lat_lon)
    df_names = pd.DataFrame(node_name)

    # 2개의 데이터 프레임 합치기
    final_df = pd.concat([df_names, df], axis=1)

    # csv 파일로 저장하기
    final_df.to_csv('node_lat_lon.csv', index=False, header=None)
    
    print('==================================================')
    print('              Complete graph.csv')
    print('==================================================')
    
    return G
    
def get_coordinate_info(data):
    coordinate_info = {}
    for i in data.values:
        coordinate_info[i[0]] = {
            'x': i[1],
            'y': i[2]
        }
    return coordinate_info

def get_node_id(G, sta_lat_lon, des_lat_lon):
    # 출발지 노드 ID
    sta_node = ox.distance.nearest_nodes(G, sta_lat_lon[1], sta_lat_lon[0], return_dist=False)

    # 목적지 노드 ID
    des_node = ox.distance.nearest_nodes(G, des_lat_lon[1], des_lat_lon[0], return_dist=False)

    return sta_node, des_node

def change_node_id_to_lat_lon(G, route_node):

    path_lat_lon = []

    for node in route_node:
        path_lat_lon.append([G.nodes[node]['y'], G.nodes[node]['x']])
        
    return path_lat_lon

def find_start(lat_lon_result):
    return lat_lon_result[0]

def find_goal(lat_lon_result):
    return lat_lon_result[-1]

def visualization_route(path_lat_lon):

    # 위치(위도, 경도) 정보를 list로 저장
    location_data = []
    for lat_lon in path_lat_lon:  # 학습으로 얻은 결과 리스트
        location_data.append([lat_lon[0], lat_lon[1]]) 

    # 출발지 정보 및 도착지 변수 생성
    start_point = find_start(location_data) # 실제 구현시 결과값 리스트가 들어갈 것
    destination = find_goal(location_data)

    # 지도 변수 만들기
    m = folium.Map(location=start_point, zoom_start=14) 

    # 마커 표시하기
    # add_to() 함수를 이용해 미리 만들어둔 변수에 내용을 추가할 수 있음
    folium.Marker(start_point,
                popup='Start_Point / 출발지',
                tooltip='Start_Point / 출발지').add_to(m)

    folium.Marker(destination,
                popup='Destination / 도착지',
                tooltip='Destination / 도착지').add_to(m)

    # 선으로 경로 표시하기
    folium.PolyLine(locations=location_data,tooltip='Polyline').add_to(m)

    # 지도를 html 파일로 저장
    m.save('visualization_route.html')

    # 지도를 웹브라우저에 띄움
    import webbrowser
    url = 'file:///C:/Users/EunJin/workplace/Reinforcement-Learning-in-Path-Finding_1/visualization_route.html' # html파일은 파이썬 코드 저장되는 폴더에 저장됨
    print(url)
    webbrowser.open(url)
