# coding=utf-8
import base64
import binascii
import datetime
import hashlib
import hmac
import json
import time
import urllib.parse
import uuid
from collections import OrderedDict

from typing import Dict


def escape(text) -> str:
    if isinstance(text, dict):
        text = json.dumps(text, ensure_ascii=False).replace(" ", "")
    return urllib.parse.quote(text, safe="~")

def getCurrentEpochTime() -> int:
    return int(time.mktime(datetime.datetime.now().timetuple()))

def getUUID() -> str:
    return str(uuid.uuid4()).upper()

def makeHeader(method, url, uuid=None, deviceId=None, headerType=None):
    if not headerType:
        headerType = 0

    header = OrderedDict()
    if headerType == 0:
        header["Host"] = url.replace("https://", "").split("/")[0]
        header["Authorization"] = None
        header["X-Twitter-Client-Version"] = "6.59.3"
        header["Accept"] = "*/*"
        header["X-Client-UUID"] = uuid if uuid else getUUID()
        header["X-Twitter-Client-Language"] = "ja"
        header["X-B3-TraceId"] = hashlib.md5(str(getCurrentEpochTime()).encode()).hexdigest()[0:16]
        # header["Proxy-Connection"] = "keep-alive"
        header["Accept-Language"] = "ja"
        header["Accept-Encoding"] = "gzip, deflate"
        header["X-Twitter-Client-DeviceID"] = deviceId if deviceId else getUUID()
        if method == "POST":
            header["Content-Type"] = "application/x-www-form-urlencoded"
            header["Content-Length"] = None
        header["User-Agent"] = "Twitter-iPhone/6.59.3 iOS/9.3.3 (Apple;iPhone8,2;;;;;1)"
        # header["Connection"] = "keep-alive"
        header["X-Twitter-Client-Limit-Ad-Tracking"] = "1"
        header["X-Twitter-API-Version"] = "5"
        header["X-Twitter-Client"] = "Twitter-iPhone"
    elif headerType == 1:
        header["Host"] = url.replace("https://", "").split("/")[0]
        header["Authorization"] = None
        header["X-Twitter-Client-Version"] = "6.59.3"
        header["X-Twitter-Polling"] = "true"
        header["X-Client-UUID"] = uuid if uuid else getUUID()
        header["X-Twitter-Client-Language"] = "ja"
        header["X-B3-TraceId"] = hashlib.md5(str(getCurrentEpochTime()).encode()).hexdigest()[0:16]
        header["x-spdy-bypass"] = "1"
        header["Accept"] = "*/*"
        header["Accept-Language"] = "ja"
        header["Accept-Encoding"] = "gzip, deflate"
        header["X-Twitter-Client-DeviceID"] = deviceId if deviceId else getUUID()
        header["User-Agent"] = "Twitter-iPhone/6.59.3 iOS/9.3.3 (Apple;iPhone8,2;;;;;1)"
        header["X-Twitter-API-Version"] = "5"
        header["X-Twitter-Client-Limit-Ad-Tracking"] = "1"
        header["X-Twitter-Client"] = "Twitter-iPhone"
    elif headerType == 2:
        header["Host"] = url.replace("https://", "").split("/")[0]
        header["Accept"] = "*/*"
        if method == "POST":
            header["Content-Type"] = "application/x-www-form-urlencoded"
            header["Content-Length"] = None
        # header["Connection"] = "keep-alive"
        # header["Proxy-Connection"] = "keep-alive"
        header["Cookie"] = "guest_id=v1:<guest_id>"
        header["Accept-Language"] = "ja"
        header["Authorization"] = None
        # OAuth oauth_nonce="uuid", oauth_signature_method="HMAC-SHA1", oauth_timestamp="timestamp", oauth_consumer_key="WXZE9QillkIZpTANgLNT9g", oauth_token="token", oauth_signature="signature", oauth_version="1.0"
        header["Accept-Encoding"] = "gzip, deflate"
        header["User-Agent"] = "accountsd/113 CFNetwork/758.5.3 Darwin/15.6.0"
    elif headerType == 3:
        header["Host"] = url.replace("https://", "").split("/")[0]
        header["X-B3-TraceId"] = hashlib.md5(str(getCurrentEpochTime()).encode()).hexdigest()[0:16]
        # header["Connection"] = "keep-alive"
        header["X-Twitter-Client-Language"] = "ja"
        # header["Proxy-Connection"] = "keep-alive"
        header["Accept"] = "*/*"
        header["Accept-Language"] = "ja"
        header["Authorization"] = None
        header["Accept-Encoding"] = "gzip, deflate"
        header["User-Agent"] = "Twitter/6.59.3 CFNetwork/758.5.3 Darwin/15.6.0"
    elif headerType == 4:
        header["Host"] = url.replace("https://", "").split("/")[0]
        header["X-Twitter-Client-DeviceID"] = deviceId if deviceId else getUUID()
        header["Authorization"] = None
        header["X-Twitter-Client-Version"] = "6.59.3"
        header["X-Guest-Token"] = None
        header["X-Client-UUID"] = uuid if uuid else getUUID()
        header["X-Twitter-Client-Language"] = "ja"
        header["X-B3-TraceId"] = hashlib.md5(str(getCurrentEpochTime()).encode()).hexdigest()[0:16]
        header["Accept"] = "*/*"
        # header["Proxy-Connection"] = "keep-alive"
        header["Accept-Language"] = "ja"
        header["Accept-Encoding"] = "gzip, deflate"
        if method == "POST":
            header["Content-Type"] = "application/x-www-form-urlencoded"
            header["Content-Length"] = None
        header["User-Agent"] = "Twitter-iPhone/6.59.3 iOS/9.3.3 (Apple;iPhone8,2;;;;;1)"
        # header["Connection"] = "keep-alive"
        header["X-Twitter-Client-Limit-Ad-Tracking"] = "1"
        header["X-Twitter-API-Version"] = "5"
        header["X-Twitter-Client"] = "Twitter-iPhone"
    elif headerType == 5:
        header["Cookie"] = None
        raise NotImplementedError("headerType 5 is not implemented yet.")
    else:
        raise NotImplementedError("No such a headerType found.")
    return header

def makeAuthorizationData(ck, at):
    authorizationData = OrderedDict()
    authorizationData["oauth_signature"] = None
    authorizationData["oauth_nonce"] = getUUID()
    authorizationData["oauth_timestamp"] = str(getCurrentEpochTime())
    authorizationData["oauth_consumer_key"] = ck
    authorizationData["oauth_token"] = at
    authorizationData["oauth_version"] = "1.0"
    authorizationData["oauth_signature_method"] = "HMAC-SHA1"
    return authorizationData

def makeBasicAuthorizationHeader(ck: str, cs: str) -> str:
    return "Basic {}".format(base64.b64encode("{}:{}".format(ck, cs).encode()).decode())

def makeBearerAuthorizationHeader(token: str) -> str:
    return "Bearer {}".format(token)

def makeSignatureBase(method: str, header: Dict, data: Dict, authorizationData: Dict, ck: str, at: str) -> list:
    signatureBase = []
    if (method.upper() == "POST" and header["Content-Type"] == "application/x-www-form-urlencoded") or method.upper() != "POST":
        signatureBase = [[escape(key), escape(value)] for key, value in data.items()]

    signatureBase.append(["oauth_consumer_key", ck])
    signatureBase.append(["oauth_nonce", authorizationData["oauth_nonce"]])
    signatureBase.append(["oauth_signature_method", "HMAC-SHA1"])
    signatureBase.append(["oauth_timestamp", authorizationData["oauth_timestamp"]])
    signatureBase.append(["oauth_version", "1.0"])
    signatureBase.append(["oauth_token", at])
    signatureBase.sort()
    return signatureBase

def makeSigningKey(cs: str, ats: str) -> str:
    return "{}&{}".format(escape(cs), escape(ats))

def makeSignatureBaseString(method: str, url: str, signatureBase: list) -> str:
    return "{}&{}&{}".format(method.upper(), escape(url), escape("&".join(["{}={}".format(key, value) for key, value in signatureBase])))

def makeOAuthSignature(signingKey: str, signatureBaseString: str) -> str:
    return escape(binascii.b2a_base64(hmac.new(signingKey.encode(), signatureBaseString.encode(), hashlib.sha1).digest())[:-1])

def makeAuthorizationHeaderString(authorizationData: Dict) -> str:
    return "OAuth " + ", ".join(["{key}=\"{value}\"".format(key=x, value=y) for x, y in authorizationData.items()])

def makePostString(data: Dict) -> str:
    return "&".join(["{key}={value}".format(key=escape(x), value=escape(y)) for x, y in data.items()])
