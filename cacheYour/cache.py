
class DataCache:
    def __init__(self, connection):
        self.connection = connection

    def checkCache(self,
                   source_brands: dict = {},
                   source_categories: dict = {},
                   source_attributes: dict = {}):
        ## category cache
        from cacheYour.categories.category import CategoryCache
        category_cache = CategoryCache(connection=self.connection)
        category_cache.checkCategoryStatusCache(source_categories=source_categories)
        print(f"Category Cache present")

        ## Brand cache
        from cacheYour.brands.brand import BrandCache
        brand_cache = BrandCache(connection=self.connection)
        brand_cache.checkBrandStatusCache(source_brands=source_brands)
        print(f"Brand Cache present")

        ## Serie cache
        from cacheYour.series.serie import SerieCache
        serie_cache = SerieCache(connection=self.connection)
        serie_cache.checkSeriesStatusCache()
        print(f"Series Cache present")

        ## Attribute cache
        from cacheYour.attributes.attribute import AttributeCache
        attribute_cache = AttributeCache(connection=self.connection)
        attribute_cache.checkAttributeStatusCache(source_attributes=source_attributes)
        attribute_cache.checkAttributeValueUnitStatusCache()
        print(f"Attribute & AttributeValueUnit Cache present")

    def triggerCache(self,
                     source_brands: dict = {},
                     source_categories: dict = {},
                     source_attributes: dict = {}):
        ## category cache
        from cacheYour.categories.category import CategoryCache
        category_cache = CategoryCache(connection=self.connection)
        category_cache.setCategoryCache(source_categories=source_categories)
        print(f"Category Cache processed")

        ## Brand cache
        from cacheYour.brands.brand import BrandCache
        brand_cache = BrandCache(connection=self.connection)
        brand_cache.setBrandCache(source_brands=source_brands)
        print(f"Brand Cache processed")

        ## Serie cache
        from cacheYour.series.serie import SerieCache
        serie_cache = SerieCache(connection=self.connection)
        serie_cache.processSeriesCache()
        print(f"Series Cache processed")

        ## Attribute cache
        from cacheYour.attributes.attribute import AttributeCache
        attribute_cache = AttributeCache(connection=self.connection)
        attribute_cache.processAttributeCache(source_attributes=source_attributes)
        attribute_cache.processAttributeValueUnitCache()
        print(f"Index Attribute Cache processed")
