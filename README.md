Integração FTP para Importação e Processamento de Pedidos no ERP Infarma

Descrição:
Este repositório contém um código desenvolvido para realizar a integração com um servidor FTP, visando a importação de arquivos de pedidos de fornecedores. O código é projetado para filtrar os arquivos de pedidos com base no CNPJ presente em cada um deles e, em seguida, compará-los com os registros armazenados em um banco de dados.

O processo de importação começa com a conexão ao servidor FTP, onde o código acessa o diretório específico para a importação dos arquivos de pedidos. Cada arquivo é analisado, e o CNPJ associado é extraído para realizar a comparação com os registros do banco de dados. Caso haja correspondência entre o CNPJ do arquivo e um CNPJ registrado no banco, o pedido é considerado válido e é enviado para o processamento no ERP Infarma.

No ERP Infarma, o pedido é processado, e uma resposta é gerada pelo sistema contendo informações sobre o status do processamento e possíveis erros ou avisos. Essa resposta é enviada de volta ao servidor FTP pelo código, para que o remetente do pedido possa obter feedback sobre o processamento realizado.

O código é estruturado de forma modular e possui uma documentação abrangente, facilitando a manutenção, a extensão e a compreensão de suas funcionalidades. Além disso, são adotadas boas práticas de programação, como tratamento de exceções e logging adequado, para garantir a robustez e a confiabilidade do sistema.

A integração FTP é realizada por meio de bibliotecas e módulos padronizados, permitindo a fácil adaptação para diferentes ambientes de servidor FTP, caso seja necessário. Além disso, são incluídos testes automatizados para validar as funcionalidades principais e evitar regressões ao longo do desenvolvimento do código.

Este projeto visa otimizar e automatizar o processo de importação e processamento de pedidos no ERP Infarma, reduzindo o tempo de espera para a realização de pedidos.




https://docs.google.com/forms/d/e/1FAIpQLSeTYy1_IM0FOfpAILQ21P5zRPAuVgqR9REUunTsZl5JWFc5Jg/viewform
