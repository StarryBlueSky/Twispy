# coding=utf-8
import json
import os
from collections import OrderedDict

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
					key, value = array
					if value == False:
						# optional argument
						continue
					if value == None:
						# necessary argument
						raise Exception("{} must have non-null parameter.".format(key))
					data[key] = value

					if key in kwargs:
						data[key] = kwargs[key]

				result = self._do(api["method"], api["url"], data, headerType=api["headerType"])
				return result

			raise AttributeError("No such a method.")

		return func
