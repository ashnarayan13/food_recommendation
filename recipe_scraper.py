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
                if output and date:
                    data[str(output)] = {'date':date, 'name':output}
                    all_recipe.write(output + " " + str(date) + str('\n'))
                # this is the recipe page

                next_page = current.xpath('.//h3/a/@href').extract_first()
                if next_page:
                    #print("Current index")
                    #print(next_page)
                    yield scrapy.Request(next_page, callback=self.parse_page)

        # done with current page -> move to next
        next_index = response.xpath('.//div[@class="archive-pagination-next"]/a/@href').extract_first()
        #print(next_index)
        #yield scrapy.Request(next_index, callback=self.parse)

    def parse_page(self, response):
        difficulty = response.xpath('.//li[@class="single-meta-difficulty"]//span/text()').extract_first()
        serves = response.xpath('.//li[@class="single-meta-serves"]//span/text()').extract_first()
        print("Fill")
        data.update({'difficulty':difficulty, 'serves':serves})
        print(data)
        with open('test.json', 'w') as fp:
            json.dump(data, fp, indent=4)
        # now extract the ingredients
        getIngredientTag = response.xpath('.//table[@class="ingredients-table"]')
        '''for i in range(len(getIngredientTag.xpath('.//tr'))):
            print(getIngredientTag.xpath('.//tr['+str(i+1)+']/td[2]/span[1]/text()').extract())
            print(getIngredientTag.xpath('.//tr['+str(i+1)+']/td[2]/span[2]/text()').extract())'''
