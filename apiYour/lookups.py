from apiYour.settingsApi import SOURCE_IDS, PURPOSE_IDS

def createCategoryIdLookup(message_handler: object, your_categories: list) -> dict:
    category_lookup = {}

    ## setting sources
    for source_row in SOURCE_IDS:
        category_lookup.update({source_row['id']: {}})
    ## setting purposes
    for purpose_row in PURPOSE_IDS:
        for source_key in category_lookup.keys():
            category_lookup[source_key].update({purpose_row['id']: {}})

    ## process categories for lookup
    for category in your_categories:
        if category.get('externalIDs') or str(category['purpose']) == "2":
            if str(category['purpose']) == "2":
                external_id = category['properties']["ID"]
                category.update({'externalIDs': {"2": [external_id]}})
            for source in category['externalIDs'].keys():
                category_lookup[str(source)][str(category['purpose'])].update({str(category['externalIDs'][source][0]): category['id']})
        else:
            ## logging
            message_handler.logStruct(topic=f"createCategoryIdLookup: Category without externalIds",
                                      data=category,
                                      level="WARNING")

    return category_lookup

def createSerieIdLookup(series: list) -> dict:
    serie_lookup = {}

    ## setting sources
    for source_row in SOURCE_IDS:
        serie_lookup.update({source_row['id']: {}})

    ## process series for lookup
    for serie in series:
        if serie.get('externalIDs'):
            for source in serie_lookup['externalIDs'].keys():
                serie_lookup[str(source)].update({str(serie['externalIDs'][source][0]): serie['id']})
        else:
            print(f"Serie without externalIds: {serie}")

    return serie_lookup

def updateCategoryIdLookup(category_lookup: dict,
                           source: str,
                           purpose:str,
                           external_id: str,
                           internal_id: int) -> dict:

    category_lookup[source][purpose].update(
        {str(external_id): internal_id})

    return category_lookup

def createAttributeIdLookup(your_attributes: list) -> dict:
    attr_lookup = {}
    for attr in your_attributes:
        if attr_lookup.get(str(attr['source'])):
            attr_lookup[str(attr['source'])].update({attr['externalId']: attr['id']})
        else:
            attr_lookup.update({str(attr['source']): {attr['externalId']: attr['id']}})

    return attr_lookup

def createAttributeNameLookup(your_attributes: list) -> dict:
    attr_lookup = {}
    for attr in your_attributes:
        if attr_lookup.get(str(attr['source'])):
            attr_lookup[str(attr['source'])].update({attr['externalId']: attr['name']})
        else:
            attr_lookup.update({str(attr['source']): {attr['externalId']: attr['name']}})

    return attr_lookup

def createBrandIdLookup(your_brands: list) -> dict:
    brand_lookup = {}
    for brand in your_brands:
        if brand.get('externalIDs'):
            for source in brand['externalIDs'].keys():
                if brand_lookup.get(str(source)):
                    brand_lookup[str(source)].update({str(brand['externalIDs'][source][0]): brand['id']})
                else:
                    brand_lookup.update({str(source): {str(brand['externalIDs'][source][0]): brand['id']}})

    return brand_lookup

def createAttributeTypeUnitNameLookup(your_attr_type_units: list) -> dict:
    attr_type_unit_lookup = {}

    for unit in your_attr_type_units:
        attr_type_unit_lookup.update({unit['name']: unit['id']})

    return attr_type_unit_lookup