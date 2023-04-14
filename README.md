# # Tabula - Raspagem de dados das Licitações da Pref. de Taboão da Serra (SP).

Este é um script Python que faz **raspagem das Licitações da Pref. de Taboão da Serra e classifica os dados em um documento do Google Sheets**. O projeto faz parte do trabalho final da conclusão do Master de Jornalismo de Dados, Automação e Data Storytelling do Insper (SP), apresentado ao Profs. Burgos e Cuducos.

---


## Motivação :bulb:

Esse projeto foi desenvolvido com a motivação de preencher um vazio de informação noticiosa dentro da cidade de Taboão da Serra, principalmente a que faz análise das contas públicas locais, pois não existe uma ferramenta, site ou plataforma de fácil utilização onde esses dados possam ser encontrados de forma simples. Este projeto beneficiaria no apoio do trabalho de jornalismo de dados localmente a partir do conteúdo público disponibilizado pela Prefeitura de Taboão da Serra (SP).

Com no próprio Portal da Transparência da cidades, a dificuldade no acesso às informaçãoes é bastante notória, já que a navegação não privilegia a leitura, tampouco o entendimento do que está em análise, de maneira clara e objetiva.

A análise exploratória, ou descritiva, realizada no trabalho apontou que a cidade de Taboão da Serra tem realizado uma quantidade significativa da verba pública em licitações com modalidade 'Dispensa de Licitação', que apresentam alguns empecilhos para identificação de critérios de escolha, concorrência de preços, entre outras. 

A fim de mitigar as dificuldades para capturar, organizar e classificar informaçẽos dos gastos públicos municipais relativos às compras realizadas pela Prefeitura, foi desenvolvido um scrapper de licitações da Prefeitura de Taboão da Serra que, em associação com um bot de Telegram, atua como **provedor de informações sobre as licitações da cidade**.

Dessa forma, o scrapper pode ajudar a garantir a transparência dos processos licitatórios e contribuir para o trabalho de jornalismo de dados.

## Configuração :wrench:

Para usar este script, você precisará fazer o seguinte:

1. Configurar um bot do Telegram e obter sua chave de API.
2. Configurar uma API do Google Sheets e obter as credenciais para acessar o documento desejado.
3. Substitua os valores das variáveis TELEGRAM_API_KEY, TELEGRAM_ADMIN_ID, GOOGLE_SHEETS_CREDENTIALS e planilha_google pela sua própria chave de API, ID do administrador, credenciais e chave do documento do Google Sheets, respectivamente.

---

## Executando o Script :computer:
Para executar o script, basta executá-lo em um ambiente Python.

O script irá configurar uma aplicação web Flask e ouvir solicitações na endpoint/classificar.

Quando uma solicitação é recebida, o script irá classificar os dados do documento do Google Sheets e enviar os resultados para o chat do Telegram com o ID especificado pelo parâmetro chat_id na solicitação.

---

## Dependências :clipboard:
Este script depende dos seguintes pacotes Python:

- Debian
- chromium 
- chromium-driver
- pandas
- oauth2client
- re
- time
- requests

Estes podem ser instalados usando o pip, no caso do Google Colab, ou através do requirements.txt, estratégia abordada aqui.
Recomenda-se o seu uso no Google Colab, local onde foi desenvolvid.

---

## Dificuldades :no_entry_sign:

Durante o projeto, foram enfrentadas algumas dificuldades, especialmente devido ao uso de uma plataforma Google Colab

Isso ocorreu porque houve **uma atualização tanto no Google Colab quanto na biblioteca Seleniu**, o que tornou o processo de validação de erros mais lento. Embora os testes pudessem ser realizados no ambiente Colab e mitigados, a **validação dos erros levou muito, muito tempo**, o que dificultou bastante a construção do projeto.

Além disso, **o tempo necessário para se familiarizar com a plataforma e o domínio necessário do Python** tornaram mais complexa a aprendizagem e leitura da documentação específica para implementação de códigos e bibliotecas.

---

## Aprendizados :heavy_check_mark:

Essas habilidades listadas são essenciais para o trabalho com desenvolvimento de software e análise de dados.

Entre eles, ter um **maior domínio de strings e pandas em Python** permite a manipulação e análise de dados, algo fundamental para diversas aplicações. 

Outro ponto, foi o **melhor entendimento do funcionamento dda raspagem com Selenium** é importante para realizar a integração de diferentes sistemas e aplicações, permitindo a troca de informações de forma mais eficiente e segura. 

A **melhoria das habilidades de scrapping** é importante para coletar e extrair informações de fontes diversas, o que é fundamental para a análise de dados. 

Por fim, ter um **maior domínio das habilidades com manipulação de dados de um dataframe para o Google Sheets** permite a análise e organização de dados de forma mais eficiente e colaborativa. Todos esses conhecimentos podem ser aplicados em diferentes áreas, como inteligência artificial, análise de dados, desenvolvimento de aplicativos, entre outras.

---

## Desafios

- Construir um servidor próprio, seja com um Raspberry Pi 3 ou um computador velho, para não depender mais do Render (nunca mais)
- Melhorar a forma como as tabelas são processada para incluir as Secretarias contendo outras tabelas
- Aprofundamento técnico para melhorar a efiência e eficácia do scrapper
