# coding=utf-8
import binascii
import datetime
import hashlib
import hmac
import time
import urllib.parse
import uuid
from collections import OrderedDict


def escape(text):
	return urllib.parse.quote(text, safe="~")

def getCurrentEpochTime():
	return int(time.mktime(datetime.datetime.now().timetuple()))

def getUUID():
	return str(uuid.uuid4()).upper()

def makeHeader(url, uuid=None, deviceId=None):
	header = OrderedDict()
	header["Host"] = url.replace("https://", "").split("/")[0]
	header["Authorization"] = None
	header["X-Twitter-Client-Version"] = "6.59.3"
	header["Accept"] = "*/*"
	header["X-Client-UUID"] = uuid if uuid else getUUID()
	header["X-Twitter-Client-Language"] = "ja"
	header["X-B3-TraceId"] = hashlib.md5(str(getCurrentEpochTime()).encode()).hexdigest()[0:16]
	header["Accept-Language"] = "ja"
	header["Accept-Encoding"] = "gzip, deflate"
	header["X-Twitter-Client-DeviceID"] = deviceId if deviceId else getUUID()
	header["User-Agent"] = "Twitter-iPhone/6.59.3 iOS/9.3.3 (Apple;iPhone8,2;;;;;1)"
	header["X-Twitter-Client-Limit-Ad-Tracking"] = "1"
	header["X-Twitter-API-Version"] = "5"
	header["X-Twitter-Client"] = "Twitter-iPhone"
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

def makeSignatureBase(method, header, data, authorizationData, ck, at):
	signatureBase = []
	if (method.upper() == "POST" and header.get("Content-Type") == "application/x-www-form-urlencoded") or method.upper() != "POST":
		for key, value in data.items():
			signatureBase.append([escape(key), escape(value)])

	signatureBase.append(["oauth_consumer_key", ck])
	signatureBase.append(["oauth_nonce", authorizationData["oauth_nonce"]])
	signatureBase.append(["oauth_signature_method", "HMAC-SHA1"])
	signatureBase.append(["oauth_timestamp", authorizationData["oauth_timestamp"]])
	signatureBase.append(["oauth_version", "1.0"])
	signatureBase.append(["oauth_token", at])
	signatureBase.sort()
	return signatureBase

def makeSignatureBaseString(method, url, signatureBase):
	return "{}&{}&{}".format(method.upper(), escape(url), escape("&".join(["{}={}".format(key, value) for key, value in signatureBase])))

def makeSigningKey(cs, ats):
	return "{}&{}".format(escape(cs), escape(ats))

def makeOAuthSignature(signingKey, signatureBaseString):
	return escape(binascii.b2a_base64(hmac.new(signingKey.encode(), signatureBaseString.encode(), hashlib.sha1).digest())[:-1])

def makeAuthorizationHeader(authorizationData):
	return "OAuth " + ", ".join(["{key}=\"{value}\"".format(key=x, value=y) for x, y in authorizationData.items()])
