import datetime
import io
import logging
import os
from typing import Dict

import boto3
import botocore.exceptions
import requests

logger = logging.getLogger()
logger.setLevel(logging.INFO)


dynamodb = boto3.resource("dynamodb")
TABLE_NAME = os.environ["TABLE_NAME"]
table = dynamodb.Table(TABLE_NAME)


s3 = boto3.resource("s3")
BUCKET_NAME = os.environ["BUCKET_NAME"]
bucket = s3.Bucket(BUCKET_NAME)


def lambda_handler(event, context):
    # {
    # "postcode": null,
    # "forecast_date": null
    # }

    forecast = get_forecast(event.get("postcode"), event.get("forecast_date"))
    logger.info(
        f"Forecast result: {forecast['forecast_date']}, {forecast['raw_json'][:100]}"
    )

    logger.info(
        f"Saving forecast to dynamo db, table={TABLE_NAME}, index={forecast['forecast_date']}"
    )
    try:
        table.put_item(Item=forecast)
    except botocore.exceptions.ClientError as e:
        logging.error(e)

    logger.info(
        f"Saving forecast to s3, bucket={BUCKET_NAME}, index={forecast['forecast_date']}"
    )
    try:
        buffer = io.BytesIO(initial_bytes=forecast["raw_json"].encode("utf-8"))
        bucket.upload_fileobj(
            buffer, f"carbon_api_raw/{forecast['forecast_date']}/0.json"
        )
    except botocore.exceptions.ClientError as e:
        logging.error(e)
    return True


def get_forecast(postcode: str = None, forecast_date: str = None) -> Dict:
    if postcode is None:
        postcode = "SW7"
    if forecast_date is None:
        request_date = datetime.date.today()
    else:
        request_date = datetime.datetime.strptime(forecast_date, "%Y-%m-%d").date()

    result = requests.get(
        f"https://api.carbonintensity.org.uk/regional/intensity/{request_date.isoformat()}/fw48h/postcode/{postcode}"
    )
    result_json = result.text

    return {"forecast_date": request_date.isoformat(), "raw_json": result_json}
