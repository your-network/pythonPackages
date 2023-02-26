from cacheYour.attributes.indexAttributes import checkAttributeStatusCache as checkAttributeIndexStatusCache, processIndexAttributeCache
from cacheYour.brands.brand import checkBrandStatusCache, setBrandCache
from cacheYour.categories.category import checkCategoryStatusCache, setCategoryCache
from cacheYour.series.serie import checkSeriesStatusCache, processSeriesCache
from cacheYour.client import RedisClient

class DataCache:
    def __init__(self, client=RedisClient):
        self.client = client

    def checkCache(self,
                   source_brands: dict = {},
                   source_categories: dict = {},
                   index_attributes: dict = {}):
        ## category cache
        from cacheYour.categories.category import CategoryCache
        category_cache = CategoryCache(client=self.client)
        category_cache.checkCategoryStatusCache(source_categories=source_categories)
        print(f"Category Cache present")

        ## Brand cache
        from cacheYour.brands.brand import BrandCache
        brand_cache = BrandCache(client=self.client)
        brand_cache.checkBrandStatusCache(source_brands=source_brands)
        print(f"Brand Cache present")

        ## Serie cache
        from cacheYour.series.serie import SerieCache
        serie_cache = SerieCache(client=self.client)
        serie_cache.checkSeriesStatusCache()
        print(f"Series Cache present")

        ## Attribute cache
        if index_attributes:
            from cacheYour.attributes.indexAttributes import AttributeIndex
            attribute_cache = AttributeIndex(client=self.client)
            attribute_cache.checkAttributeIndexStatusCache(index_attributes=index_attributes)
            print(f"Index Attribute Cache present")
        else:
            from cacheYour.attributes.attribute import AttributeCache
            attribute_cache = AttributeCache(client=self.client)
            attribute_cache.checkAttributeStatusCache()
            attribute_cache.checkAttributeValueUnitStatusCache()
            print(f"Attribute & AttributeValueUnit Cache present")

    def triggerCache(self,
                     source_brands: dict = {},
                     source_categories: dict = {},
                     index_attributes: dict = {}):
        ## category cache
        from cacheYour.categories.category import CategoryCache
        category_cache = CategoryCache(client=self.client)
        category_cache.setCategoryCache(source_categories=source_categories)
        print(f"Category Cache processed")

        ## Brand cache
        from cacheYour.brands.brand import BrandCache
        brand_cache = BrandCache(client=self.client)
        brand_cache.setBrandCache(source_brands=source_brands)
        print(f"Brand Cache processed")

        ## Serie cache
        from cacheYour.series.serie import SerieCache
        serie_cache = SerieCache(client=self.client)
        serie_cache.processSeriesCache()
        print(f"Series Cache processed")

        ## Attribute cache
        if index_attributes:
            from cacheYour.attributes.indexAttributes import AttributeIndex
            attribute_cache = AttributeIndex(client=self.client)
            attribute_cache.processIndexAttributeCache(index_attributes=index_attributes)
            print(f"Index Attribute Cache processed")

        ## attributes logic
        if index_attributes:
            processIndexAttributeCache(index_attributes=index_attributes)
        else:
            from cacheYour.attributes.attribute import AttributeCache
            attribute_cache = AttributeCache(client=self.client)
            attribute_cache.processAttributeCache()
            attribute_cache.processAttributeValueUnitCache()
