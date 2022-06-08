from recipe_scrapers import scrape_me

# give the url as a string, it can be url from any site listed below
scraper = scrape_me('https://mealplans.cooksmarts.com/days/1488')

print(scraper.title())