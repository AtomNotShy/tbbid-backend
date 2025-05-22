import requests
if __name__ == '__main__':
    import requests

    url = "https://data.ggzy.gov.cn/yjcx/index/search"

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://data.ggzy.gov.cn",
        "Referer": "https://data.ggzy.gov.cn/portal_legal/companyPer.html",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36",
        # 注意：可选，不加也能返回数据，必要时加上从浏览器中复制的 Cookie
        "Cookie": "Path=/; Path=/; PHPSESSID=8dj3lilorhla7e6du3e9grnroc; insert_cookie=38491973"
    }

    data = {
        "keyword": "四川宝鑫建设有限公司",
        "page": "1"
    }

    # 如果你走的是本地代理（如 Clash 开启了 7890）
    proxies = {
        "http": "http://127.0.0.1:7890",
        "https": "http://127.0.0.1:7890",
    }

    response = requests.post(url, headers=headers, json=data,  timeout=10)

    # 打印返回 JSON
    print(response.status_code)
    print(response.json())




