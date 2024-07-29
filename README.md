
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
