import argparse
import re
import requests
from bs4 import BeautifulSoup
from utils import normalize_text

BASE_URL = "https://factcheck.snu.ac.kr/v2/facts/{}"
FACTLIST_URL = "https://factcheck.snu.ac.kr/v2/facts?page={}&score={}"


def parse_page_by_id(id):
    res = {"id": str(id)}
    url = BASE_URL.format(id)
    try:
        req = requests.get(url)
        soup = BeautifulSoup(req.text, 'html.parser')
        title, source = [s.get_text() for s in soup.select(".fcItem_detail_li_p > p")]
        content = soup.select_one('div.fcItem_detail_exp > p.exp').get_text()
        res.update({"title": title, "source": source, "content": content})
    except:
        return res, False

    res = {k: normalize_text(v) for k, v in res.items() if isinstance(v, str)}
    return res, True


def main(args):   
    res = []
    count = 0
    for score in range(6): 
        """ # score == 6 """
        page = 1
        while True:
            url = FACTLIST_URL.format(page, score)
            req = requests.get(url)
            soup = BeautifulSoup(req.text, 'html.parser')

            ids = [a['href'].split('/')[3] for a in soup.select("a.btn_detail")]
            if not ids:
                break
            
            for id in ids:
                parsed, ok = parse_page_by_id(id)
                if ok:
                    parsed.update({"score": score})
                    res.append(parsed)
                    count += 1 
                
                    if args.verbose and count % args.steps == 0:
                        print("\n#[+] count {}, score {}, page {}\n title: {}".format(
                                count, score, page, parsed['title']))
            page += 1
    
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--score", default=0)
    parser.add_argument("--verbose", default=True)
    parser.add_argument("--steps", default=10)
    parser.add_argument("--output", default="./snufc/output.txt")
    args = parser.parse_args()
    main(args)