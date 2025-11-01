"""用於自動從 Google Maps API 建立衛星地圖的模組
此模組提供以下功能：
1. 從 Google Maps 下載指定地理區域的衛星圖像
2. 將圖像組織成結構化的地圖資料庫
3. 生成地理參考的元數據
4. 將地圖資料以標準化的 CSV 格式儲存

注意：需要有效的 Google Maps API 金鑰才能運作
"""
import csv
import math
import shutil
import requests



############################################################################################
# Satellite map building script
# Requires access to Google Static Maps API,
#   see https://developers.google.com/maps/documentation/maps-static/overview
# It will not work with current API_KEY, you need to get your own
############################################################################################

# Path to the folder where the map will be saved
MAP_PATH = "../assets_ncue/map/"
class FlightZone:
    """由兩個點（緯度和經度）定義的矩形飛行區域
    用於指定需要下載衛星圖像的地理範圍"""
    def __init__(self, top_left_lat, top_left_lon,\
         bottom_right_lat, bottom_right_lon, filename = "default"):
        self.filename = filename
        self.top_left_lat = top_left_lat
        self.top_left_lon = top_left_lon
        self.bottom_right_lat = bottom_right_lat
        self.bottom_right_lon = bottom_right_lon

    def __str__(self):
        return f"{self.__class__.__name__}; \n{self.top_left_lat}: %f \nt{self.top_left_lon}: \
            \n{self.bottom_right_lat}: %f \n{self.bottom_right_lon} %f" 
class PatchSize:
    """地圖片段的大小（以十進制緯度和經度表示）
    用於定義下載衛星圖像時的分割大小"""
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def __str__(self):
        return f"{self.__class__.__name__}; \n{self.lat}: %f \n{self.lon}"

def csv_write_image_location():
    """Writes a csv file with the geographical location of the downloaded satellite images"""
    # 修正：使用正確的列名列表，而不是單個字符串
    header = ["Filename", "Top_left_lat", "Top_left_lon", "Bottom_right_lat", "Bottom_right_long"]
    file_path = MAP_PATH + 'map.csv'
    with open(file_path, 'w', encoding='UTF8', newline='') as file:  # 添加 newline='' 避免空行
        writer = csv.writer(file)
        writer.writerow(header)  # 寫入正確的列名
        for photo in photo_list:
            # 修正：只使用文件名，而不是完整路徑
            filename_only = photo.filename.split('/')[-1] if '/' in photo.filename else photo.filename
            line = [filename_only, 
                   str(photo.top_left_lat), 
                   str(photo.top_left_lon), 
                   str(photo.bottom_right_lat), 
                   str(photo.bottom_right_lon)]
            writer.writerow(line)

# These 2 variables determine the number of images that form the map

#define as a pair of coordinates determining a rectangle in which the satellite photos will be taken
flight_zone = FlightZone(24.069793, 120.548037, 24.064620, 120.561510)

#define as height (latitude) and width (longitude) of the patch to be taken
patch_size = PatchSize(0.001676, 0.00341)

# Number of satellite patches needed to build the map
width = math.floor((flight_zone.bottom_right_lon -  flight_zone.top_left_lon) / patch_size.lon)
height = math.floor((flight_zone.top_left_lat - flight_zone.bottom_right_lat) / patch_size.lat)

total = width * height
print(f"The script will download : {total} images. Do you want to continue? [Y/N]")
answer = input()

while answer not in ('Y', 'N', 'y', 'n'):
    print("Please answer with Y or N")
    answer = input()

if answer in ('Y', 'y'):
    print("Downloading images...")
elif answer in ('N', 'n'):
    print("Exiting...")
    exit(1)

current_center = PatchSize(flight_zone.top_left_lat - patch_size.lat / 2, \
     flight_zone.top_left_lon + patch_size.lon / 2)
current_top_left = PatchSize(flight_zone.top_left_lat, flight_zone.top_left_lon)
current_bottom_right = PatchSize(current_top_left.lat - patch_size.lat, \
     current_top_left.lon + patch_size.lon)

center = str(current_center.lat) + "," + str(current_center.lon)
zoom = "18" # optimized for the perspective of a wide angle camera at 120 m altitude
size = "640x640"  # maximum allowed size
maptype = "satellite"
scale = "2" # maximum allowed scale
#restricted by IP address, so you will have to generate your own
API_KEY = ""

URL = "https://maps.googleapis.com/maps/api/staticmap?" # base URL for the Google Maps API

#defining a params dict for the parameters to be sent to the API
PARAMS = {'center':center,
          'zoom':zoom,
          'size':size,
          'scale':scale,
          'maptype':maptype,
          'key':API_KEY
        }

photo_list = [] # list of all the photos that will be downloaded
index = 0 # index of the current image

# build map by downloading and stitching together satellite images
for i in range(0, height):
    for j in range(0, width):
        photo_name = 'sat_patch' + '_' + f"{index:04d}"+ '.png'

        #send GET request to the API which returns a satellite image upon success
        r = requests.get(url = URL, params = PARAMS, stream=True, timeout=10)


        # if request successful, write image to file
        if r.status_code == 200:
            with open(MAP_PATH + photo_name, 'wb') as out_file:
                shutil.copyfileobj(r.raw, out_file)
                print("image "+ str(index) + " downloaded")
        else:
            print("Error " + r.status_code + " downloading image " + str(index))
        
        current_patch = FlightZone(current_top_left.lat, current_top_left.lon, \
             current_bottom_right.lat, current_bottom_right.lon, photo_name)
        photo_list.append(current_patch)
        index += 1
        current_center.lon = current_center.lon + patch_size.lon
        current_top_left.lon += patch_size.lon
        current_bottom_right.lon += patch_size.lon
        PARAMS['center'] = str(current_center.lat) + "," + str(current_center.lon)
    current_top_left.lat -= patch_size.lat
    current_top_left.lon = flight_zone.top_left_lon
    current_bottom_right.lat -= patch_size.lat
    current_bottom_right.lon = flight_zone.top_left_lon + patch_size.lon
    current_center.lat = current_center.lat - patch_size.lat
    current_center.lon = flight_zone.top_left_lon + patch_size.lon / 2
    PARAMS['center'] = str(current_center.lat) + "," + str(current_center.lon)

print("Map images downloaded, writing csv file")
csv_write_image_location()
print("Map built successfully, check the map folder: " + MAP_PATH)