#from ._abstract import CookSmartsScraper
from ._abstract import *
from ._utils import normalize_string
import re
import requests
import json
from operator import itemgetter

minCarbs = 0.9

class CookSmarts(CookSmartsScraper):
    @classmethod
        
    def host(cls):
        return "mealplans.cooksmarts.com"

    def author(self):
        #return self.schema.author()
        return ""

    def title(self):
        return normalize_string(self.soup.find("h1", {"class": "recipe__name"}).get_text())
        #return self.soup.select_one("h1 .recipe__name")
        
    def category(self):
        #return self.schema.category()
        return ""

    def total_time(self):
        #return self.schema.total_time()
        return ""

    def yields(self):
        #print(self.soup.find("Servings:").content)
        return ""

    def image(self):
        #return self.schema.image()
        return ""

    def ingredients(self):
        
        ingList = self.soup.find("ul", {"class": "recipe__ingredients"}).find_all("li")
        cleanIngList = []
        for each in ingList:
            ing = {}
            cleanEach = normalize_string(each.get_text())
            name = cleanEach[0: cleanEach.find(" - ")]
            amount = cleanEach[cleanEach.find(" - ")+3 : len(cleanEach)]
            
            match = re.search('[a-zA-Z]', amount)
            qty = amount[0 : match.start()-1]
            units = ""
            if (qty.find(",") != -1):
                #If qty has a comma, then there was no unit and we need to strip the comma
                qty = qty.split(',')[0]
                units = "items"
                
            match = re.search('^[^a-zA-Z]+(.*)', amount)
            if (amount.find(",") != -1):
                if (units == ""):
                    units = match[1].split(',')[0]
                    if (units.find("(") != -1):
                        units = match[1].split('(')[0]

                preparation = amount[amount.find(",")+2 : len(amount)]
            else:
                if (units == ""):
                    units = match[1]
                preparation = ""
            
            ing = {
                    'Ingredient': name,
                    'Qty': qty,
                    'Units': units,
                    'Preparation': preparation
                  }
                  
            cleanIngList.append(ing)
            
        return cleanIngList

    def instructions(self):
        #return self.schema.instructions()
        return ""

    def ratings(self):
        #return self.schema.ratings()
        return ""

    def cuisine(self):
        #return self.schema.cuisine()
        return ""

    def description(self):
        #return self.schema.description()
        return ""
        
    def nutrition(self):
        carbsUrl = self.url + "/nutrition_top_sources?nutrient=total_carbs&view=standard"
        carbsHtml = requests.get(carbsUrl, headers=COOKSMARTS_HEADERS, cookies=COOKIES).content
        carbSoup = BeautifulSoup(carbsHtml, "html.parser")
        
        carbsList = []
        
        for each in carbSoup.find_all("div", {"class": "facts__details-row"}):
            cleanEach = normalize_string(each.get_text())
            
            ing = normalize_string(each.contents[0])
            
            carbs = normalize_string(each.find("span").get_text())
            if carbs.find("<") != -1:
                carbs = 0
            else:
                carbs = int(carbs[0 : len(carbs)-1])
                
            if (carbs > minCarbs):
                carbsList.append([ing, carbs])
        
        return sorted(carbsList, key=itemgetter(1), reverse=True)
