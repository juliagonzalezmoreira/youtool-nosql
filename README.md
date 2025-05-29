<h1 align="center">
  Projeto NoSQL: Coleta de Dados do YouTube com youtool
</h1>

<p align="center">
	<b><i>
Este é um projeto prático para a disciplina Laboratório de Banco de Dados, cujo objetivo é coletar e armazenar dados do YouTube utilizando a API do YouTube, a biblioteca youtool, e o MongoDB.
  </i></b>
</p>

<p align="center">
	<img alt="Tamanho do código no GitHub em bytes" src="https://img.shields.io/github/languages/code-size/juliagonzalezmoreira/youtool-nosql?color=6272a4" />
	<img alt="Linguagem principal" src="https://img.shields.io/github/languages/top/juliagonzalezmoreira/youtool-nosql?color=6272a4"/>
</p>

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

## 📁 Estrutura
- `project.py`                  : Script principal de coleta e processamento de dados
- `tests_all.py`                  : Script de testes
- `reset_db.py`                  : Reseta o banco caso necessário
- `requirements.txt`        : Arquivo com dependências do projeto
- `README.md`                Informações do projeto.
- `.gitignore`              : Arquivo para ignorar arquivos 

## 🛠️ Tecnologias Usadas
* Python
* youtool (biblioteca para interagir com a API do YouTube)
* MongoDB (Banco de Dados NoSQL)

## 📍 Instruções 

### Pré-Requisitos
Para executar o projeto localmente, é necessário ter os seguintes requisitos:
- [Python](https://www.python.org/)
- [MongoDB](https://www.mongodb.com/)
- [API Keys](https://console.cloud.google.com/)

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
YOUTUBE_API_KEYS="chave_api1, chave_api2"
CHANNEL_URL="https://youtube.com/@seu-canal"
MONGO_URI="mongodb+srv://<user>:<senha>@cluster0.slcacxc.mongodb.net/..." #Atlas MongoDB
DB_NAME=youtube_analysis #nome do banco
SINCE=2024-01-01T00:00:00Z
TRANSCRIPTION_LANG=en
TRANSCRIPTION_DIR=./transcricoes
```

**3. Execute**
```
py project.py
```
   ### GIF
  ![project](https://github.com/user-attachments/assets/d97a404f-e9b2-4c1d-a293-cc109160aa7c)

<details>
  <summary>📸 Resultados do projeto (clique para expandir)</summary>
	
  ### Testes
  ![tests](https://github.com/user-attachments/assets/6cd586ce-d587-4bc9-81be-39b95ab655e0)

  ### MongoDB
  ![bd](https://github.com/user-attachments/assets/eae1299c-9dae-4e81-93b1-a60c9951deee)

</details>

## 🔗 Referências
- [Biblioteca youtool](https://github.com/PythonicCafe/youtool)
- Documentação do trabalho enviada pelo professor Fernando Masanori

## ✅ Feedback

Caso tenha algum feedback, entre em contato!

<a href = "mailto:juliagonzalezmoreira@gmail.com"><img src="https://img.shields.io/badge/Gmail-D14836?style=for-the-badge&logo=gmail&logoColor=white"></a> <a href="https://www.linkedin.com/in/julia-gonzalez-moreira/" target="_blank"><img src="https://img.shields.io/badge/-LinkedIn-%230077B5?style=for-the-badge&logo=linkedin&logoColor=white" target="_blank"></a>

<p align="center"> Desenvolvido com 💜 por Julia Gonzalez Moreira </p>
