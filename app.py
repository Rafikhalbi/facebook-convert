from flask import Flask,render_template,request
import requests
res = requests.Session()
import re

url = 'https://free.facebook.com'
url_login = 'https://free.facebook.com/login/device-based/regular/login/?refsrc=deprecated&lwv=100&refid=8'

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def fbcookies(username,password):
    # print(username,password)
    GETHOME = res.get(url,headers = {
        'Host': 'free.facebook.com',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Linux; Android 10; CPH2179) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode':'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7',
    }).content
    cookie = dict(res.cookies.get_dict())
    
    try:
        data= {
            'lsd': re.search(r'name="lsd" value="(.*?)"',str(GETHOME))[1],
            'jazoest': re.search(r'name="jazoest" value="(.*?)"',str(GETHOME))[1],
            'm_ts': re.search(r'name="m_ts" value="(.*?)"',str(GETHOME))[1],
            'li': re.search(r'name="li" value="(.*?)"',str(GETHOME))[1],
            'try_number': '0',
            'unrecognized_tries': '0',
            'email': username,
            'pass': password,
            'login': 'Masuk',
            'bi_xrwh': '0'
        }
    except:
        return "Terjadi Kesalahan"
    # print(data)
    try:
        RESPONSE = res.post(url_login,headers={
            'Host': 'free.facebook.com',
            'content-length': '160',
            'cache-control': 'max-age=0',
            'origin': 'https://free.facebook.com',
            'upgrade-insecure-requests': '1',
            'dnt': '1',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (Linux; Android 10; CPH2179) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Mobile Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://free.facebook.com/',
            'accept-language': 'id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7'
        }, data = data, cookies = cookie)
        if 'c_user' in res.cookies.get_dict():
            return ';'.join(['%s=%s'%(key,value) for key,value in res.cookies.get_dict().items()])
        elif 'checkpoint' in res.cookies.get_dict():
            return "Akun Facebook Anda Terkena Checkpoint"
        else:
            return "Username / Password Salah"
    except:
        return "Username / Password Salah"
     
    
    
@app.route('/fb-cookies',methods=["GET","POST"])
def fb_cookies():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        cv = fbcookies(username,password)
        
        return render_template('fbcookies.html',cookies=cv)
        
    elif request.method == "GET":
        return render_template('fbcookies.html')
   
if __name__ == '__main__':
    app.run(debug=True)