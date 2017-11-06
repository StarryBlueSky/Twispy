# Twispy
Twispyは, **唯一**の 全Twitter APIエンドポイントに対応した Python製のTwitter APIラッパーです。

ライブラリとは分離したJSONファイルにエンドポイント情報を記述して動的にラップしているので `/api.json`を更新するだけで TwitterのAPI仕様変更に対応できるという 大きな特徴があります。


もし, 動作しないエンドポイントを見つけましたら Issue立てお願いします。

## Intro

### Install & Update

```bash
pip3 install -e "git+https://github.com/NephyProject/Twispy.git#egg=twispy"
```

## Get started

```python
from twispy import API

# Twitter公式クライアントのConsumer Key, Consumer Secretが好ましいです
ck = "IQKbtAYlXLripLGPWd0HUA"
cs = "GgDYlkSvaPxGxC4X8liwpUoqKwwr3lCADbz8A7ADU"
# https://nephy.jp/tools/getauth
at = ""
ats = ""

api = API(ck, cs, at, ats)


# 以下は普通のAPIラッパーではアクセスできないAPIの一例です


# 固定ツイートを登録する
api.account_pin_tweet(
	id=851150296810115072
)
# 固定ツイートを解除する
api.account_unpin_tweet(
	id=851150296810115072
)

# ユーザーの拡張プロフィール(誕生日, Periscope等)を取得
r = api.users_extended_profile(
	screen_name="Twitter"
)
"""
{
    "birthdate": {
        "month": 3,
        "visibility": "public",
        "day": 21,
        "year_visibility": "self"
    },
    "id": 783214,
    "periscope_profile": {
        "web_link": "https://www.pscp.tv/u/1JRKmoXNLWEPy",
        "visible": true,
        "app_link": "pscp://user_id/1JRKmoXNLWEPy",
        "periscope_id": "1JRKmoXNLWEPy"
    },
    "id_str": "783214"
}
"""

# 2ユーザーの関係を取得します
# sourceが自分のときは 公式キー利用時に限り blockされているかorしているか の情報が返却されます
r = api.friendships_show(
        source_screen_name="SlashNephy",
        target_screen_name="Twitter"
)
"""
{
    "relationship": {
        "source": {
            "blocking": false,
            "blocked_by": false,
            "all_replies": false,
            "id": 701282649466245120,
            "live_following": false,
            "following_received": false,
            "can_dm": false,
            "marked_spam": false,
            "muting": false,
            "id_str": "701282649466245120",
            "screen_name": "SlashNephy",
            "followed_by": false,
            "following_requested": false,
            "can_media_tag": true,
            "notifications_enabled": false,
            "want_retweets": false,
            "following": false
        },
        "target": {
            "id_str": "783214",
            "screen_name": "Twitter",
            "followed_by": false,
            "following_requested": false,
            "id": 783214,
            "following": false,
            "following_received": false
        }
    }
}
"""

# フォローしているユーザー限定で「上坂すみれ」を含むツイートを検索します
r = api.search_universal(
	q="上坂すみれ",
	modules="tweet",
	result_type="follows"
)

# 投票ツイートをする
api.create_poll(
	text="おねーちゃん",
	choices=[
		"保登心愛", "天々座理世", "桐間紗路", "宇治松千夜"
	],
	minutes=2880 # 2日間
)

# UserStreamに接続する
def callback(stream):
	if "text" in stream:
		print("{} by @{}".format(stream["text"], stream["user"]["screen_name"]))

	if "event" in stream and "favorite" in stream["event"]:
		print("{} favorited @{}'s `{}`".format(stream["source"]["screen_name"], stream["target"]["screen_name"], stream["target_object"]["text"]))

api.streaming(callback)

# これらの他に twispy/api.json に記されているエンドポイントにすべてアクセスできます
```
