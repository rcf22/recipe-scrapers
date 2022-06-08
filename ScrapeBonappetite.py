from recipe_scrapers import scrape_me

# give the url as a string, it can be url from any site listed below
scraper = scrape_me('https://www.bonappetit.com/recipe/sizzling-pork-and-eggplant-hiyayakko')

print(scraper.title())
print(scraper.ingredients())