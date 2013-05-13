from import_rozrabiaki_pl import import_latest_jokes
from import_GL_jokes import import_GL_top_jokes
from crawler_settings import SCRAPE_GL_TOP_JOKES, SCRAPE_ROZRABIAKA

def main():
    if SCRAPE_GL_TOP_JOKES:
        import_GL_top_jokes()
    if SCRAPE_ROZRABIAKA:
        import_latest_jokes()

if __name__ == '__main__':
    main()
