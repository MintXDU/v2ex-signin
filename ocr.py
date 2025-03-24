import requests
import base64
import urllib.parse
import json

with open('config.json', 'r') as file:
    config = json.load(file)
    API_KEY = config['API_KEY']
    SECRET_KEY = config['SECRET_KEY']

def recognize_captcha():
        
    url = "https://aip.baidubce.com/rest/2.0/ocr/v1/webimage_loc?access_token=" + get_access_token()
    
    ##### 图像数据，base64编码后进行urlencode，要求base64编码和urlencode后大小不超过4M，image 从本地读取
    # 读取PNG图片文件
    with open("captcha.png", "rb") as image_file:
        image_data = image_file.read()

    # 将图片数据转换为Base64编码
    base64_encoded = base64.b64encode(image_data).decode('utf-8')

    # 对Base64编码后的字符串进行URL编码
    urlencoded_data = urllib.parse.quote(base64_encoded)

    payload= 'image=' + urlencoded_data + '&detect_direction=false&poly_location=false&probability=false'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload.encode("utf-8"))
    
    return json.loads(response.text)["words_result"][0]["words"]

def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))
