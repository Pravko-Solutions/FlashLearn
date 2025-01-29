import requests


class SimpleGoogleSearch:
    def __init__(self, api_key, cse_id):
        self.api_key = api_key
        self.cse_id = cse_id
    def search(self, queries):
        r = []
        for q in queries:
            p = {"key": self.api_key, "cx": self.cse_id, "q": q}
            r.append(requests.get("https://www.googleapis.com/customsearch/v1", params=p).json())
        return r
