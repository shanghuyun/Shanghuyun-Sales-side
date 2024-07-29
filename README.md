
# 尚虎雲平台-銷售端文件

## 簡介
這是一個用於銷售商品的平台。

## 下載檔案

1. 請先將檔案下載下來 [載點](https://github.com/shanghuyun/Shanghuyun-Sales-side/releases/tag/%E6%AA%94%E6%A1%88)

## 部署到 PythonAnywhere

### 1. 註冊 PythonAnywhere 帳戶

請先至 [PythonAnywhere](https://www.pythonanywhere.com/registration/register/beginner/) 註冊一個帳戶。

↓↓↓註冊完成畫面應該如下圖↓↓↓

![註冊完成畫面](docs/images/註冊pythonanywhere.png)

### 2. 上傳檔案

- 點擊 **"Files"** 底下的 **Browse files**

  ![點擊 Browse files](docs/images/點擊browseFiles.png)

- 將剛剛下載的檔案上傳

  ![檔案上傳](docs/images/檔案上傳.png)

### 3. 新增 Bash

返回一開始畫面新增一個 **Bash**

![新增 Bash](docs/images/新增bash.png)

### 4. 安裝虛擬機

輸入以下指令

```bash
mkvirtualenv myvirtualenv --python=/usr/bin/python3.10 && unzip Sales-side.zip && cd Sales-side && pip install -r requirements.txt
```

![執行完成畫面](docs/images/執行完成.png)

### 5. 新增 Web 應用程序

點擊 **Open Web tab** 新增一個 App

![新增 app](docs/images/新增app.png)
![點選 Add a new web app](docs/images/addApp.png)
![點選 Next](docs/images/Next.png)
![點選 manualConfiguration](docs/images/manualConfiguration.png)
![點選 Python 3.10](docs/images/選擇3.10.png)
![點選 Next 完成設置](docs/images/完成設置.png)

### 6. 配置 WSGI

進入 WSGI 設置

![進入 WSGI 設置](docs/images/進入WSGI設置.png)

將程式碼改成以下程式碼，記得要替換成自己的帳號名稱，並按下保存

```python
# +++++++++++ DJANGO +++++++++++
# To use your own django app use code like this:
import os
import sys

# assuming your django settings file is at '/home/myusername/mysite/mysite/settings.py'
path = '/home/替換成自己的帳號名稱/Sales-side'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'core.settings'

# serve django via WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

![保存設置](docs/images/保存.png)

### 7. 設置 Virtualenv

輸入 Virtualenv

```
myvirtualenv
```

![輸入 Virtualenv](docs/images/輸入Virtualenv.png)

### 8. 重新加載 Web 應用程序

重新加載 Web 應用程序以使變更生效。

![重載 Web](docs/images/重載Web.png)

### 9. 完成

點擊網址

![點擊網址](docs/images/點擊網址.png)

大功告成了!

![大功告成](docs/images/大功告成.png)

## 網站配置

接下來會介紹如何更新網站內容

### 1. 進入管理員後台

在網址後輸入`/admin`進入後台管理介面

![進入後台](docs/images/進入後台.png)

### 2. **(重要)**輸入預設帳號密碼，並變更密碼

帳號:admin
密碼:csie2024

![變更密碼](docs/images/變更密碼.png)

### 3. 變更個人資料

有紅色星號的為必填其餘為選填，**用戶選擇admin**

![個人資料修改畫面](docs/images/個人資料.png)

![個人資料影響畫面](docs/images/變更密碼.png)
*此為個人資料所影響畫面*

### 4. 變更網頁標題 & logo

![網頁標題&logo修改畫面](docs/images/網頁標題&logo.png)

![網頁標題影響畫面](docs/images/網頁標題.png)
*此為網頁標題所影響畫面*

![網頁logo影響畫面](docs/images/網頁logo.png)
*此為網頁logo所影響畫面*

### 5. 變更輪播圖

![輪播圖新增畫面](docs/images/輪播圖.png)

![輪播圖影響畫面](docs/images/輪播圖影響.png)
*此為輪播圖所影響畫面*

### 6. 變更關於我們
![關於我們變更畫面](docs/images/關於我們.png)

![關於我們影響畫面](docs/images/關於我們影響.png)
*此為關於我們所影響畫面*

### 7. 新增賣家
- 目標網址請填生產端網址，當前版本商品內容都是由生產端提供，若需架設生產端請參考[這裡](https://github.com/shanghuyun/Shanghuyun-Production-side)

### 8. 變更嵌入地圖

- 嵌入式地圖程式碼由google map獲取，詳細步驟可參考[這裡](https://www.design-hu.com.tw/wordpress/wordpress-tools/google-maps-embed-to-website.html)
![嵌入地圖影響畫面](docs/images/地圖.png)
*此為關於我們所影響畫面*