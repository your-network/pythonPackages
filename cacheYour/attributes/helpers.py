def processAttributeIndexDetails(attribute: dict) -> dict:
    from cacheYour.attributes.indexAttributes import FILTER_ATTRIBUTES
    ## processing
    if attribute['valueType'] == 'number':
        if attribute['sourceType'] == "range":
            attr_value = "integer_range"
        else:
            attr_value = "float"

    elif attribute['valueType'] == 'string':
        if attribute['sourceType'] == "y_n":
            attr_value = "boolean"

        elif attribute['sourceType'] == "text":
            attr_value = "keyword"

        elif attribute['sourceType'] == "dropdown":
            attr_value = "keyword"

        else:
            attr_value = "keyword"
    else:
        attr_value = "keyword"
    attribute.update({'indexValueType': attr_value})

    ## extra details
    index_details = FILTER_ATTRIBUTES.get(str(attribute['id']), {})

    ## updating attribute
    attribute_final = {**attribute, **index_details}

    return attribute_final

