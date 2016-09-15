# coding=utf-8
import json
from collections import OrderedDict

from twispy.handler import API
from twispy.request import Request

# put your credentials
# maybe unless use twitter official keys, cannot use apis
ck = "xxx"
cs = "xxx"
at = "xxx"
ats = "xxx"

# if you have uuids
# uuid = "xxx"
# deviceId = "xxx"
uuid = None
deviceId = None

if __name__ == "__main__":
	# if use apis in api.json
	api = API(ck, cs, at, ats, uuid=uuid, deviceId=deviceId)

	# Twitter's polling api checks also data order
	data = OrderedDict()
	data["twitter:string:choice1_label"] = "巨人"
	data["twitter:string:choice2_label"] = "阪神"
	data["twitter:api:api:endpoint"] = "1"
	data["twitter:card"] = "poll2choice_text_only"
	data["twitter:long:duration_minutes"] = 1440
	result = api.cards_create(
		card_data=data
	)
	print(json.dumps(result, sort_keys=False, indent=4))

	# you can override parameters
	result = api.statuses_update(
		card_uri=result["card_uri"],
		status="33-4で優勝したのは？"
	)
	print(json.dumps(result, sort_keys=False, indent=4))

	# if test something new apis
	request = Request(ck, cs, at, ats, uuid=uuid, deviceId=deviceId)

	method = "GET"  # GET or POST or PUT or DELETE
	url = "https://api.twitter.com/1.1/aaa/bbb/ccc.json"
	data = {
		"id": 334
	}  # data(dict) will be automatically converted parameter or post string.
	request.do(method, url, data)
