from ._abstract import CookSmartsScraper
from ._utils import normalize_string

class CookSmarts(CookSmartsScraper):
    @classmethod
        
    def host(cls):
        return "mealplans.cooksmarts.com"

    def author(self):
        #return self.schema.author()
        return ""

    def title(self):
        #return self.soup.select_one("h1 .recipe__name")
        return normalize_string(self.soup.find("h1", {"class": "recipe__name"}).get_text())
		
    def category(self):
        #return self.schema.category()
        return ""

    def total_time(self):
        #return self.schema.total_time()
        return ""

    def yields(self):
        #return self.schema.yields()
        return ""

    def image(self):
        #return self.schema.image()
        return ""

    def ingredients(self):
        #return self.schema.ingredients()
        return ""

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
