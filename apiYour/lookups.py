def createCategoryIdLookup(your_categories):
    category_lookup = {}
    for category in your_categories:
        if category.get('externalIDs'):
            for source in category['externalIDs'].keys():
                if category_lookup.get(source):
                    if category_lookup[source].get(category['purpose']):
                        category_lookup[source][category['purpose']].update(
                            {category['externalIDs'][source][0]: category['id']})
                    else:
                        category_lookup[source].update(
                            {category['purpose']: {category['externalIDs'][source][0]: category['id']}})
                else:
                    category_lookup.update(
                        {source: {category['purpose']: {category['externalIDs'][source][0]: category['id']}}})
        else:
            print(f"Category without externalIds: {category}")

    return category_lookup

def createAttributeIdLookup(your_attributes):
    attr_lookup = {}
    for attr in your_attributes:
        if attr_lookup.get(attr['source']):
            attr_lookup[attr['source']].update({attr['externalId']: attr['id']})
        else:
            attr_lookup.update({attr['source']: {attr['externalId']: attr['id']}})

    return attr_lookup

def createAttributeNameLookup(your_attributes):
    attr_lookup = {}
    for attr in your_attributes:
        if attr_lookup.get(attr['source']):
            attr_lookup[attr['source']].update({attr['externalId']: attr['name']})
        else:
            attr_lookup.update({attr['source']: {attr['externalId']: attr['name']}})

    return attr_lookup

def createBrandIdLookup(your_brands):
    brand_lookup = {}
    for brand in your_brands:
        if brand['externalIDs']:
            for source in brand['externalIDs'].keys():
                if brand_lookup.get(source):
                    brand_lookup[source].update({brand['externalIDs'][source][0]: brand['id']})
                else:
                    brand_lookup.update({source: {brand['externalIDs'][source][0]: brand['id']}})

    return brand_lookup

def createAttributeTypeUnitNameLookup(your_attr_type_units):
    attr_type_unit_lookup = {}

    for unit in your_attr_type_units:
        attr_type_unit_lookup.update({unit['name']: unit['id']})

    return attr_type_unit_lookup