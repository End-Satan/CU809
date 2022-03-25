from flask import Flask
import requests

app = Flask(__name__)


HOST_IP = "120.53.243.247"  # 你的目的服务器IP（比如v2ray）
HOST_PORT = "8180"  # 你的目的服务器端口

THIS_SERVER_IP = requests.get("http://httpbin.org/ip").json()["origin"]


@app.route("/", methods=["GET"])
def get_token():
    j1_data = {
        "authenticateBasic": {"userType": "3"},
        "authenticateDevice": {
            "deviceModel": "Wotv_Android",
            "physicalDeviceID": "7185b6cb-70c9-48f5-8563-51dfac10c3f4",
        },
        "authenticateTolerant": {"subnetID": "8601", "bossID": "TJBOSS2"},
    }

    p = requests.post(
        "http://119.3.176.199:33200/VSP/V3/Authenticate", json=j1_data
    ).json()

    jSessionID = p.get("jSessionID")
    csrfToken = p.get("csrfToken")
    fmt_headers = {
        "X_CSRFToken": csrfToken,
        "Cookie": "CSRFSESSION={}; JSESSIONID={}".format(csrfToken, jSessionID),
        "user-agent": "Mozilla/5.0 (Linux; U; Android 4.0.4; es-mx; HTC_One_X Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0",
    }
    j2_data = {
        "VSCIP": "{}:33200".format(THIS_SERVER_IP),
        "codeRate": "1",
        "contentId": "fe2daad63b6e46ea920275307cbd31b1",
        "contentIdV6": "20729754",
        "mediaIdV6": "20729916",
        "subContentId": "fe2daad63b6e46ea920275307cbd31b1",
        "userId": "02910308087",
        "userIp": "192.168.7.188",
        "videoName": "极盗行动",
        "videoType": "1",
    }

    p2 = requests.post(
        "https://mobileapi.chinaunicomvideo.cn:10001/queryVideoURLForWV",
        headers=fmt_headers,
        json=j2_data,
    ).json()

    tvURL = p2.get("tvURL")
    trueURL = requests.get(tvURL).json()

    return trueURL.get("url")


@app.route("/VSP/V3/PlayVOD", methods=["GET", "POST"])
def res_auth():
    result = {
        "result": {
            "retMsg": "Success,platform authorize:270623 has free product.",
            "retCode": "000000000",
        },
        "authorizeResult": {
            "productID": "84001002",
            "isLocked": "0",
            "isParentControl": "0",
        },
        "playURL": "http://{}:{}/?rrsip={}&zoneoffset=0&servicetype=0&icpid=&limitflux=-1&limitdur=-1&tenantId=8601&accountinfo=%2C10000000000041%2C121.25.67.1%2C20220323221750%2C1571729558144191%2Ca03007316b0783fc8b82661561090526623284%2C0.0%2C1%2C0%2C%2C%2C1%2C84001002%2C%2C%2C1%2C1%2C270622%2CEND&GuardEncType=2".format(
            HOST_IP, HOST_PORT, HOST_IP
        ),
    }

    return result


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="33200", debug=True)
