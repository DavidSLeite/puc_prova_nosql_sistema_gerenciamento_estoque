
from datetime import datetime
import json
import boto3
import time
from decimal import Decimal


def lambda_handler(event, context):

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('tb_posicao_estoque_filial')

    partitionKey = event.get('codigo_partitionkey')
    sortKey = event.get('codigo_sortkey')
    query_type = event.get('query_type')
    qtd_itens = event.get('quantidade_itens')

    def decimal_default(obj):
        if isinstance(obj, Decimal):
            return float(obj)
        raise TypeError

    def query_scan_dynamo() -> dict:
        response = table.scan(
            Limit=qtd_itens
        )

        lista_item = []
        for item in response['Items']:
            lista_item.append(item['posicao_estoque'])

        return lista_item
    
    def query_dynamo(partitionKey, sortKey) -> dict:

        response = table.get_item(Key={'codigo_partitionkey': partitionKey, 'codigo_sortkey':sortKey})

        if ("Item" in response):
            response = response['Item']['posicao_estoque']
        else:
            response = {}

        return response
    
    if query_type == 'query':
        inicio = time.time()
        response = query_dynamo(partitionKey, sortKey)
        fim = time.time()
        latencia = fim - inicio
        print(f"Query {partitionKey} da loja {sortKey} Latencia - {round(latencia, 4)}ms")
    elif query_type == 'scan':
        inicio = time.time()
        response = query_scan_dynamo()
        fim = time.time()
        latencia = fim - inicio
        print(f"Query Scan top {qtd_itens} Latencia - {round(latencia, 4)}ms")
    
    return {
        'status_code': 200,
        'Message': 'SUCCESS',
        'Item': json.dumps(response, default=decimal_default, ensure_ascii=False)
    }