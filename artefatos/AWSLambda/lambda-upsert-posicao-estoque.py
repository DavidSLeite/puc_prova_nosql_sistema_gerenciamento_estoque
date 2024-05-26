from datetime import datetime
import json
import boto3
import time


def lambda_handler(event, context):

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('tb_posicao_estoque_filial')
    
    def upsert_dynamo(item):
        partitionKey = item['codigo_barra']
        sortKey = item['filial']

        item_dynamo = {
            'codigo_partitionkey': partitionKey,
            'codigo_sortkey': sortKey,
            'posicao_estoque': item,
            'data_inclusao_item': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        response = table.get_item(Key={'codigo_partitionkey': partitionKey, 'codigo_sortkey':sortKey})

        if ("Item" in response):
            dataposicao_estoque_response = response['Item']['posicao_estoque']['data_atulizacao_posicao_estoque']
            data_posicao_estoque_item = item_dynamo['posicao_estoque']['data_atulizacao_posicao_estoque']

            if data_posicao_estoque_item > dataposicao_estoque_response:
                table.put_item(Item=item_dynamo)
        else:
            table.put_item(Item=item_dynamo)


    for item in event["Records"]:
        item_body = json.loads(item['body'])

        for i in item_body:
            pk = i['codigo_barra']
            sk = i['filial']
            inicio = time.time()
            upsert_dynamo(i)
            fim = time.time()
            latencia = fim - inicio
            print(f"upsert codigo_barra {pk} da loja {sk} Latencia - {round(latencia, 4)}ms")
            
    return {
        'status_code': 200,
        'Message': 'Item Inserted or Updated in DynamoDB'
    }