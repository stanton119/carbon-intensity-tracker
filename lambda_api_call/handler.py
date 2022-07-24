import json
from typing import Dict
import requests
import datetime
import boto3

import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("carbonForecast")


def lambda_handler(event, context):
    forecast = get_forecast()
    logger.info(f"Saving forecast to dynamo db, index={forecast['forecast_date']}")
    return table.put_item(Item=forecast)


def get_forecast(postcode: str = "SW7") -> Dict:
    request_date = datetime.date.today()
    result = requests.get(
        f"https://api.carbonintensity.org.uk/regional/intensity/{request_date.isoformat()}/fw48h/postcode/{postcode}"
    )
    result_json = result.text

    return {"forecast_date": request_date.isoformat(), "raw_json": result_json}
