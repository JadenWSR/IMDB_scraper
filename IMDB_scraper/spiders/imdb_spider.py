# to run 
# scrapy crawl imdb_spider -o movies.csv

from gc import callbacks
import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    
    start_urls = ['https://www.imdb.com/title/tt5834204/']

    def parse(self, response):
        """
        Assumptions: Sart on a movie page, and then navigate to the Cast & Crew page.
        Effects: Once there, the parse_full_credits(self,response) should be called, by specifying
                 this method in the callback argument to a yielded scrapy.Request.
        The parse() method does not return any data. 
        """
        # navigate to the Cast & Crew page
        page = response.urljoin("fullcredits/?ref_=tt_ql_cl")
        
        yield scrapy.Request(url=page, callback=self.parse_full_credits)


    def parse_full_credits(self, response):
        """
        Assumption: start on the Cast & Crew page.
        Effects: yield a scrapy.Request for the page of each actor listed on the page. Crew members are not included.
                The yielded request should specify the method parse_actor_page(self, response) should be called when
                the actor’s page is reached.
        The parse_full_credits() method does not return any data. 
        """

        for url in [a.attrib["href"] for a in response.css("td.primary_photo a")]:
            yield scrapy.Request(url =  response.urljoin(url), callback = self.parse_actor_page)

    def parse_actor_page(self, response):
        """
        Assumption: Start on the page of an actor.
        Effects: It should yield a dictionary with two key-value pairs, of the form {"actor" : actor_name, "movie_or_TV_name" : movie_or_TV_name}.
                 The method should yield one such dictionary for each of the movies or TV shows on which that actor has worked.
        """
        # Get the actor name
        actor = response.css(".header .itemprop::text").get()
        # get the list of movie or TV name
        movie_or_TV_name = response.css("b a::text").getall()
        for name in movie_or_TV_name:
            yield {
                'actor': actor,
                'movie_or_TV_name': name
            }