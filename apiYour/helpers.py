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
