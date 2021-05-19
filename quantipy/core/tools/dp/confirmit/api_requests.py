import requests as req
import json


def get_surveys(projectid, public_url, idp_url, client_id, client_secret, schema_vars=None, schema_filter=None):
    # Source configuration
    source_projectid = projectid
    source_public_site_url = public_url
    source_idp_url = idp_url
    source_client_id = client_id
    source_client_secret = client_secret
    data_params = {}
    meta_params = {}
    if schema_vars:
        data_params['variables'] = schema_vars
        meta_params['variables'] = schema_vars

    if schema_filter:
        data_params['filterExpression'] = schema_filter

    def get_token(source_idp_url, source_client_id, source_client_secret):
        # Get access token
        response = req.post(source_idp_url + 'identity/connect/token',
                            data="grant_type=api-user&scope=pub.surveys",
                            auth=(source_client_id, source_client_secret),
                            headers={'Content-Type': 'application/x-www-form-urlencoded'})
        response.raise_for_status()
        resp_obj = response.json()
        return resp_obj['access_token']


    def get_survey_data(source_token, source_public_site_url, source_projectid):
        # Get source data records
        headers = {'Authorization': 'Bearer ' + source_token, "Accept": "application/x-ndjson", "Content-Type": "application/json"}
        url = source_public_site_url + 'v1/surveys/' + source_projectid + '/responses/data'
        response = req.get(url, params=data_params, headers=headers, stream=False)
        response.raise_for_status()

        # Decode json response - data
        res = response.content.decode("utf-8")
        json_lines = res.splitlines()
        json_data = []
        for line in json_lines:
            json_data.append(json.loads(line))
        return json_data


    def get_survey_meta(source_token, source_public_site_url, source_projectid):
        # Get survey schema records
        headers = {'Authorization': 'Bearer ' + source_token, "Accept": "application/json", "Content-Type": "application/json"}
        url = source_public_site_url + 'v1/surveys/' + source_projectid + '/responses/schema'
        response_schema = req.get(url, params=meta_params, headers=headers, stream=False)
        response_schema.raise_for_status()
        # Decode json response - schema
        res = response_schema.content.decode("utf-8")
        json_lines = res.splitlines()
        json_meta = []
        for line in json_lines:
            json_meta.append(json.loads(line))
        return json_meta


    source_token = get_token(source_idp_url, source_client_id, source_client_secret)
    json_data = get_survey_data(source_token, source_public_site_url, source_projectid)
    json_meta = get_survey_meta(source_token, source_public_site_url, source_projectid)

    return json_data, json_meta


def upload_surveys(api_data, json_data, json_meta, data_vars):
    # Source configuration
    source_projectid = api_data.get("projectid")
    source_public_site_url = api_data.get("public_url")
    source_idp_url = api_data.get("idp_url")
    source_client_id = api_data.get("client_id")
    source_client_secret = api_data.get("client_secret")

    key_vars = []
    filtered_data = []
    root_vars = json_meta[0].get('root')
    for key_var in root_vars.get('keys'):
        key_vars.append(key_var.get('name'))

    for data_record in json_data:
        dr_obj = {}
        for selected_data in data_vars:
            dr_obj[selected_data] = data_record.get(selected_data)
        for key_var in key_vars:
            dr_obj[key_var] = data_record.get(key_var)
        filtered_data.append(dr_obj)

    data = {
        "dataSchema": {
            "keys": key_vars,
            "variables": data_vars
        },
        "data": filtered_data
    }

    # Get access token
    response = req.post(source_idp_url + 'identity/connect/token',
                        data="grant_type=api-user&scope=pub.surveys",
                        auth=(source_client_id, source_client_secret),
                        headers={'Content-Type': 'application/x-www-form-urlencoded'})
    response.raise_for_status()
    resp_obj = response.json()
    source_token = resp_obj['access_token']

    # Upload source data records
    headers = {'Authorization': 'Bearer ' + source_token, "Accept": "application/json", "Content-Type": "application/json"}
    url = source_public_site_url + 'v1/surveys/' + source_projectid + '/responses/data'
    response = req.patch(url, data=json.dumps(data), headers=headers)
    response.raise_for_status()
    return response
