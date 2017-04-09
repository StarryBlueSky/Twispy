# coding=utf-8
import json
import os
from collections import OrderedDict
from typing import List, Dict, Union

from twispy.request import Request

with open(os.path.abspath(os.path.dirname(__file__)) + "/api.json", "rb") as f:
    api_dict = json.loads(f.read().decode())

class API:
    __slots__ = list(api_dict.keys()) + ["_request", "_do", "streaming"]

    def __init__(self, ck, cs, at, ats, uuid=None, deviceId=None):
        self._request = Request(ck, cs, at, ats, uuid, deviceId)
        self._do = self._request.do
        self.streaming = self._request.streaming

    def __getattr__(self, name):
        def func(**kwargs) -> Union[List, Dict]:
            if name in api_dict:
                api = api_dict[name]

                data = OrderedDict()
                for array in api["data"]:
                    key, value = array[0:2]
                    data[key] = value

                    if key in kwargs:
                        data[key] = str(kwargs[key])

                    if data[key] == False:
                        # optional argument
                        del data[key]
                        continue
                    if data[key] == None:
                        # necessary argument
                        raise Exception("{} must have non-null parameter.".format(key))

                result = self._do(api["method"], api["url"], data, headerType=api["headerType"], authorizationType=api["authorizationType"])
                return result

            raise AttributeError("No such a method found.")

        return func

    @staticmethod
    def default_callback(stream) -> None:
        print(json.dumps(stream, indent=4))

    def create_poll(self, text: str, choices: List[str], minutes=1440) -> Dict:
        """
        Create Twitter poll tweet. CK/CS must be Twitter Official Keys.
        :param text: Tweet content
        :param choices: List[str]: 
        :param minutes: how long this poll lasts (minute)
        :return: status object
        """

        if len(choices) not in [2, 3, 4]:
            raise Exception("choices must has 2 to 4")

        params = OrderedDict()
        for i in range(len(choices)):
            params["twitter:string:choice{}_label".format(i + 1)] = choices[i]
        params["twitter:api:api:endpoint"] = "1"
        params["twitter:card"] = "poll{}choice_text_only".format(len(choices))
        params["twitter:long:duration_minutes"] = minutes

        r = self.cards_create(
            card_data=json.dumps(params)
        )

        if "card_uri" not in r:
            raise Exception("API returned an error.\nAPI response: {}\n".format(repr(r)))

        return self.statuses_update(
            status=text,
            card_uri=r["card_uri"]
        )
