import requests
import sys
from datetime import datetime

url = "https://canary.discord.com/api/webhooks/1279016777430601800/hkzbbo9z782ch8IP0CyIIohppoF5GMWh0VKbTx2H-u8V1PwORm_wliQOnRKRyqVpw5_y"

log = sys.argv[1]
author = sys.argv[2]

# 制限回避のために文字数をカウント
print(log)
if len(log) > 4070:
    cut_index = log.rfind('\n', 0, 4070)
    if cut_index == -1:
        cut_index = 4070
    log = log[:4070] + "\nその他多数のcommit"



data = {
    "content": "<@&1270581745615372461> あたらしいDeployだよ！",
    "embeds": [
    {
        "id": 66608588,
        "description": f"```\n{log}\n```",
        "title": "New Deploy",
        "timestamp": datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
        "footer": {
            "text": "実行者: " + author
        },
        "color": 25600
        }
    ],
    "components": [],
    "actions": {},
    "username": "Deploy通知ちゃん"
}

requests.post(url, json=data)
