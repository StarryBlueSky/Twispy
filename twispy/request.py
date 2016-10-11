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

	def do(self, method, url, data=None, headerType=0, authorizationType=0, bearerToken=None):
		method = method.upper()
		if not data:
			data = {}

		header = makeHeader(method, url, self.uuid, self.deviceId, headerType)

		if authorizationType == 0:
			authorizationData = makeAuthorizationData(self.ck, self.at)
			signatureBase = makeSignatureBase(method, header, data, authorizationData, self.ck, self.at)
			signatureBaseString = makeSignatureBaseString(method, url, signatureBase)
			signingKey = makeSigningKey(self.cs, self.ats)

			authorizationData["oauth_signature"] = makeOAuthSignature(signingKey, signatureBaseString)
			header["Authorization"] = makeAuthorizationHeader(authorizationData)
		elif authorizationType == 1:
			header["Authorization"] = makeBasicAuthorizationHeader(self.ck, self.cs)
		elif authorizationType == 2:
			header["Authorization"] = makeBearerAuthorizationHeader(bearerToken)
		elif authorizationType == 3:
			header["Cookie"] = None
			raise NotImplementedError("authorizationType 3 is not implemented yet.")
		else:
			raise NotImplementedError("This authorizationType was not supported.")

		if method == "GET":
			request = requests.get(url, params=data, headers=header)
		elif method == "POST":
			postString = makePostString(data)
			header["Content-Length"] = str(len(postString))
			request = requests.post(url, data=postString, headers=header)
		else:
			raise NotImplementedError("This method was not supported.")
		result = json.loads(request.text)

		return result

	def streaming(self, callback, data=None):
		method = "GET"
		url = "https://userstream.twitter.com/1.1/user.json"
		if not data:
			data = {
				"replies": "all",
				"filter_level": "none",
				"include_followings_activity": "True",
				"stall_warnings": "True",
				"with": "followings"
			}

		header = makeHeader(method, url, self.uuid, self.deviceId, 0)
		authorizationData = makeAuthorizationData(self.ck, self.at)
		signatureBase = makeSignatureBase(method, header, data, authorizationData, self.ck, self.at)
		signatureBaseString = makeSignatureBaseString(method, url, signatureBase)
		signingKey = makeSigningKey(self.cs, self.ats)
		authorizationData["oauth_signature"] = makeOAuthSignature(signingKey, signatureBaseString)
		header["Authorization"] = makeAuthorizationHeader(authorizationData)

		stream = requests.get(url, params=data, headers=header, stream=True)
		for line in stream.iter_lines():
			if not line:
				continue
			line = line.decode()

			try:
				jsonObj = json.loads(line)
			except:
				raise Exception("failed to decode json. reserved data was `{}`.".format(line))
			callback(jsonObj)
