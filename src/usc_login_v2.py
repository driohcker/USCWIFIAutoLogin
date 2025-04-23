import requests
import time
import re
import subprocess
import time
from encryption.srun_md5 import *
from encryption.srun_sha1 import *
from encryption.srun_base64 import *
from encryption.srun_xencode import *

# === WiFi 参数 ===
TARGET_WIFI = "USCWIFI"

# === 校园网参数 ===
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36'
}
init_url = "http://210.43.112.9"
get_challenge_api = "http://210.43.112.9/cgi-bin/get_challenge"
srun_portal_api = "http://210.43.112.9/cgi-bin/srun_portal"

n = '200'
type = '1'
ac_id = '5'
enc = "srun_bx1"

username = "你的学号"
password = "你的密码"

# === 自动连接 WiFi ===
def connect_wifi():
    print(f"尝试连接WiFi：{TARGET_WIFI}")
    subprocess.run(f'netsh wlan connect name="{TARGET_WIFI}"', shell=True)
    time.sleep(5)

# === 检查当前 WiFi 是否连接 ===
def check_wifi_connected():
    result = subprocess.run(
        'netsh wlan show interfaces',
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8',  # 强制用 utf-8 解码
        errors='ignore'    # 忽略非法字符
    )
    output = result.stdout
    if output:
        return TARGET_WIFI in output
    else:
        print("获取WiFi信息失败")
        return False


# === 初始化获取IP ===
def init_getip():
    global ip
    init_res = requests.get(init_url, headers=header)
    print("初始化获取ip")
    ip = re.search('id="user_ip" value="(.*?)"', init_res.text).group(1)
    print("ip:" + ip)

# === 获取 token ===
def get_token():
    global token
    get_challenge_params = {
        "callback": "jQuery112404953340710317169_" + str(int(time.time() * 1000)),
        "username": username,
        "ip": ip,
        "_": int(time.time() * 1000),
    }
    get_challenge_res = requests.get(get_challenge_api, params=get_challenge_params, headers=header)
    token = re.search('"challenge":"(.*?)"', get_challenge_res.text).group(1)
    print("token为:" + token)

# === 信息加密准备 ===
def get_chksum():
    chkstr = token + username
    chkstr += token + hmd5
    chkstr += token + ac_id
    chkstr += token + ip
    chkstr += token + n
    chkstr += token + type
    chkstr += token + i
    return chkstr

def get_info():
    info_temp = {
        "username": username,
        "password": password,
        "ip": ip,
        "acid": ac_id,
        "enc_ver": enc
    }
    i = re.sub("'", '"', str(info_temp))
    i = re.sub(" ", '', i)
    return i

def do_complex_work():
    global i, hmd5, chksum
    i = get_info()
    i = "{SRBX1}" + get_base64(get_xencode(i, token))
    hmd5 = get_md5(password, token)
    chksum = get_sha1(get_chksum())
    print("所有加密工作已完成")

def login():
    srun_portal_params = {
        'callback': 'jQuery11240645308969735664_' + str(int(time.time() * 1000)),
        'action': 'login',
        'username': username,
        'password': '{MD5}' + hmd5,
        'ac_id': ac_id,
        'ip': ip,
        'chksum': chksum,
        'info': i,
        'n': n,
        'type': type,
        'os': 'windows+10',
        'name': 'windows',
        'double_stack': '0',
        '_': int(time.time() * 1000)
    }
    srun_portal_res = requests.get(srun_portal_api, params=srun_portal_params, headers=header)
    print("登录返回信息：", srun_portal_res.text)

    try:
        res = requests.get(srun_portal_api, params=srun_portal_params, headers=header)
        print("登录返回信息：", res.text)

        # 解析返回内容中是否包含登录成功提示
        if 'E0000: Login is successful.' in res.text:
            print("✅ 登录成功！")
        elif 'E2531: Password is error' in res.text:
            print("❌ 密码错误，请检查用户名和密码。")
        elif 'E2553: Account is not found' in res.text:
            print("❌ 账号不存在。")
        else:
            print("⚠️ 登录失败，返回信息未识别。")
    except Exception as e:
        print("登录请求失败，错误信息：", str(e))

if __name__ == '__main__':
    print("启动校园网自动登录脚本...")

    connect_wifi()

    for attempt in range(10):
        if check_wifi_connected():
            print(f"第 {attempt+1} 次检测：已连接 {TARGET_WIFI}")
            break
        else:
            print(f"第 {attempt+1} 次检测：WiFi尚未连接，等待中...")
            time.sleep(2)
    else:
        print("连接WiFi失败，程序退出")
        exit(1)

    init_getip()
    get_token()
    do_complex_work()
    login()
