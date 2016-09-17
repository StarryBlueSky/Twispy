# coding=utf-8
import requests

from twispy.utils import *


class Request:
	def __init__(self, ck, cs, at, ats, uuid=None, deviceId=None):
		self.ck = ck
		self.cs = cs
		self.at = at
		self.ats = ats
		self.uuid = uuid
		self.deviceId = deviceId

	def do(self, method, url, data=None, headerType=0):
		if not data:
			data = {}

		header = makeHeader(method, url, self.uuid, self.deviceId, headerType)
		authorizationData = makeAuthorizationData(self.ck, self.at)
		signatureBase = makeSignatureBase(method, header, data, authorizationData, self.ck, self.at)
		signatureBaseString = makeSignatureBaseString(method, url, signatureBase)
		signingKey = makeSigningKey(self.cs, self.ats)

		authorizationData["oauth_signature"] = makeOAuthSignature(signingKey, signatureBaseString)
		header["Authorization"] = makeAuthorizationHeader(authorizationData)

		if method.upper() == "GET":
			request = requests.get(url, params=data, headers=header)
		else:
			dataString = "&".join(["{key}={value}".format(key=escape(x), value=escape(y)) for x, y in data.items()])
			header["Content-Length"] = str(len(dataString))
			request = requests.post(url, data=dataString, headers=header)
		result = json.loads(request.text)

		self.header = header
		self.authorizationData = authorizationData
		self.signatureBase = signatureBase
		self.signatureBaseString = signatureBaseString
		self.signingKey = signingKey

		return result
