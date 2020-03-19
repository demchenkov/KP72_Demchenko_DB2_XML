from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lxml import etree
import os
import webbrowser


def cleanup():
    try:
        os.remove("../documents/tsn.xml")
        os.remove("../documents/wallet.xml")
        os.remove("../documents/wallet.xhtml")
    except OSError:
        pass


def scrap_data():
    process = CrawlerProcess(get_project_settings())
    process.crawl('tsn')
    process.crawl('wallet')
    process.start()


def tsn_task():
    root = etree.parse("../documents/tsn.xml")
    pages = root.xpath("//page")
    min_img = pages[0].xpath("count(fragment[@type='image'])")
    for page in pages:
        url = page.xpath("@url")[0]
        count = page.xpath("count(fragment[@type='image'])")
        if count < min_img:
            min_img = count
        print("%s: %d" % (url, count))
    print("Minimal count: ", min_img)


def wallet_task():
    transform = etree.XSLT(etree.parse("wallet.xsl"))
    result = transform(etree.parse("../documents/wallet.xml"))
    result.write("../documents/wallet.xhtml", pretty_print=True, encoding="UTF-8")
    webbrowser.open('file://' + os.path.realpath("../documents/wallet.xhtml"))


if __name__ == '__main__':
    cleanup()
    print("Scrapping...")
    scrap_data()
    print("Scrapping finished.")
    while True:
        print("_" * 40)
        print("1) Minimal count of images on pages of tsn.ua")
        print("2) Products on wallet.ua")
        print("Enter number of task:", end='', flush=True)
        number = input()
        print("_" * 40)
        if number == "1":
            tsn_task()
        elif number == "2":
            wallet_task()
        else:
            break
