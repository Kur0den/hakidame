import requests
import sys

url = "WEBHOOK_URL"

hash = sys.argv[1]
files = sys.argv[2]
added_bytes = sys.argv[3]
removed_bytes = sys.argv[4]
author = sys.argv[5]
commit_message = sys.argv[6]

# 制限回避のために文字数をカウント
count = 0
status_data = ""
for line in files.split('\n'):
    if line:
        status, file = line.split('\t')
        match status:
            case "A":
                status = "+"
            case "D":
                status = "-"
        count += len(status) + len(file) + 1
        status_data += f"{status} {file}\n"
        if count > 4070:
            status_data += "他多数のファイル"
            break



data = {
    "content": "<@&1270581745615372461> あたらしいcommitだよ！",
    "embeds": [
    {
        "id": 66608588,
        "description": "```diff\n" + status_data + "```",
        "fields": [
                {
                "name": "容量変化",
                "value": f"```diff\n+ {added_bytes}\n- {removed_bytes}\n```",
                "inline": False
                }
            ],
        "title": "New Commit",
        "timestamp": "2024-08-16T15:00:00.000Z",
        "footer": {
            "text": author
        },
        "author": {
            "name": hash
        },
        "color": 25600
        }
    ],
    "components": [],
    "actions": {},
    "username": "Commit通知ちゃん"
}

requests.post(url, json=data)
