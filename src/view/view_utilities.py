import re

def filter_stratagems(stratagems, filter_text):
    filtered_list = {}
    
    has_special_chars = bool(re.search(r'[^a-zA-Z0-9\s]', filter_text))

    for id, stratagem in stratagems.items():
        stratagem_name = stratagem.name
        
        if has_special_chars:
            if filter_text.lower() in stratagem_name.lower():
                filtered_list.update({id: stratagem})
        else:
            normalized_stratagem_name = ''.join(char for char in stratagem_name if char.isalnum() or char.isspace())
            if filter_text.lower() in normalized_stratagem_name.lower():
                filtered_list.update({id: stratagem})

    return filtered_list

def sort_stratagems(stratagemDict):
    return dict(sorted(stratagemDict.items(), key=lambda value:(value[1].category, value[1].name)))