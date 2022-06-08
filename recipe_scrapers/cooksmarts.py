from ._abstract import AbstractScraper


class Template(AbstractScraper):
    @classmethod
		
    def host(cls):
        return "cooksmarts.com"

    def author(self):
        #return self.schema.author()
        return ""

    def title(self):
		self.soup.find(class="recipe__name").get_text()
        #return self.schema.title()
        return ""

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
