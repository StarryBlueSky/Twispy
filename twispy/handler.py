# coding=utf-8
import json
import os
from collections import OrderedDict

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
				data = OrderedDict()
				for array in api["data"]:
					key = array[0]
					if key in kwargs:
						data[key] = kwargs[key]
					else:
						data[key] = array[1]
				print(data)
				result = self._do(api["method"], api["url"], data)
				return AttrDict(result)
		return func

class ResponseBody:
	pass
