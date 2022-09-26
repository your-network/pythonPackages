def fillterCategoryPurpose(categories: list,
                           purpose: int) -> list:
    filter_list = []

    for category in categories:
        if category['purpose'] == purpose:
            filter_list.append(category)

    return filter_list

