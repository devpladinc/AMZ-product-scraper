from product_scraper import AmazonProductScraper as AMZ

def main():
    #create bot
    bot = AMZ()
    bot.get_data()

if __name__ == "__main__":
    main()