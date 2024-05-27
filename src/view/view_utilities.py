def filter_stratagems(stratagems, filter_text):
    filtered_list = {}
    for id, stratagem in stratagems.items():
        if filter_text.lower() in stratagem.name.lower():
            filtered_list.update({id:stratagem})

    return filtered_list

def sort_stratagems(stratagemDict):
    return dict(sorted(stratagemDict.items(), key=lambda value:(value[1].category, value[1].name)))