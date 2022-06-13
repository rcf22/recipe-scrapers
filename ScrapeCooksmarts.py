from recipe_scrapers import scrape_me
from fractions import Fraction

def scaleQty(qty, scaler, units):
    scaledQty = float(sum(Fraction(s) for s in qty.split()))/scaler
    #print('Orig: ' + qty + ', Scaled: ' + str(scaledQty))
    return round(scaledQty, 2)

#def convertUnits(qty, units):
#    return float(sum(Fraction(s) for s in qty.split()))
    
# give the url as a string, it can be url from any site listed below
scraper = scrape_me('https://mealplans.cooksmarts.com/days/1488')

carbsDivisor = 2

print(scraper.title())
ingList = scraper.ingredients()
nutrList = scraper.nutrition()
servings = scraper.yields()

ingAmountDivisor = int(servings)*2
#print(convertUnits("1"))
#print(convertUnits("1/8"))
#print(convertUnits("8 1/3"))

for nutrIng in nutrList:
    name = nutrIng[0]
   
    for ing in ingList:
        ingDict = eval(ing)
        
        if (ingDict['Ingredient'] == name):
            # Matched an ingredient to a nutrition fact entry
            # Scale the amount/carbs to half serving and print if > 0.5g carbs
            
            scaledCarbs = nutrIng[1] / carbsDivisor
            if (scaledCarbs > 0.5):
                scaledQty = scaleQty(ingDict['Qty'], ingAmountDivisor, ingDict['Units'])
                print(str(scaledQty) + " " + ingDict['Units'] + " " + nutrIng[0] + ": " + str(scaledCarbs) + " g")
