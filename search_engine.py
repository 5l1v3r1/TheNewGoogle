import crawler
from create_pages import Page
from create_website import Website
from create_base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


def from_file_to_list(file):
    f = open(file, "r")
    websites = f.read().split("\n")
    f.close()
    return websites


def fill_database(session, titles, scanned_urls):
    session.add(Website(title=titles[0], url=scanned_urls[0]))
    ID = session.query(Website.id).filter(Website.title == titles[0]).one()
    for count in range(1, len(titles)):
        session.add(Page(title=titles[count], url=scanned_urls[count], website_id=ID[0]))


def crawl(session, websites, titles, urls):
    for item in websites:
        base_url = item
        crawler.scan_page(item, base_url)
        fill_database(session, titles, urls)


def main():
    engine = create_engine("sqlite:///crawl_info.db")
    Base.metadata.create_all(engine)
    session = Session(bind=engine)

    websites = from_file_to_list("the_internet.txt")
    crawl(session, websites, crawler.titles, crawler.scanned_urls)

    session.commit()

if __name__ == "__main__":
    main()
