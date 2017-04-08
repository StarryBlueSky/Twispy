# Twispy
Twispyは, **唯一**の 全Twitter APIエンドポイントに対応した Python製のTwitter APIラッパーです。


もし, 動作しないエンドポイントを見つけましたら Issue立てお願いします。

## Get started

```python
from twispy.handler import API, Request

# Twitter公式クライアントのConsumer Key, Consumer Secretが好ましい
ck = "IQKbtAYlXLripLGPWd0HUA"
cs = "GgDYlkSvaPxGxC4X8liwpUoqKwwr3lCADbz8A7ADU"
# https://nephy.jp/tools/getauth
at = ""
ats = ""

api = API(ck, cs, at, ats)
request = Request(ck, cs, at, ats)

# フォローしているユーザー限定で「上坂すみれ」を含むツイートを検索します
r = api.search_universal(
	q="上坂すみれ",
	modules="tweet",
	result_type="follows"
)

# 投票ツイート (API側で順序チェックが行われるので厳密に順序を守る)
from collections import OrderedDict
params = OrderedDict()
params["twitter:string:choice1_label"] = "保登心愛"
params["twitter:string:choice2_label"] = "天々座理世"
params["twitter:string:choice3_label"] = "桐間紗路"
params["twitter:string:choice4_label"] = "宇治松千夜"
params["twitter:api:api:endpoint"] = "1"
params["twitter:card"] = "poll4choice_text_only"
params["twitter:long:duration_minutes"] = 1440

import json
r = api.cards_create(
	card_data=json.dumps(params)
)
r = api.statuses_update(
	status="投票テスト",
	card_uri=r["card_uri"]
)

# UserStream に接続
def callback(stream):
	if "text" in stream:
		print("{} by @{}".format(stream["text"], stream["user"]["screen_name"]))

	if "event" in stream and "favorite" in stream:
		print("{} favorited @{}'s `{}`".format(stream["source"]["screen_name"], stream["target"]["screen_name"], stream["target_object"]["text"]))

request.streaming(callback)

# これらの他に twispy/api.json に記されているエンドポイントにすべてアクセスできます
```
