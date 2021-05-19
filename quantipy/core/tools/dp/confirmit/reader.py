import json
import pandas as pd
from quantipy.core.helpers.functions import load_json
from quantipy.core.tools.dp.prep import start_meta
from .languages_file import languages
from .helpers import int_or_float

def quantipy_from_confirmit(meta_json, data_json, verbose=False, text_key='en-GB'):
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
        if parsed_meta.get('type') == 'array' and parsed_meta.get('subtype') == 'single':
            subvar_obj['properties'] = {'created': True}
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
        set_obj = {'items': children_arr}
        if parsed_meta.get('type') == 'array':
            set_obj['name'] = parsed_meta['name']
        sets[parsed_meta['name']] = set_obj

    def get_grid_items(variable):
        children_array = []
        fields = variable.get('fields')
        var_type = variable.get('variableType')
        if fields:
            for field in fields:
                if variable.get('complex-grid'):
                    source = "columns@{}".format(field['code'])
                    language_text = field['texts'][0]['text']
                else:
                    if var_type == 'rating' or var_type == 'singleChoice':
                        source = "columns@{variable_name}[{{{variable_name}_{field}}}]" \
                            .format(variable_name=variable['name'], field=field['code'])
                    else:
                        source = "columns@{variable_name}_{field}" \
                            .format(variable_name=variable['name'], field=field['code'])
                    language_code = field['texts'][0].get('languageId')
                    language_text = {}
                    if language_code:
                        language_text[languages[language_code]] = field['texts'][0]['text']
                item_props = {
                    'source': source,
                    'text': language_text
                }
                if var_type != 'ranking' and var_type != 'rating' and var_type != 'singleChoice':
                   item_props['properties'] = {}
                children_array.append(item_props)
        return children_array
        

    def get_options(variable, var_type, is_child, has_nodes):
        if variable is None:
            return None
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

        for idx, value in enumerate(variable):
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
                        col_values_val = idx + 1

                language_code = value["texts"][0]["languageId"]
                values_dict = {"text": { languages[language_code]: value["texts"][0]["text"]}, "value": col_values_val}
                if value.get('score'):
                    values_dict["factor"] = int(value.get('score'))
                col_values_arr.append(values_dict)
        return col_values_arr

    def get_main_info(variable_meta, var_type, has_nodes=False, is_child=False, complex_grid=False):
        if is_child:
            variable = variable_meta.get('keys')[0]
        else:
            variable = variable_meta

        confirmit_var_type = variable.get('variableType')

        if has_nodes:
            options = variable.get("nodes")
        else:
            options = variable.get("options")

        variable_obj = {
            "name": variable['name'],
            "type": var_type
        }
        is_single_grid_var = confirmit_var_type == 'singleChoice' and var_type == 'array'
        if is_single_grid_var:
            tags = variable.get('tags')
            if tags is not None:
                variable_obj['tags'] = tags
        if confirmit_var_type != 'rating' and not is_single_grid_var:
            variable_obj['parent'] = {}
        if var_type != 'float' and var_type != 'int' and var_type != 'single' and confirmit_var_type != 'rating' and not is_single_grid_var:
           variable_obj['properties'] = {}
        if var_type == 'array':
            variable_obj['items'] = get_grid_items(variable)
            if confirmit_var_type == 'numeric':
                numeric_type = int_or_float(variable)
                variable_obj['subtype'] = numeric_type
            if confirmit_var_type == 'text':
                variable_obj['subtype'] = 'string'
            if confirmit_var_type == 'rating' or confirmit_var_type == 'singleChoice':
                variable_obj['subtype'] = 'single'
                lib['values'][variable['name']] = get_options(options, var_type, is_child, has_nodes)
                variable_obj['values'] = 'lib@values@' + variable['name']
            if confirmit_var_type == 'ranking':
                variable_obj['subtype'] = 'int'
                lib['values'][variable['name']] = get_options(options, var_type, is_child, has_nodes)
                variable_obj['values'] = 'lib@values@' + variable['name']
            if confirmit_var_type == 'multiGrid':
                variable_obj['subtype'] = 'delimited set'
                if complex_grid:
                    lib['values'][variable['name']] = get_options(options, var_type, is_child, has_nodes)
                    variable_obj['values'] = 'lib@values@' + variable['name']

        if var_type != 'float' and var_type != 'int' and var_type != 'array' and var_type != 'string' and var_type != 'date':
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

    def reformat_loop_data(loop_var, loop_of_loop=None):
        for data in data_parsed:
            try:
                old_values = data.pop(loop_var)
                for idx, value in enumerate(old_values):
                    for k, v in value.items():
                        if loop_of_loop is None:
                            if k != loop_var:
                                k = '{loop_var}_{k}'.format(loop_var=loop_var, k=k)
                        else:
                            if k != loop_of_loop:
                                k = '{loop_var}_{k}'.format(loop_var=loop_var, k=k)
                            else:
                                k = loop_var
                        k = '{k}_{string_idx}'.format(k=k, string_idx=str(idx + 1))
                        data[k] = v
            except KeyError:
                pass

    def parse_confirmit_types(variable, loop_of_loop=None):
        confirmit_var_type = variable.get('variableType')
        is_loop = variable.get('is_loop')
        if verbose:
            confirmit_info[variable['name']] = variable
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
                try:
                    filtered_parent_iter = filter(lambda x: x['name'] == has_parent, vars_arr)
                    filtered_parent = next(filtered_parent_iter)
                except StopIteration:
                    filtered_parent = {}
                if filtered_parent.get('variableType') == 'multiGrid':
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
                if filtered_parent.get('variableType') == 'grid3D':
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

        if confirmit_var_type == 'singleChoice':
            has_nodes = False

            if variable.get('nodes'):
                has_nodes = True

            if variable.get("isCompound") and variable.get("fields") and variable.get("options"):
                parsed_meta = get_main_info(variable, 'array')
                masks_output[variable['name']] = parsed_meta
                fill_items_arr(parsed_meta)
                single_children_arr = []
                for subvar in parsed_meta['items']:
                    parsed_subvar_meta = create_subvar_meta(parsed_meta, subvar, True)
                    columns_output[parsed_subvar_meta['name']] = parsed_subvar_meta
                    single_children_arr.append(parsed_subvar_meta['name'])
                grid_vars.append({'parent': variable['name'], 'children': single_children_arr})

            else:
                if is_loop:
                    root_name = variable['name']
                    reformat_loop_data(root_name, loop_of_loop)
                    loop_children = variable.get('variables')
                    loop_of_loop = variable.get('children')
                    lc_root_names = []
                    lol_root_names = []
                    for idx, opt in enumerate(variable['options']):
                        variable['name'] = root_name + '_' + opt['code']
                        columns_output[variable['name']] = get_main_info(variable, 'single', has_nodes=has_nodes)
                        for lc_idx, loop_child in enumerate(loop_children):
                            if idx == 0:
                                lc_root_names.append(loop_child['name'])
                            loop_child['name'] = root_name + '_' + lc_root_names[lc_idx] + '_' + opt['code']
                            parse_confirmit_types(loop_child)
                            loop_child['name'] = lc_root_names[lc_idx]
                        for lol_idx, loop in enumerate(loop_of_loop):
                            if idx == 0:
                                lol_root_names.append(loop['name'])
                            loop['name'] = root_name + '_' + lol_root_names[lol_idx] + '_' + opt['code']
                            parse_confirmit_types(loop, lol_root_names[lol_idx])
                            loop['name'] = lol_root_names[lol_idx]

                else:
                    columns_output[variable['name']] = get_main_info(variable, 'single', has_nodes=has_nodes)
                    single_vars.append(variable['name'])
        if confirmit_var_type == 'multiChoice':
            delimited_set_vars.append(variable['name'])
            columns_output[variable['name']] = get_main_info(variable, 'delimited set')
        if confirmit_var_type == 'dateTime':
            columns_output[variable['name']] = get_main_info(variable, 'date')
        if confirmit_var_type == 'numeric':
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
                numeric_type = int_or_float(variable)
                columns_output[variable['name']] = get_main_info(variable, numeric_type)
        if confirmit_var_type == 'text':
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
        if confirmit_var_type == 'rating':
            if variable.get('isCompound'):
                parsed_meta = get_main_info(variable, 'array')
                masks_output[variable['name']] = parsed_meta
                fill_items_arr(parsed_meta)
                single_children_arr = []
                for subvar in parsed_meta['items']:
                    parsed_subvar_meta = create_subvar_meta(parsed_meta, subvar, True)
                    columns_output[parsed_subvar_meta['name']] = parsed_subvar_meta
                    single_children_arr.append(parsed_subvar_meta['name'])
                grid_vars.append({'parent': variable['name'], 'children': single_children_arr})
            else:
                single_vars.append(variable['name'])
                columns_output[variable['name']] = get_main_info(variable, 'single')
        if confirmit_var_type == 'ranking':
            parsed_meta = get_main_info(variable, 'array')
            masks_output[variable['name']] = parsed_meta
            fill_items_arr(parsed_meta)
            int_children_arr = []
            for subvar in parsed_meta['items']:
                parsed_subvar_meta = create_subvar_meta(parsed_meta, subvar, True)
                columns_output[parsed_subvar_meta['name']] = parsed_subvar_meta
                int_children_arr.append(parsed_subvar_meta['name'])
            grid_vars.append({'parent': variable['name'], 'children': int_children_arr})
        if confirmit_var_type == 'multiGrid':
            if variable['name'] not in multigrid_vars:
                multigrid_vars[variable['name']] = {
                    'name': variable['name'],
                    'variableType': variable['variableType'],
                    'complex-grid': True,
                    'options': variable.get('options'),
                    'fields': []
                }

    def set_as_loop(variable):
        ch_var = variable.get('keys')[0]
        ch_var['texts'] = variable.get('texts')
        ch_var['variables'] = variable.get('variables')
        children_arr = []
        if variable.get('children'):
            for child in variable.get('children'):
                children_arr.append(set_as_loop(child))
        ch_var['children'] = children_arr
        ch_var['is_loop'] = True
        return ch_var

    data_array = []
    sub_data_array = []
    columns_array = []
    confirmit_info = {}
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
            ch_var = set_as_loop(children_var)
            vars_arr.append(ch_var)

    for variable in vars_arr:
        parse_confirmit_types(variable)
    
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
    info = {
        "text": "Converted from SAV file .",
        "from_source": {"pandas_reader": "sav"}
    }
    if verbose:
        info["has_external"] = {
            "confirmit": {
                "meta": {
                    "columns": confirmit_info
                }
            }
        }
    output_obj = {
        "info": info,
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
