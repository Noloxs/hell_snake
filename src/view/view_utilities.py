def filter_strategems(strategems, filter_text):
    filtered_list = {}
    for id, strategem in strategems.items():
        if filter_text.lower() in strategem.name.lower():
            filtered_list.update({id:strategem})

    return filtered_list

def sort_strategems(strategemDict):
    return dict(sorted(strategemDict.items(), key=lambda value:(value[1].category, value[1].name)))