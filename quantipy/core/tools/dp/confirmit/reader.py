import json
import pandas as pd
from quantipy.core.helpers.functions import load_json
from quantipy.core.tools.dp.prep import start_meta
from .languages_file import languages


def quantipy_from_confirmit(meta_json, data_json, text_key='en-GB'):
    types_translations = {
        'numeric': 'float',
        'text': 'string',
        'singleChoice': 'single',
        'multiChoice': 'delimited set' 
    }
    def create_subvar_meta(parsed_meta, subvar, values=False):
        parent_key = 'masks@' + parsed_meta['name']
        name = subvar['source'].replace('columns@', '')
        subvar_obj = {
            'name': name,
            'parent': {parent_key: {'type': parsed_meta['type']}},
            'text': subvar['text'],
            'type': parsed_meta['subtype']
        }
        if values:
            subvar_obj['values'] = 'lib@values@' + parsed_meta['name']
        return subvar_obj

    def fill_items_arr(parsed_meta):
        try:
            var_idx = columns_array.index('columns@' + parsed_meta['name'])
            columns_array[var_idx] = 'masks@' + parsed_meta['name']
        except ValueError:
            columns_array.append('masks@' + parsed_meta['name'])

        children_arr = []
        for item in parsed_meta['items']:
            children_arr.append(item['source'])
        sets[parsed_meta['name']] = {'items': children_arr}

    def get_grid_items(variable):
        children_array = []
        fields = variable.get('fields')
        if fields:
            for field in fields:
                if variable.get('complex-grid'):
                    source = 'columns@' + field['code']
                    language_text = field['texts'][0]['text']
                else:
                    source = 'columns@' + variable['name'] + '_' + field['code']
                    language_code = field['texts'][0].get('languageId')
                    language_text = {}
                    if language_code:
                        language_text[languages[language_code]] = field['texts'][0]['text']

                children_array.append({
                    'properties': {},
                    'source': source,
                    'text': language_text
                })
        return children_array
        

    def get_options(variable, var_type, is_child, has_nodes):
        col_values_arr = []
        def get_nodes_children(value):
            node_obj = {}
            node_obj['text'] = {}
            try:
                confirmit_texts = value.get('texts')[0]
                language_id = confirmit_texts.get('languageId')
                if language_id:
                    node_obj['text'] = { languages[language_id]: confirmit_texts.get('text') }
            except (TypeError, KeyError):
                pass
            node_obj['value'] = value.get('code')

            col_values_arr.append(node_obj)
            children = value.get('children')
            if children:
                for child in children:
                    get_nodes_children(child)

        for value in variable:
            if has_nodes:
               get_nodes_children(value) 
            else:
                loopReference = value.get('loopReference')
                if(loopReference and var_type == 'single'):
                    filtered_loop_ref = filter(lambda x: x['name']  == loopReference, children_vars) 
                    child_var = list(filtered_loop_ref)
                    col_values_val = get_main_info(child_var[0], var_type, is_child=True)
                else:
                    try:
                        col_values_val = int(value["code"])
                    except ValueError:
                        col_values_val = value["code"]

                language_code = value["texts"][0]["languageId"]
                values_dict = {"text": { languages[language_code]: value["texts"][0]["text"]}, "value": col_values_val}
                if value.get('score'):
                    values_dict["factor"] = value.get('score')
                col_values_arr.append(values_dict)
        return col_values_arr

    def get_main_info(variable_meta, var_type, has_nodes=False, is_child=False, complex_grid=False):
        if is_child:
            variable = variable_meta.get('keys')[0]
        else:
            variable = variable_meta

        if has_nodes:
            options = variable.get("nodes")
        else:
            options = variable.get("options")

        variable_obj = {
            "name": variable['name'],
            "parent": {},
            "type": var_type
            # "properties": {}
        }
        if var_type != 'float' and var_type != 'single':
           variable_obj['properties'] = {}
        if var_type == 'array':
            variable_obj['items'] = get_grid_items(variable)
            if variable.get('variableType') == 'numeric':
                variable_obj['subtype'] = 'float'
            if variable.get('variableType') == 'text':
                variable_obj['subtype'] = 'string'
            if variable.get('variableType') == 'rating':
                variable_obj['subtype'] = 'single'
                lib['values'][variable['name']] = get_options(options, var_type, is_child, has_nodes)
                variable_obj['values'] = 'lib@values@' + variable['name']
            if variable.get('variableType') == 'ranking':
                variable_obj['subtype'] = 'int'
            if variable.get('variableType') == 'multiGrid':
                variable_obj['subtype'] = 'delimited set'
                if complex_grid:
                    lib['values'][variable['name']] = get_options(options, var_type, is_child, has_nodes)
                    variable_obj['values'] = 'lib@values@' + variable['name']

        if var_type != 'float' and var_type != 'array' and var_type != 'string' and var_type != 'date':
            variable_obj['values'] = get_options(options, var_type, is_child, has_nodes)
        if variable.get('titles'):
            language_code = variable['titles'][0].get("languageId")
            if language_code:
                variable_obj['text'] = { languages[language_code]: variable['titles'][0]["text"] }
        else:
            if variable.get('texts'):
                language_code = variable['texts'][0]["languageId"]
                variable_obj['text'] = { languages[language_code]: variable['texts'][0]["text"] }
            else:
                variable_obj['text'] = { global_language: "" }
        if is_child:
            variable_obj.update({
                'texts': variable_meta.get('texts'),
                'variables': [get_main_info(var_meta, types_translations[var_meta['variableType']]) for var_meta in variable_meta.get('variables')]
            })
        
        return variable_obj

    data_array = []
    sub_data_array = []
    columns_array = []
    if isinstance(data_json, list):
        data_parsed = data_json
    else:
        with open(data_json, "r") as read_data_file:
            data_parsed = json.load(read_data_file)

    if isinstance(meta_json, dict):
        meta_parsed = meta_json
    else:
        with open(meta_json, "r") as read_meta_file:
            meta_parsed = json.load(read_meta_file)

    for idx, element in enumerate(data_parsed):
        for k, v in element.items():
            if idx == 0:
                columns_array.append('columns@' + k)
            sub_data_array.append(v)
        data_array.append(sub_data_array)

    global_language_code = meta_parsed.get("languages")[0].get("confirmitLanguageId")
    global_language = languages[global_language_code]
    lib = {"default text": global_language, "values": {}}
    sets = {}
    columns_output = {}
    masks_output = {}
    grid_vars = []
    single_vars = []
    delimited_set_vars = []
    multigrid_vars = {}
    grid3d_vars = {}
    root_vars = meta_parsed.get('root')
    vars_arr = root_vars.get('variables')
    for key_var in root_vars.get('keys'):
        vars_arr.append(key_var)
    children_vars = root_vars.get('children')
    if children_vars:
        for children_var in children_vars:
            vars_arr.append(children_var['keys'][0])
    for variable in vars_arr:
        has_parent = variable.get('parentVariableName')
        if has_parent:
            if has_parent in multigrid_vars:
                language_code = variable.get('texts')[0].get('languageId')
                language_text = { 'text': {} }
                if language_code:
                    language_text['text'] = { languages[language_code]: variable['texts'][0]['text'] }
                multigrid_vars[has_parent]['fields'].append(
                    {
                        'code': variable['name'],
                        'texts': [language_text]
                    })
            elif has_parent in grid3d_vars:
                language_code = variable.get('titles')[0].get('languageId')
                language_text = { 'text': {} }
                if language_code:
                    language_text['text'] = { languages[language_code]: variable['titles'][0]['text'] }
                grid3d_vars[has_parent]['fields'].append({
                        'code': variable['name'],
                        'texts': [language_text]
                    })
            else:
                filtered_parent_iter = filter(lambda x: x['name'] == has_parent, vars_arr)
                filtered_parent = next(filtered_parent_iter)
                if filtered_parent['variableType'] == 'multiGrid':
                    if has_parent not in multigrid_vars:
                        try:
                            language_code = variable.get('texts')[0].get('languageId')
                        except TypeError:
                            language_code = None
                        language_text = { 'text': {} }
                        if language_code:
                            language_text['text'] = { languages[language_code]: variable['texts'][0]['text'] }
                        multigrid_vars[has_parent] = {
                            'name': has_parent,
                            'variableType': filtered_parent['variableType'],
                            'complex-grid': True,
                            'options': filtered_parent.get('options'),
                            'fields': [{
                                'code': variable['name'],
                                'texts': [language_text]
                            }]
                        }
                if filtered_parent['variableType'] == 'grid3D':
                    if has_parent not in grid3d_vars:
                        try:
                            language_code = variable.get('titles')[0].get('languageId')
                        except TypeError:
                            language_code = None
                        language_text = { 'text': {} }
                        if language_code:
                            language_text['text'] = { languages[language_code]: variable['titles'][0]['text'] }
                        grid3d_vars[has_parent] = {
                            'name': has_parent,
                            'variableType': filtered_parent['variableType'],
                            'complex-grid': True,
                            'options': filtered_parent.get('options'),
                            'fields': [{
                                'code': variable['name'],
                                'texts': [language_text]
                            }]
                        }    

        if variable.get('variableType') == 'singleChoice':
            has_nodes = False
            if variable.get('options'):
                try:
                    int(variable['options'][0]['code'])
                except ValueError:
                    pass
            if variable.get('nodes'):
                has_nodes = True
                try:
                    int(variable['nodes'][0]['code'])
                except ValueError:
                    pass

            single_vars.append(variable['name'])
            columns_output[variable['name']] = get_main_info(variable, 'single', has_nodes)
        if variable.get('variableType') == 'multiChoice':
            delimited_set_vars.append(variable['name'])
            columns_output[variable['name']] = get_main_info(variable, 'delimited set')
        if variable.get('variableType') == 'dateTime':
            columns_output[variable['name']] = get_main_info(variable, 'date')
        if variable.get('variableType') == 'numeric':
            if variable.get('fields'):
                parsed_meta = get_main_info(variable, 'array')
                masks_output[variable['name']] = parsed_meta
                fill_items_arr(parsed_meta)
                numeric_children_arr = []
                for subvar in parsed_meta['items']:
                    parsed_subvar_meta = create_subvar_meta(parsed_meta, subvar)
                    columns_output[parsed_subvar_meta['name']] = parsed_subvar_meta
                    numeric_children_arr.append(parsed_subvar_meta['name'])
                grid_vars.append({'parent': variable['name'], 'children': numeric_children_arr})
            else:
                columns_output[variable['name']] = get_main_info(variable, 'float')
        if variable.get('variableType') == 'text':
            if variable.get('fields'):
                parsed_meta = get_main_info(variable, 'array')
                masks_output[variable['name']] = parsed_meta
                fill_items_arr(parsed_meta)
                text_children_arr = []
                for subvar in parsed_meta['items']:
                    parsed_subvar_meta = create_subvar_meta(parsed_meta, subvar)
                    columns_output[parsed_subvar_meta['name']] = parsed_subvar_meta
                    text_children_arr.append(parsed_subvar_meta['name'])
                grid_vars.append({'parent': variable['name'], 'children': text_children_arr})
            else:
                columns_output[variable['name']] = get_main_info(variable, 'string')
        if variable.get('variableType') == 'rating':
            parsed_meta = get_main_info(variable, 'array')
            masks_output[variable['name']] = parsed_meta
            fill_items_arr(parsed_meta)
            single_children_arr = []
            for subvar in parsed_meta['items']:
                parsed_subvar_meta = create_subvar_meta(parsed_meta, subvar, True)
                columns_output[parsed_subvar_meta['name']] = parsed_subvar_meta
                single_children_arr.append(parsed_subvar_meta['name'])
            grid_vars.append({'parent': variable['name'], 'children': single_children_arr})
        if variable.get('variableType') == 'ranking':
            parsed_meta = get_main_info(variable, 'array')
            masks_output[variable['name']] = parsed_meta
            fill_items_arr(parsed_meta)
            int_children_arr = []
            for subvar in parsed_meta['items']:
                parsed_subvar_meta = create_subvar_meta(parsed_meta, subvar)
                columns_output[parsed_subvar_meta['name']] = parsed_subvar_meta
                int_children_arr.append(parsed_subvar_meta['name'])
            grid_vars.append({'parent': variable['name'], 'children': int_children_arr})
        if variable.get('variableType') == 'multiGrid':
            if variable['name'] not in multigrid_vars:
                multigrid_vars[variable['name']] = {
                    'name': variable['name'],
                    'variableType': variable['variableType'],
                    'complex-grid': True,
                    'options': variable.get('options'),
                    'fields': []
                }
    
    for k, v in multigrid_vars.items():
        parsed_meta = get_main_info(v, 'array', complex_grid=True)
        masks_output[v['name']] = parsed_meta
        fill_items_arr(parsed_meta)
        multigrid_children_arr = []
        for subvar in parsed_meta['items']:
            parsed_subvar_meta = create_subvar_meta(parsed_meta, subvar)
            columns_output[parsed_subvar_meta['name']]['parent'] = parsed_subvar_meta['parent']
            multigrid_children_arr.append(parsed_subvar_meta['name'])

    sets['data file'] = {
        "text": { global_language: "Variable order in source file" },
        "items": columns_array
    }
    output_obj = {
        "info": {
            "text": "Converted from SAV file .",
            "from_source": {"pandas_reader": "sav"}
        },
        "lib": lib,
        "masks": masks_output,
        "sets": sets,
        "type": "pandas.DataFrame",
        "columns": columns_output
    }
    for data in data_parsed:
        for nav in grid_vars:
            if nav['parent'] in data:
                old_values = data.pop(nav['parent'])
                try:
                    for k, v in old_values.items():
                        data[nav['parent'] + '_' + k] = v
                except AttributeError:
                   data[nav['parent']] = old_values 
        for single in single_vars:
            if data.get(single):
                try:
                    data[single] = int(data[single])
                except:
                    pass
            else:
                data[single] = None

        for delset_var in delimited_set_vars:
            str_true_var = ''
            if data.get(delset_var) and data[delset_var].get('true'):
                for true_var in data[delset_var]['true']:
                    str_true_var += str(true_var) + ';'
                data[delset_var] = str_true_var
            else:
                data[delset_var] = None

    df = pd.DataFrame.from_dict(data=data_parsed)
    return output_obj, df
