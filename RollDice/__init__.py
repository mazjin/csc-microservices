import logging

import azure.functions as func
from . import roller


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('RollDice - received HTTP request')

    roll_string, number_rolls, drop_rule, number_drops = get_params(req, ['roll', 'number_rolls', 'drop_rule', 'number_drops'])
    if roll_string:
        roll_result = roller.RollMultiple(roll_string, number_rolls, drop_rule, number_drops) if number_rolls and int(number_rolls) > 1 else roller.Roll(roll_string)
        logging.info(f"RollDice - rolled {roll_string} for result of {roll_result.result}")
        return func.HttpResponse(roll_result.to_json(), status_code=200)
    else:
        logging.warn('RollDice - received request had no roll info defined')
        return func.HttpResponse(
             "Please try again using a valid roll definition.",
             status_code=400
        )

def get_params(req, param_names):
    params=dict(zip(param_names,list(map(lambda x: req.params.get(x), param_names))))
    if (not all(params.values())):
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else: 
            return [param or req_body.get(param_name) for (param_name, param) in params.items()]
    return params.values()
            
