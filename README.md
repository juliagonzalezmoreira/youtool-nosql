<h1 align="center">
  Projeto NoSQL: Coleta de Dados do YouTube com youtool
</h1>

<p align="center">
	<b><i>
Este é um projeto prático para a disciplina Laboratório de Banco de Dados, cijo objetivo é coletar e armazenar dados do YouTube utilizando a API do YouTube, a biblioteca youtool, e o MongoDB.
  </i></b>
</p>

<p align="center">
	<img alt="Tamanho do código no GitHub em bytes" src="https://img.shields.io/github/languages/code-size/juliagonzalezmoreira/youtool-nosql?color=6272a4" />
	<img alt="Linguagem principal" src="https://img.shields.io/github/languages/top/juliagonzalezmoreira/youtool-nosql?color=6272a4"/>
</p>

## 📁 Estrutura
- `.env`                   : Variáveis de ambiente (MONGO_URI, YOUTUBE_API_KEYS, CHANNEL_URL)
- `etl.py`                  : Script principal de coleta e processamento de dados
- `requirements.txt`        : Arquivo com dependências do projeto
- `test_etl.py`             : Testes automatizados para o código
- `README.md`                Informações do projeto.
- `.gitignore`              : Arquivo para ignorar arquivos 
  
## 🎯 Objetivos
* Utilizar a biblioteca youtool para acessar a API do YouTube e coletar dados.
* Armazenar os dados coletados em um banco de dados NoSQL (MongoDB).
* Aplicar conceitos aprendidos em NoSQL, manipulação de dados e integração com APIs externas.

## 🎥 Canal de Análise
* Para este projeto, escolhi o canal [Amelia Dimoldenberg](https://www.youtube.com/@AmeliaDimoldenberg) para coletar os dados.

## 📌 Funcionalidades Implementadas
* Coleta de Vídeos: Coleta dados sobre os vídeos de um canal do YouTube (ID, título, descrição, etc.).
* Coleta de Comentários: Coleta os comentários de cada vídeo do canal.
* Coleta de Transcrições: Coleta as transcrições dos vídeos, caso estejam disponíveis.
* Coleta de Livechat/Superchat: Coleta informações de chats ao vivo, incluindo superchats.

## 🔎 Testes
1. test_get_db:
* Objetivo: Verificar se a função get_db conecta corretamente ao MongoDB com a URI configurada.
* O que é testado: Confirma se a URI do MongoDB é usada corretamente para estabelecer a conexão.
2. test_get_yt:
* Objetivo: Testar se a função get_yt configura corretamente o cliente da API do YouTube com as chaves de API.
* O que é testado: Verifica se as chaves de API são passadas corretamente para a biblioteca youtool.
3. test_fetch_and_store:
* Objetivo: Verificar se a função fetch_and_store coleta e armazena vídeos do YouTube no MongoDB.
* O que é testado: Confirma que os vídeos são armazenados corretamente e o número de vídeos processados é o esperado.
4. test_fetch_and_store_comments:
* Objetivo: Testar se a função fetch_and_store_comments coleta e armazena os comentários dos vídeos no MongoDB.
* O que é testado: Verifica se os comentários são armazenados corretamente com atributos como autor e conteúdo.
5. test_fetch_and_store_transcriptions:
* Objetivo: Verificar se a função fetch_and_store_transcriptions coleta e armazena as transcrições dos vídeos no MongoDB.
* O que é testado: Confirma que as transcrições são coletadas e armazenadas corretamente, incluindo o status e nome do arquivo.
6. test_fetch_and_store_livechat:
* Objetivo: Testar se a função fetch_and_store_livechat coleta e armazena dados do livechat (incluindo superchats) no MongoDB.
* O que é testado: Verifica se as mensagens do livechat e os superchats são armazenados corretamente, validando valores monetários dos superchats.

## 🛠️ Tecnologias Usadas
* Python
* youtool (biblioteca para interagir com a API do YouTube)
* MongoDB (Banco de Dados NoSQL)
* pytest (framework para testes)
* mongomock (mocking para testes com MongoDB)
* python-dotenv (carregamento de variáveis de ambiente)

## 📍 Instruções 

### Pré-Requisitos
Para executar o projeto localmente, é necessário ter os seguintes requisitos:
- [Python](https://www.python.org/)
- [MongoDB](https://www.mongodb.com/)

❗️ Certifique-se de que todas as ferramentas necessárias estejam instaladas em sua máquina local e, em seguida, prossiga com os seguintes passos. <br>

### Instruções para executar o projeto em sua máquina:

**0. Baixe os arquivos**

```bash
# Clone o repositório
$ git clone https://github.com/juliagonzalezmoreira/youtool-nosql
```
**1. Instale as dependências**

```
pip install -r requirements.txt
```
**2. Configure as variáveis de ambiente**

Crie um arquivo .env e adicione as variáveis de ambiente:

```
MONGO_URI="mongodb+srv://<usuario>:<senha>@cluster0.mongodb.net/youtube_data?retryWrites=true&w=majority"
YOUTUBE_API_KEYS="sua_api_key_1,sua_api_key_2"
CHANNEL_URL="https://youtube.com/@AmeliaDimoldenberg"
```

**3. Execute os testes automatizados**
```
pytest
```

🔗 Referências
- [Biblioteca youtool](https://github.com/PythonicCafe/youtool)
- Documentação do trabalho enviada pelo professor Fernando Masanori

✅ Feedback
Caso tenha algum feedback, entre em contato!

<a href = "mailto:juliagonzalezmoreira@gmail.com"><img src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white"></a> <a href="https://www.linkedin.com/in/julia-gonzalez-moreira/" target="_blank"><img src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white" target="_blank"></a>

<p align="center"> Desenvolvido com 💜 por Julia Gonzalez Moreira </p>
