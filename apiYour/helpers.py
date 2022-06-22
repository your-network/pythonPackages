def createCategoryIdLookup(your_categories):
    your_attr_gr = [x for x in your_categories if x['purpose'] == 'AttributeGroup']
    your_cat = [x for x in your_categories if x['purpose'] == 'Taxonomy']
    your_nfts = [x for x in your_categories if x['purpose'] == 'NFTCollection']

    attr_gr_lookup = {}
    for attr in your_attr_gr:
        attr_gr_lookup.update({attr['properties']['ID']: attr['id']})

    cat_lookup = {}
    for cat in your_cat:
        cat_lookup.update({cat['properties']['ID']: cat['id']})

    nft_lookup = {}
    for nft in your_nfts:
        nft_lookup.update({nft['properties']['ID']: nft['id']})

    return attr_gr_lookup, cat_lookup, nft_lookup


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

def logging_error_message(topic, status_code, content, payload):
    import logging
    from datetime import datetime
    message = (f"Time: {datetime.now()}"
                  f""
                  f"Call {topic} failure."
                  f""
                  f"text: {content}, "
                  f""
                  f"data: {payload}")
    logging.error(message)
    print(message)