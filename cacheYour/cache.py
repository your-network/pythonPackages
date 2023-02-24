from cacheYour.attributes.attribute import checkAttributeStatusCache, processAttributeCache, processAttributeValueUnitCache, checkAttributeValueUnitStatusCache
from cacheYour.attributes.indexAttributes import checkAttributeStatusCache as checkAttributeIndexStatusCache, processIndexAttributeCache
from cacheYour.brands.brand import checkBrandStatusCache, setBrandCache
from cacheYour.categories.category import checkCategoryStatusCache, setCategoryCache
from cacheYour.series.serie import checkSeriesStatusCache, processSeriesCache

class DataCache:
    @staticmethod
    def checkCache(source_brands: dict = {},
                   source_categories: dict = {},
                   index_attributes: dict = {}):
        checkCategoryStatusCache(source_categories=source_categories)
        print(f"Category Cache present")
        checkBrandStatusCache(source_brands=source_brands)
        print(f"Brand Cache present")
        checkSeriesStatusCache()
        print(f"Series Cache present")
        if index_attributes:
            checkAttributeIndexStatusCache(index_attributes=index_attributes)
            print(f"Index Attribute Cache present")
        else:
            checkAttributeStatusCache()
            checkAttributeValueUnitStatusCache()
            print(f"Attribute & AttributeValueUnit Cache present")

    def triggerCache(self,
                     source_brands: dict = {},
                     source_categories: dict = {},
                     index_attributes: dict = {}):
        setCategoryCache(source_categories=source_categories)
        setBrandCache(source_brands=source_brands)
        processSeriesCache()

        ## attributes logic
        if index_attributes:
            processIndexAttributeCache(index_attributes=index_attributes)
        else:
            processAttributeCache()
            processAttributeValueUnitCache()
