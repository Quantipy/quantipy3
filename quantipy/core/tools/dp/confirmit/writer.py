from quantipy.core.tools.dp.confirmit.api_requests import get_surveys, upload_surveys


def quantipy_to_confirmit(projectid, public_url, idp_url, client_id, client_secret, schema_vars):
    json_data, json_meta = get_surveys(projectid, public_url, idp_url, client_id, client_secret)

    api_data = {
        "projectid": projectid,
        "public_url": public_url,
        "idp_url": idp_url,
        "client_id": client_id,
        "client_secret": client_secret
    }

    return upload_surveys(api_data, json_data, json_meta, schema_vars)