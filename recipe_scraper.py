import scrapy
import json

all_recipe = open("all_recipes_date.txt", 'w')
data = dict()

class BrickSetSpider(scrapy.Spider):
    name = "recipe_spider"
    start_urls = ['https://veenasvegnation.com/recipe-index/']

    def parse(self, response):
        for recipe in response.xpath('.//div[@class="masonry-grid"]'):
            # get all grid data
            for i in range(2, len(recipe.xpath('.//h3/a/text()'))):
                current = recipe.xpath('./div[' + str(i) + ']')
                print(current.xpath('.//h3/a/text()').extract_first())
                output = current.xpath('.//h3/a/text()').extract_first()
                date = current.xpath('.//div[@class="archive-item-date-posted"]/text()').extract_first()
                cooking_time = current.xpath('.//div[@class="archive-item-meta-cooking-time"]/text()').extract_first()
                solution = [int(s) for s in cooking_time.split() if s.isdigit()]
                if output and date :
                    all_recipe.write(output + "," + str(date) + ",")
                    data[output] = {'name':output, 'date':date}
                if solution:
                    all_recipe.write(str(solution)+',')
                    data[output].update({'time':solution})
                else:
                    all_recipe.write(str(1)+',')
                    data[output].update({'time':1})
                # get category
                category = []
                category_list = len(current.xpath('.//ul[@class="post-categories"]//li'))
                print(category_list)
                for cat in range(category_list):
                    currentCategory = current.xpath('.//ul[@class="post-categories"]/li[' + str(cat+1) + ']/a/text()').extract_first()
                    if currentCategory:
                        all_recipe.write(str(currentCategory)+',')

                all_recipe.write('\n')
                # this is the recipe page

                next_page = current.xpath('.//h3/a/@href').extract_first()
                if next_page:
                    #print("Current index")
                    #print(next_page)
                    yield scrapy.Request(next_page, callback=self.parse_page)

        # done with current page -> move to next
        next_index = response.xpath('.//div[@class="archive-pagination-next"]/a/@href').extract_first()
        #with open("data.json", 'w') as fp:
        #    json.dump(data, fp, indent=4)
        #print(next_index)
        #yield scrapy.Request(next_index, callback=self.parse)

    def parse_page(self, response):
        difficulty = response.xpath('.//li[@class="single-meta-difficulty"]//span/text()').extract_first()
        serves = response.xpath('.//li[@class="single-meta-serves"]//span/text()').extract_first()
        name = response.xpath('//h1/text()').extract_first()
        print("Fill")
        all_recipe.write(name+','+str(difficulty)+","+str(serves)+'\n')
        data[name].update({'difficulty':difficulty, 'serves':serves})
        # now extract the ingredients
        getIngredientTag = response.xpath('.//table[@class="ingredients-table"]')
        ingredients_list = dict()
        ing = []
        qty = []
        for i in range(len(getIngredientTag.xpath('.//tr'))):
            quantity = getIngredientTag.xpath('.//tr['+str(i+1)+']/td[2]/span[1]/text()').extract()
            ingredient = getIngredientTag.xpath('.//tr['+str(i+1)+']/td[2]/span[2]/text()').extract()
            all_recipe.write(str(quantity)+','+str(ingredient)+'\n')
            if quantity and ingredient:
                qty.append(quantity)
                ing.append(ingredient)
        ingredients_list['ingredients'] = {'ingredient':ing, 'quantity':qty}
        data[name].update(ingredients_list)
        with open('data.json', 'w') as fp:
            json.dump(data, fp, indent=4)
