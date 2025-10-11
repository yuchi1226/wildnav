# 將飛行區域修改為彰化師範大學的指南

要將您的程式應用於彰化師範大學區域，您需要修改以下幾個檔案中的參數。以下是詳細的修改指南：

## 1. 修改 build_map.py

### 確定彰化師範大學的經緯度範圍
首先，您需要確定彰化師範大學的經緯度範圍。您可以通過Google地圖獲取這些信息：

1. 打開Google地圖並找到彰化師範大學
2. 右擊地圖左上角點，選擇「這是什麼？」獲取緯度和經度
3. 同樣方式獲取右下角點的座標

假設彰化師範大學的經緯度範圍大致為：
- 左上角：24.0810, 120.5730
- 右下角：24.0740, 120.5830

### 修改 flight_zone 參數
在 `build_map.py` 中，找到以下行並修改為彰化師範大學的座標：

```python
# 修改前：
flight_zone = FlightZone(60.408615, 22.460445, 60.400855, 22.471289)

# 修改後：
flight_zone = FlightZone(24.0810, 120.5730, 24.0740, 120.5830)
```

### 調整 patch_size (可選)
根據新區域的大小，您可能需要調整 `patch_size`：

```python
# 如果需要調整補丁大小，修改這行：
patch_size = PatchSize(0.001676, 0.00341)  # 根據需要調整這些值
```

### 更新 API 密鑰
確保您使用的是有效的 Google Maps API 密鑰：

```python
# 替換為您自己的 API 密鑰
API_KEY = "您的_API_密鑰"
```

## 2. 修改 extract_image_meta_exif.py

### 更新照片路徑
如果您將無人機照片放在不同的文件夾中，請更新路徑：

```python
# 修改前：
photo_folder = '../assets/query/'

# 修改後（根據您的實際路徑）：
photo_folder = '../assets/彰師大_query/'
```

## 3. 修改 wildnav.py

### 更新地圖和照片路徑
根據您的文件結構，更新地圖和無人機照片的路徑：

```python
# 修改前：
map_path = "../assets/map/"
map_filename = "../assets/map/map.csv"
drone_photos_filename = "../assets/query/photo_metadata.csv"

# 修改後（根據您的實際路徑）：
map_path = "../assets/彰師大_map/"
map_filename = "../assets/彰師大_map/map.csv"
drone_photos_filename = "../assets/彰師大_query/photo_metadata.csv"
```

### 更新照片讀取路徑
同樣需要更新照片讀取路徑：

```python
# 在 csv_read_drone_images 函數中：
photo_path = "../assets/彰師大_query/"  # 根據您的實際路徑修改

# 在 csv_read_sat_map 函數中：
photo_path = "../assets/彰師大_map/"  # 根據您的實際路徑修改
```

## 4. 修改 superglue_utils.py

### 更新輸入輸出路徑
確保輸入輸出路徑正確：

```python
# 修改前：
input = '../assets/map/'
output_dir = "../results"

# 修改後：
input = '../assets/彰師大_map/'  # 根據您的實際路徑修改
output_dir = "../彰師大_results"  # 根據您的實際路徑修改
```

## 5. 創建必要的文件夾結構

在運行程式之前，請確保創建以下文件夾結構：

```
項目根目錄/
├── assets/
│   ├── 彰師大_map/      # 存放衛星地圖圖像
│   └── 彰師大_query/    # 存放無人機照片
├── 彰師大_results/      # 存放結果文件
└── (其他項目文件)
```

## 6. 運行流程

1. 首先運行 `build_map.py` 下載彰化師範大學區域的衛星圖像
2. 將無人機照片放入 `../assets/彰師大_query/` 文件夾
3. 運行 `extract_image_meta_exif.py` 提取無人機照片的元數據
4. 運行 `wildnav.py` 進行特徵匹配和位置計算

## 注意事項

1. **Google Maps API 限制**:
   - 確保您的 API 密鑰有足夠的配額來下載所需數量的衛星圖像
   - 大型區域可能需要多個 API 請求，請注意使用限制

2. **圖像質量**:
   - 確保衛星圖像和無人機圖像的質量足夠高，以便特徵匹配算法能夠正常工作
   - 如果匹配效果不佳，可以嘗試調整 `superglue_utils.py` 中的參數

3. **坐標系統**:
   - 確保所有坐標使用相同的坐標系統（通常是 WGS84）
   - 如果需要，可以將坐標轉換為當地坐標系統

4. **性能考慮**:
   - 大型區域可能需要較長的處理時間
   - 考慮使用 GPU 加速 SuperGlue 算法的運行

通過以上修改，您的程式應該能夠適用於彰化師範大學區域。如果您在實施過程中遇到任何問題，請隨時詢問。