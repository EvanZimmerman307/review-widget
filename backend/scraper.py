import requests
from bs4 import BeautifulSoup

def is_captcha(title):
    captcha_keywords = ['Robot or human?', 'Activate and hold the button', 'confirm that you’re human']
    return any(keyword in title for keyword in captcha_keywords)

def fetch_product_info(url):
    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status()  # Raise an error for bad responses
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        
        title = soup.title.string
        # description = soup.find('meta', attrs={'name': 'description'})['content']
        # Check if the page is a captcha page
        if is_captcha(title):
            raise Exception("This page is a captcha page")

        description = [p.get_text(strip=True) for p in soup.find_all('p')]
        title = [p.get_text(strip=True) for p in soup.find_all('h1')]
        
    except requests.Timeout:
        raise Exception("The request timed out")

    except requests.TooManyRedirects:
        raise Exception("Too many redirects")

    except requests.RequestException as e:
        raise Exception("Request Exception")
       
    return title, description


if __name__ == "__main__":
    urls= [
        "https://kith.com/collections/kith-footwear/products/x2j162xf85500",
        "https://www.amazon.com/eos-Cashmere-Moisture-Lightweight-Non-Greasy/dp/B08KT2Z93D/?_encoding=UTF8&pd_rd_w=a3wu2&content-id=amzn1.sym.aeef70de-9e3e-4007-ae27-5dbb7b4a72f6&pf_rd_p=aeef70de-9e3e-4007-ae27-5dbb7b4a72f6&pf_rd_r=21NA7K6QEXX5X2F6N2KM&pd_rd_wg=l7cK3&pd_rd_r=903996a9-0eaa-4382-bfac-680c67cfe909&ref_=pd_hp_d_btf_crs_zg_bs_3760911",
        #"https://www.walmart.com/ip/Austin-Peanut-Butter-on-Cheese-Sandwich-Crackers-Single-Serve-Snack-Crackers-20-Count/1837462801?classType=REGULAR&athbdg=L1600&adsRedirect=true",
        #"https://www.meijer.com/shopping/product/sony-zx-series-stereo-headphones-black/2724286708.html",
        #"https://us.shein.com/SHEIN-EZwear-Women-s-Hooded-Sweatshirt-With-Slogan-Print-And-Kangaroo-Pocket-FAITH-OVER-FEAR-PSALM-563-p-29621449.html?src_identifier=uf=usbingsearch09_cheaptrendyclothes02_20220804&src_module=ads&mallCode=1&pageListType=4&imgRatio=3-4",
        "https://www.gap.com/browse/product.do?pid=538469002&rrec=true&mlink=5001,1,home_gaphome2_rr_0&clink=1",
        "https://www.target.com/p/marvel-youth-spider-man-halloween-costume/-/A-90605950?preselect=90599841#lnk=sametab",
        "https://www.nike.com/t/ja-2-basketball-shoes-zNhj0Q/FD7328-500"
    ]
    for url in urls:
        title, description = fetch_product_info(url)
        print(f"Title: {title}")
        print(f"Description: {description}")
