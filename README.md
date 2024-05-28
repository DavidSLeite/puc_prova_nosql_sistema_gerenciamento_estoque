# Apresentação de Solução na Nuvem AWS para Sistema de Gerenciamento de Estoque

Este projeto visa desenvolver um sistema de gerenciamento de estoque na nuvem AWS para uma cadeia de supermercados com várias filiais.

A solução proposta garantirá uma gestão eficiente e centralizada dos estoques, proporcionando visibilidade em tempo real, escalabilidade, segurança e alta disponibilidade.

#### Arquitetura da Solução
![](https://github.com/DavidSLeite/puc_prova_nosql_sistema_gerenciamento_estoque/blob/main/artefatos/images/desenho_solucao.png?raw=true)

#### 1 - Camada de Aplicação

* Aplicação principal responsável pelo modulo de cadastros, vendas e gerenciamento de estoque.
A aplicação PDV implantada em cada filial será responsável por publicar numa fila de menssageria a posição do estoque, assim garantindo comunicação assincrona entre aplicação e banco de dados.


#### 2 - Camada de Integração e Serviços

* Amazon API Gateway: Interface para integração com outros sistemas e aplicativos, permitindo que as filiais acessem os dados de estoque de maneira segura e eficiente.
* AWS Lambda: Funções serverless para processamento de eventos, como atualizações e consulta de estoque em tempo real.
* Amazon SQS: Filas para gerenciamento de tarefas assíncronas, como processamento de pedidos e sincronização de dados entre filiais.

#### 3 - Camada de Banco de Dados

* Amazon DynamoDB: Banco de dados NoSQL para armazenamento de dados de estoque de produtos.

## Caracteristicas AWS DynamoDB

O Amazon DynamoDB é um serviço de banco de dados NoSQL gerenciado, oferecido pela AWS, que utiliza um modelo de dados baseado em chave-valor, No modelo chave-valor, os dados são armazenados como pares de chave e valor, onde cada chave é única e está associada a um valor. Esse valor pode ser um documento estruturado em JSON ou um simples atributo.

O modelo de Escalabilidade Horizontal facilita a distribuição de dados entre múltiplos servidores, permitindo que o DynamoDB escale horizontalmente de forma eficiente. Isso significa que ele pode lidar com grandes volumes de dados e tráfego de consultas com facilidade.

A operação baseada em chave-valor garante baixa latência nas operações de leitura e escrita, o que é crucial para aplicações que requerem respostas rápidas e proximas do tempo real.

## Provisionamento DynamoDB

### Modo On-Demand

O modo On-Demand do Amazon DynamoDB é projetado para fornecer flexibilidade e simplicidade de gerenciamento ao escalar automaticamente a capacidade de leitura e escrita conforme a necessidade. Aqui estão algumas características principais desse modo:

- Escalabilidade Automática: O modo On-Demand ajusta automaticamente a capacidade de leitura e escrita de acordo com o tráfego da aplicação, eliminando a necessidade de planejamento de capacidade.

- Pagamento por Uso: Em vez de pagar por uma capacidade provisionada, os usuários pagam apenas pelas leituras e escritas que realizam. Isso pode ser mais econômico para aplicações com padrões de tráfego imprevisíveis ou sazonais.

- Simplificação de Gerenciamento: Não há necessidade de monitorar ou ajustar a capacidade manualmente, reduzindo a sobrecarga administrativa e permitindo que os desenvolvedores se concentrem em outras tarefas.

- Alta Disponibilidade e Desempenho: O DynamoDB em modo On-Demand ainda garante alta disponibilidade e baixa latência, mesmo durante picos de tráfego inesperados.

### Modo Provisioned

O modo Provisioned permite aos usuários especificar a capacidade de leitura e escrita antecipadamente. Esse modo é ideal para aplicações com padrões de tráfego previsíveis. As principais características incluem:

- Controle de Capacidade: Os usuários podem definir a quantidade de capacidade de leitura e escrita necessária, permitindo um controle preciso sobre os recursos utilizados.

- Custos Previsíveis: Como a capacidade é provisionada antecipadamente, os custos são mais previsíveis e podem ser otimizados para cargas de trabalho estáveis.

- Reserva de Capacidade: DynamoDB oferece a opção de reservar capacidade, o que pode resultar em descontos significativos em comparação com o pagamento sob demanda.

- Escalabilidade Personalizada: Os usuários podem ajustar a capacidade provisionada manualmente ou utilizar o auto scaling para ajustar automaticamente a capacidade com base em políticas predefinidas, garantindo que a aplicação tenha sempre os recursos necessários.

- Desempenho Consistente: Com capacidade provisionada, o desempenho da aplicação pode ser mais consistente, pois a capacidade de leitura e escrita é garantida de acordo com as configurações especificadas.


## Atenção!!!

Essa documentação foi criada para avaliação final da disciplina **Bancos de Dados Nosql**, maiores informações sobre provisionamento de recursos que não seja o dynamodb não será abordado nessa demonstração.

A criação dos recursos SQS e API Gateway só serão mencionados aqui.

O código de ingestão e consulta que serão adicinados ao AWS Lambda estarão contidos neste repositório, mas não será abordado a criação e detalhes do provisionamento deste na conta AWS.

### Demonstração e teste


1° Passo: Criação das filas SQS

![](https://github.com/DavidSLeite/puc_prova_nosql_sistema_gerenciamento_estoque/blob/main/artefatos/images/sqs.png?raw=true)

2° Passo: Criação das AWS Lambda Function

![](https://github.com/DavidSLeite/puc_prova_nosql_sistema_gerenciamento_estoque/blob/main/artefatos/images/lista_lambda.png?raw=true)

Importantente realizar o vinculo entre a fila **mercado-puc-queue-estoque** e o lambda **lambda-upsert-posicao-estoque**, sendo que a cada evento inserido na fila será triggado o lambda que por sua vez irá se integrar com o DynamoDB.

![](https://github.com/DavidSLeite/puc_prova_nosql_sistema_gerenciamento_estoque/blob/main/artefatos/images/lambda_upsert.png?raw=true)

Os códigos que foram utilizados nos lambdas estão contidos neste repositório.

```artefatos/AWSLambda/lambda-upsert-posicao-estoque.py```

```artefatos/AWSLambda/lambda-query-posicao-estoque.py```

3° Provisionamento do DynamoDB

Criação da tabela com PartitionKey e SortKey

![](https://github.com/DavidSLeite/puc_prova_nosql_sistema_gerenciamento_estoque/blob/main/artefatos/images/create_dy_pt1.png?raw=true)

Configuração do provisionamento da tabela, a tabela irá usar 5 DPUs para leitura e 5 DPUs para escrita.

O provisionamento de Auto Scaling estará ativo com no mínimo 5 DPUs e no máximo 10 DPUs para ambos (Leitura/Escrita), podendo a qualquer momento ser ajustado conforme a necessidade.

![](https://github.com/DavidSLeite/puc_prova_nosql_sistema_gerenciamento_estoque/blob/main/artefatos/images/create_dy_pt2.png?raw=true)

Um DPU (DynamoDB Processing Unit) é uma unidade de medida utilizada pelo DynamoDB para definir a capacidade de processamento e o consumo de recursos em operações de leitura e escrita em tabelas.

Entender DPUs ajuda a gerenciar custos e desempenho ao usar o DynamoDB, seja em modo provisionado ou on-demand.

### Custo estimado

![](https://github.com/DavidSLeite/puc_prova_nosql_sistema_gerenciamento_estoque/blob/main/artefatos/images/create_dy_pt3.png?raw=true)

![](https://github.com/DavidSLeite/puc_prova_nosql_sistema_gerenciamento_estoque/blob/main/artefatos/images/create_dy_pt3_custos.png?raw=true)

### Teste de carga

Iremos fazer um teste de carga para evidênciar a latência na inserção ou consultas de registros no DynamoDB.

Para isso foi utilizado o script python ```artefatos/app_carga_estoque/app.py``` que envia menssagens em batch para a fila SQS, e para uso do mesmo será necessário a instalação e configuração do ```AWS CLI``` em sua maquina local e instalação da lib boto3 com pip do python.

Outra opção é postar uma mensagem direto na fila SQS pelo console AWS.

![](https://github.com/DavidSLeite/puc_prova_nosql_sistema_gerenciamento_estoque/blob/main/artefatos/images/carga.png?raw=true)

![](https://github.com/DavidSLeite/puc_prova_nosql_sistema_gerenciamento_estoque/blob/main/artefatos/images/itens_dynamodb.png?raw=true)

O DynamoDB é um banco de dados que responde requisições em baixa latência, é possível acompanhar isso nos logs do lambda ```lambda-upsert-posicao-estoque``` pois para realizar o upsert, esse lambda primeiro requisita o item na base do dynamodb, caso o item exista ele atualiza o registro senão ele insere o mesmo no dynamodb.

![](https://github.com/DavidSLeite/puc_prova_nosql_sistema_gerenciamento_estoque/blob/main/artefatos/images/latencia_dynamo.png?raw=true)

Agora com os itens carregados na tabela podemos fazer query no DynamoDB através do lambda ```lambda-query-posicao-estoque```, para esse teste fizemos a consulta diretamente no console do aws lambda.

Essa Lambda Function está programada para receber dois tipos de payloads (Query ou Scan), segue abaixo o payload de entrada e o comportamento de saída:


Payload Query

```
{
  "codigo_barra": "5140642011605",
  "filial": "1001",
  "query_type": "query"
}
```

Saída:

![](https://github.com/DavidSLeite/puc_prova_nosql_sistema_gerenciamento_estoque/blob/main/artefatos/images/lambda_query.png?raw=true)

Payload Scan

```
{
  "query_type": "scan",
  "quantidade_itens": 5
}
```

Saída:

![](https://github.com/DavidSLeite/puc_prova_nosql_sistema_gerenciamento_estoque/blob/main/artefatos/images/lambda_scan.png?raw=true)

Em um caso real quando o API Gateway receber uma requisição POST com o payload de "Query" ou "Scan", a aplicação receberá um json como resposta:

Resposta Scan

Resposta Query

```
{
  "status_code": 200,
  "Message": "SUCCESS",
  "Item": {
    "nome_produto": "Café",
    "filial": "1001",
    "data_atulizacao_posicao_estoque": "2024-05-27 21:16:31",
    "qtd_estoque": 3011,
    "codigo_barra": "5140642011605"
  }
}
```

```
{
  "status_code": 200,
  "Message": "SUCCESS",
  "Itens": [
    {
      "nome_produto": "Café",
      "filial": "1001",
      "data_atulizacao_posicao_estoque": "2024-05-27 21:16:31",
      "qtd_estoque": 3011,
      "codigo_barra": "5140642011605"
    },
    {
      "nome_produto": "Café",
      "filial": "1002",
      "data_atulizacao_posicao_estoque": "2024-05-27 21:16:36",
      "qtd_estoque": 3361,
      "codigo_barra": "5140642011605"
    },
    {
      "nome_produto": "Barra de Cereal",
      "filial": "1001",
      "data_atulizacao_posicao_estoque": "2024-05-27 21:16:31",
      "qtd_estoque": 1810,
      "codigo_barra": "2733750189730"
    },
    {
      "nome_produto": "Barra de Cereal",
      "filial": "1002",
      "data_atulizacao_posicao_estoque": "2024-05-27 21:16:36",
      "qtd_estoque": 1420,
      "codigo_barra": "2733750189730"
    },
    {
      "nome_produto": "Laranja",
      "filial": "1001",
      "data_atulizacao_posicao_estoque": "2024-05-27 21:16:31",
      "qtd_estoque": 2101,
      "codigo_barra": "1140106125130"
    }
  ]
}
```


### Encerramento

Chegamos ao fim deste trabalho de apresentação da solução na nuvem AWS para o sistema de gerenciamento de estoque.

Ao longo deste documento, detalhamos etapas do desenvolvimento, desde a concepção inicial até a implementação final, destacando as funcionalidades e benefícios que esta solução oferece.

O objetivo foi apresentar uma arquitetura que não só atende às necessidades atuais de gerenciamento de estoque, mas que também seja escalável e performático.

Espero que as informações apresentadas aqui tenham sido claras e úteis, fornecendo uma visão abrangente sobre a capacidade não só do Dynamodb mas também o potencial da nuvem AWS.

