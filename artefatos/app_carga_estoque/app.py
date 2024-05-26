import json
from datetime import datetime
from random import randint
import boto3


sqs_client = boto3.client('sqs')

def send_message_sqs(mensagem):
    try:
        # Envia a mensagem para a fila SQS
        response = sqs_client.send_message(
            QueueUrl='mercado-puc-queue-estoque',
            MessageBody=mensagem
        )
    except Exception as e:
        raise(f"Ocorreu um erro ao enviar a mensagem: {e}")

    return response["MessageId"]


def run() -> None:
    list_filial = ["1001", "1002"]
    with open('produtos_supermercado.json', 'r', encoding='utf-8') as file:
        content = json.loads(file.read())

    for filial in list_filial:
        itens_tratados = []
        for item in content:
            item["filial"] = filial
            item["qtd_estoque"] = randint(1, 10000)
            item["data_atulizacao_posicao_estoque"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            itens_tratados.append(item)

        qtd_item_batch = 35
        for i in range(0, len(itens_tratados), qtd_item_batch):
            item_batch = itens_tratados[i:i+qtd_item_batch]
            messageId = send_message_sqs(json.dumps(item_batch))
            print(f'Mensagem enviada com sucesso! ID da mensagem: {messageId}')


if __name__ == "__main__":
    run()