import logging
import azure.functions as func
import mimetypes
from . import populateSheet

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    req_body = req.get_json()
    if req_body:
        response = populateSheet.populateSheet(req_body['character'],context)
        return func.HttpResponse(
            body=response, 
            status_code=200,
            mimetype="application/pdf"
        )
    else: 
        logging.warn("PopulateSheet - received request but no character info defined")
        return func.HttpResponse(
             "Please try again using valid character data.",
             status_code=400
        )

