import requests 
from bs4 import BeautifulSoup,Tag 
from PIL import Image,ImageDraw, ImageFont
from pathlib import Path

url = "http://www.proveyourworth.net/level3/start"
url_log = "http://www.proveyourworth.net/level3/activate?statefulhash"
payload = "http://www.proveyourworth.net/level3/payload"

path = Path('./')

request = requests.Session()

def hashValue(url):
    req = request.get(url)
    if req.status_code == 200:
        html_parse = BeautifulSoup(req.text, 'html.parser')
        return html_parse.find('input',{'name' : 'statefulhash'})['value']

def login(url_log, hashValue):
    hash = hashValue(url)

    with request.get(f'{url_log}={hash}') as req:
        if req.status_code == 200:
            print('Successfully logged!')
        else:
            print('Failed')

def downloadPayload(payload):
    req = request.get(payload, stream=True)

    with open('image.jpg', 'wb') as image:
        for elem in req.iter_content():
            image.write(elem)

    req.close()
    print('Image Ready To Sign')


def signWithMyName(image):    
    image = Image.open(image)

    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('varsity_regular.ttf', 20)
    draw.text((image.width/3,30), f'William Isaac Luna Villagrana \n Web Developer \n Hash:  {hashValue(url)}', fill='red', font=font)

    image.save('image.jpg', 'JPEG')
    print('Image Signed and Saved')

def post(payload):
    payload = request.get(payload)
    post = f"{payload.headers['X-Post-Back-To']}"
   

    file = {
        "image" : open(path / 'image.jpg', 'rb'),
        "code" : open(path / 'proveyourworth.py', 'rb'),
        "resume" : open(path / 'Resume William.pdf', 'rb'),
        "email" : 'lunapsygeek@gmail.com',
        "name" : 'William Isaac Luna Villagrana',
        "aboutme" : 'Im a Web Developer with experience in MERN Stack, Pythom, Django, C# .NET. Never give up!'
    }

    data = {
        "email" : 'lunapsygeek@gmail.com',
        "name" : 'William Isaac Luna Villagrana',
        "aboutme" : 'Im a Web Developer with experience in MERN Stack, Pythom, Django, C# .NET. Never give up!',
        "image" : 'https://github.com/LunaPsyWill/ProveYourWorth/blob/main/image.jpg',
        "code" : 'https://github.com/LunaPsyWill/ProveYourWorth/blob/main/proveyourworth.py',
        "resume" : 'https://drive.google.com/file/d/14xHjnTnhi9bEDPVPtAfQIxRq0ak_9S5X/view?usp=sharing'
    }

    with request.post(post, data=data, files=file) as req:
        if req.status_code == 200:
            print('Successfully Completed!')
        else:
            print('POST failed')
            
        print(req.text) 

if __name__ == '__main__':
    hashValue(url)
    login(url_log, hashValue)
    downloadPayload(payload)
    signWithMyName('image.jpg')
    post(payload)
