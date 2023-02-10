from cacheYour.attributes.attribute import checkAttributeStatusCache, processAttributeCache, processAttributeValueUnitCache, checkAttributeValueUnitStatusCache
from cacheYour.brands.brand import checkBrandStatusCache, setBrandCache
from cacheYour.categories.category import checkCategoryStatusCache, setCategoryCache
from cacheYour.series.serie import checkSeriesStatusCache, processSeriesCache

class DataCache:
    @staticmethod
    def checkCache(source_brands: dict = {},
                   source_categories: dict = {}):
        checkCategoryStatusCache(source_categories=source_categories)
        print(f"Category Cache present")
        checkBrandStatusCache(source_brands=source_brands)
        print(f"Brand Cache present")
        checkSeriesStatusCache()
        print(f"Series Cache present")
        checkAttributeStatusCache()
        print(f"Attribute Cache present")
        checkAttributeValueUnitStatusCache()
        print(f"AttributeValueUnit Cache present")

    @staticmethod
    def triggerCache(source_brands: dict = {},
                     source_categories: dict = {}):
        setCategoryCache(source_categories=source_categories)
        setBrandCache(source_brands=source_brands)
        processSeriesCache()
        processAttributeCache()
        processAttributeValueUnitCache()
