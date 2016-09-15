# coding=utf-8
import json
import os

from attrdict import AttrDict

from twispy.request import Request

with open(os.path.abspath(os.path.dirname(__file__)) + "/api.json") as f:
	api_dict = json.load(f)

class API(object):
	__slots__ = list(api_dict.keys()) + ["_do"]

	def __init__(self, ck, cs, at, ats, uuid=None, deviceId=None):
		self._do = Request(ck, cs, at, ats, uuid, deviceId).do

	def __getattr__(self, name):
		def func(**kwargs):
			if name in api_dict:
				api = api_dict[name]
				data = api["data"]
				for key, value in api["data"]:
					if key in kwargs:
						data[key] = kwargs[key]
				result = self._do(api["method"], api["url"], data)
				return AttrDict(result)
		return func

class ResponseBody:
	pass
