
class DataCache:
    def __init__(self, connection):
        self.connection = connection

    def checkCache(self,
                   source_brands: dict = {},
                   source_categories: dict = {},
                   index_attributes: dict = {}):
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
        if index_attributes:
            from cacheYour.attributes.indexAttributes import AttributeIndex
            attribute_cache = AttributeIndex(connection=self.connection)
            attribute_cache.checkAttributeStatusCache(index_attributes=index_attributes)
            print(f"Index Attribute Cache present")
        else:
            from cacheYour.attributes.attribute import AttributeCache
            attribute_cache = AttributeCache(connection=self.connection)
            attribute_cache.checkAttributeStatusCache()
            attribute_cache.checkAttributeValueUnitStatusCache()
            print(f"Attribute & AttributeValueUnit Cache present")

    def triggerCache(self,
                     source_brands: dict = {},
                     source_categories: dict = {},
                     index_attributes: dict = {}):
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
        if index_attributes:
            from cacheYour.attributes.indexAttributes import AttributeIndex
            attribute_cache = AttributeIndex(connection=self.connection)
            attribute_cache.processIndexAttributeCache(index_attributes=index_attributes)
            print(f"Index Attribute Cache processed")
        else:
            from cacheYour.attributes.attribute import AttributeCache
            attribute_cache = AttributeCache(connection=self.connection)
            attribute_cache.processAttributeCache()
            attribute_cache.processAttributeValueUnitCache()
            print(f"Index Attribute Cache processed")
