import requests, json, logging, traceback

def PushMessage(summary, content):
    url = "https://wxpusher.zjiecode.com/api/send/message"
    payload = {
        "appToken": "",
        "content": content,
        "summary": summary,
        "contentType": 1,
        "uids": [""]
    }
    payload = json.dumps(payload)
    logging.debug("summary: %s, content: %s.", summary, content)
    header = {"content-type": "application/json"}
    try:
        r = requests.post(url, data = payload, headers = header)
        logging.info(r.text)
    except Exception as e:
        logging.warning("summary: %s, content: %s.", summary, content)
        logging.error("Exception: %s", traceback.format_exc())
    pass

def main():
    #logging.basicConfig(level=logging.INFO)
    #PushMessage("test summary", "test content")
    pass

if __name__ == "__main__":
    main()
