from fastapi import FastAPI, Depends
from fastapi.openapi.docs import get_redoc_html
#
from .deps import basic_auth


def reset_api_doc(api: FastAPI):
    openapi_url = '/doc/openapi.json'

    @api.get(openapi_url,
             include_in_schema=False,
             dependencies=[Depends(basic_auth)],
             )
    def openapi_schema():
        return api.openapi()

    @api.get('/doc',
             include_in_schema=False,
             dependencies=[Depends(basic_auth)],
             )
    def doc_html():
        return get_redoc_html(
            openapi_url=openapi_url,
            title='E Api - Doc'
        )
