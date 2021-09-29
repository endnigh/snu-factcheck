import re
import requests
from bs4 import BeautifulSoup


BASE_URL = "https://factcheck.snu.ac.kr/v2/facts/{}"
FACTLIST_URL = "https://factcheck.snu.ac.kr/v2/facts?page={}&score={}"



def main(args):
    res = []
    count = 0
    for score in range(6): 
        """ # score == 6 """
        page = 1
        while True:
            url = FACTLIST_URL.format(page, score)
            req = requests.get(url)
            soup = BeautifulSoup(req.text, 'lxml')

            ids = [a['href'].split('/')[3] for a in soup.select("a.btn_detail")]
            if not hrefs:
                break
            
            for id in ids:
                parsed, ok = parse_page_by_id(id)
                if ok:
                    parsed["score"] = score
                    res.append(parsed)
                    count += 1 
                
                if args.verbose:
                    print(
                        "\n# score {}, page {}\n title: {}".format(score, page, parsed['title'])
                    )
            page += 1

    return res
