# WildNav 系統功能概述

WildNav 是一個基於圖像特徵匹配的地理定位系統，主要用於無人機航拍圖像與衛星地圖的匹配定位。

## 系統架構

系統主要由以下幾個模組組成：

### 1. 核心功能模組 (wildnav.py)
- 實現了主要的圖像匹配和地理定位功能
- 包含兩個主要類：
  - `GeoPhotoDrone`: 儲存無人機照片及其 GNSS 位置和相機旋轉參數
  - `GeoPhoto`: 儲存衛星照片及其地理邊界座標

### 2. 地圖建構模組 (build_map.py)
- 使用 Google Maps API 自動構建衛星地圖
- 實現了以下功能：
  - 定義飛行區域（FlightZone）
  - 下載衛星圖片
  - 生成地圖metadata CSV文件

### 3. 數據視覺化模組 (plot_data.py)
- 用於分析和視覺化定位結果
- 功能包括：
  - 繪製真實座標與計算座標的對比圖
  - 計算定位誤差統計
  - 生成性能報告

### 4. 圖像特徵提取模組 (superglue_utils.py)
- 整合了 SuperGlue 深度學習模型
- 用於圖像特徵提取和匹配

## 數據結構

系統使用兩種主要的CSV文件格式：

1. 地圖圖像metadata (map.csv):
```
Filename, Top_left_lat, Top_left_lon, Bottom_right_lat, Bottom_right_long
```

2. 無人機圖像metadata (photo_metadata.csv):
```
Filename, Latitude, Longitude, Altitude, Gimball_Roll, Gimball_Yaw, Gimball_Pitch, Flight_Roll, Flight_Yaw, Flight_Pitch
```

## 工作流程

1. 系統首先通過 build_map.py 建立衛星地圖資料庫
2. 無人機在目標區域進行航拍，並記錄初始 GNSS 位置資訊
3. wildnav.py 使用 SuperGlue 進行圖像特徵匹配
4. 根據匹配結果計算精確的地理位置
5. 最後通過 plot_data.py 進行結果分析和視覺化

## 性能指標

系統提供以下性能指標：
- 定位成功率（定位成功的圖像數/總圖像數）
- 平均定位誤差（米）
- 最大定位誤差（米）
