import os
import boto3
import base64
from botocore.exceptions import ClientError
import json
import datetime
import decimal
import logging


# Inherit from JSONEncoder
class DictionaryToJSON(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.isoformat()
        if isinstance(o, datetime.timedelta):
            return f"{o.seconds*1000000+o.microseconds}"
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super().default(o)


def get_secret(secret_name):
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    # print("Get Client")
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        # print("Get secret")
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        # print(get_secret_value_response)
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            return json.loads(secret)
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
            return decoded_binary_secret


# Obtener parametros desde el Parameter Store del Systems Manager
# Recibe una lista de nombres de parámetros, ejemplo:
# db_config = get_parameters(["/dev/sql/2016/globals", "/dev/sql/2016/bcredicorp"])
def get_parameters(parameter_name_list):
    ssm = boto3.client('ssm', region_name=os.environ.get('AWS_REGION'))
    configuration_list = ssm.get_parameters(Names=parameter_name_list, WithDecryption=True)
    conn_props = dict()
    # Al diccionario global_config se le hace merge de último,
    # para habilitar el override de parámetros específicos
    # por encima de los globales
    global_config = dict()
    for config in configuration_list['Parameters']:
        param_json = json.loads(config['Value'])
        if config['Name'].find('globals') == -1:
            conn_props = {**param_json, **conn_props}
        else:
            global_config = param_json
    conn_props = {**global_config, **conn_props}
    return conn_props


log_levels = {
    'DEBUG': logging.DEBUG,
    'INFO':  logging.INFO,
    'WARN':  logging.WARN,
    'ERROR': logging.ERROR,
    'FATAL': logging.FATAL
}


def get_log_level(log_level_name: str) -> int:
    if log_level_name in log_levels:
        return log_levels[log_level_name]
    else:
        return logging.INFO
