from quantipy.core.tools.dp.forsta.api_requests import upload_surveys
import json


def quantipy_to_forsta(self, projectid, public_url, idp_url, client_id, client_secret, schema_vars):
    json_meta = self._original_meta
    to_forsta_format = self._code_mapping['to_forsta_format']

    decoded_data = self._data.replace(to_forsta_format)
    json_data = json.loads(decoded_data.to_json(orient='records'))

    api_data = {
        "projectid": projectid,
        "public_url": public_url,
        "idp_url": idp_url,
        "client_id": client_id,
        "client_secret": client_secret
    }

    return upload_surveys(api_data, json_data, json_meta, schema_vars)