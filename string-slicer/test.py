import unicodedata
import websockets
import json
import asyncio
from uuid import uuid4

def check(name):
    named = ""
    for n in name:
        named += unicodedata.east_asian_width(n)
    return named

def count(name):
    count = 0
    for char in name:
        match unicodedata.east_asian_width(char):
            case "W" | "F":
                count += 2
            case "a":
                pass
            case _:
                count += 1
    return count

def name_formatter(name, count, config):
    TARGET_LEN = config["name_len"] - len("... ")
    name_len = count
    print("target:", TARGET_LEN)
    for char in name[::-1]:
        match unicodedata.east_asian_width(char):
            case "W" | "F":  # 全角文字
                name_len -= 2  # 2文字分減らす
                name = name[:-1]
            case "a":  # 曖昧な文字
                pass  # 何もしない
            case _: # その他
                name_len -= 1 # 1文字分減らす
                name = name[:-1]
        print(name, char, name_len)
        if name_len <= TARGET_LEN:
            break
    format_name = name + "... "
    # if name_len != TARGET_LEN:
    #     print("Filling with spaces")
    #     print(TARGET_LEN - name_len)
    #     name += " " * (TARGET_LEN - name_len)
    return format_name


async def main():
    config = json.load(open("./config.json", "r"))
    unique_id = str(uuid4())
    async with websockets.connect(
        f"wss://{config['instance']}/streaming?i={config['token']}"
    ) as ws:
        await ws.send(
            json.dumps({"type": "connect", "body": {"channel": "homeTimeline", "id": unique_id}})
        )
        print("connected")
        print("=" * config["line_len"])
        while True:
            res = json.loads(await ws.recv())
            if res["body"].get("id") == unique_id:
                res = res["body"]["body"]
                name = res["user"]["name"] if res["user"]["name"] is not None else res["user"]["username"]
                print(check(name))
                print(name)
                print("-")
                c = count(name=name)
                print("raw:", len(name))
                print("count:", c)
                print("-")
                if config["name_len"] - c < 0:
                    format_name = name_formatter(name, c, config)
                else:
                    format_name = name
                format_name = format_name + " " * (config["name_len"] - count(format_name))
                print(format_name + "|")
                print("-")
                print("space:", config["name_len"] -c)
                print("formatLen:", count(format_name))
                print("configLen:", config["name_len"])
                print("-" * config["line_len"])



if __name__ == "__main__":
    asyncio.run(main())
