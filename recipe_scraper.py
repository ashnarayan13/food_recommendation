import scrapy
import json
import re

rewrite = dict()
save_url = open('recipe.txt', 'w')

class BrickSetSpider(scrapy.Spider):
    name = "recipe_spider"
    start_urls = ['https://veenasvegnation.com/recipe-index/']

    def parse(self, response):
        for recipe in response.xpath('.//div[@class="masonry-grid"]'):
            # get all grid data
            print(len(recipe.xpath('.//h3/a/text()')))
            for i in range(1, len(recipe.xpath('.//h3/a/text()'))+1):
                current = recipe.xpath('./div[' + str(i+1) + ']')
                print(current.xpath('.//h3/a/text()').extract_first())
                output = current.xpath('.//h3/a/text()').extract_first()
                date = current.xpath('.//div[@class="archive-item-date-posted"]/text()').extract_first()
                cooking_time = current.xpath('.//div[@class="archive-item-meta-cooking-time"]/text()').extract_first()
                if cooking_time:
                    solution = [int(s) for s in re.findall(r'-?\d+', cooking_time)]
                    rewrite.setdefault('time', []).append(solution[0])
                else:
                    rewrite.setdefault('time', []).append(1)
                if output and date :
                    rewrite.setdefault('name', []).append(output.lower())
                    rewrite.setdefault('date', []).append(date)
                # get category
                category = []
                category_list = len(current.xpath('.//ul[@class="post-categories"]//li'))
                print(category_list)
                for cat in range(category_list):
                    currentCategory = current.xpath('.//ul[@class="post-categories"]/li[' + str(cat+1) + ']/a/text()').extract_first()
                    if currentCategory:
                        category.append(currentCategory.lower())
                if len(category):
                    rewrite.setdefault('category',[]).append(category)
                else:
                    rewrite.setdefault('category',[]).append(['unknown'])

                # this is the recipe page

                next_page = current.xpath('.//h3/a/@href').extract_first()
                if next_page:
                    self.crawler.engine.schedule(scrapy.Request(next_page, callback=self.parse_page), self)

        # done with current page -> move to next
        next_index = response.xpath('.//div[@class="archive-pagination-next"]/a/@href').extract_first()
        #print(next_index)
        yield scrapy.Request(next_index, callback=self.parse)

    def parse_page(self, response):
        difficulty = response.xpath('.//li[@class="single-meta-difficulty"]//span/text()').extract_first()
        if difficulty:
            rewrite.setdefault('difficulty', []).append(difficulty.lower())
        else:
            rewrite.setdefault('difficulty', []).append('unknown')
        serves = response.xpath('.//li[@class="single-meta-serves"]//span/text()').extract_first()
        name = response.xpath('.//h1/text()').extract_first()
        if serves:
            ser = [int(s) for s in re.findall(r'-?\d+', serves)]
            rewrite.setdefault('serves', []).append(ser[0])
        else:
            rewrite.setdefault('serves', []).append(1)
        print("Fill")

        # now extract the ingredients
        getIngredientTag = response.xpath('.//table[@class="ingredients-table"]')
        ing = []
        qty = []
        ing.append(name.lower())
        qty.append(0)
        for i in range(len(getIngredientTag.xpath('.//tr'))):
            quantity = getIngredientTag.xpath('.//tr['+str(i+1)+']/td[2]/span[1]/text()').extract_first()
            ingredient = getIngredientTag.xpath('.//tr['+str(i+1)+']/td[2]/span[2]/text()').extract_first()
            if quantity and ingredient:
                qty.append(quantity)
                ing.append(ingredient.lower())
        if len(qty) and len(ing):
            rewrite.setdefault('quantity', []).append(qty)
            rewrite.setdefault('ingredient', []).append(ing)
        with open('rewrite.json', 'w') as fp:
            json.dump(rewrite, fp, indent=4)
