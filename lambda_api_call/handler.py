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
    # {
    # "postcode": null,
    # "forecast_date": null
    # }
    forecast = get_forecast(event["postcode"], event["forecast_date"])
    logger.info(f"Saving forecast to dynamo db, index={forecast['forecast_date']}")
    return table.put_item(Item=forecast)


def get_forecast(postcode: str = "SW7", forecast_date: str = None) -> Dict:
    if forecast_date is None:
        request_date = datetime.date.today()
    else:
        request_date = datetime.datetime.strptime(forecast_date, "%Y-%m-%d").date()

    result = requests.get(
        f"https://api.carbonintensity.org.uk/regional/intensity/{request_date.isoformat()}/fw48h/postcode/{postcode}"
    )
    result_json = result.text

    return {"forecast_date": request_date.isoformat(), "raw_json": result_json}
