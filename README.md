# Automação para Redefinição de senhas
> RPA dedicado e automatizar o processo de redefinição de senhas de usuários master de todas as plataformas dos clientes de uma empresa.

![v3.11.3][python-image] ![v22.3.1][pip-image]

O projeto consiste na integração com o Google Cloud para consultar e editar informações de uma planilha do Sheets. Nessa planilha, iremos consultar o ID de cada usuário master referente a uma plataforma de cliente, para posteriormente realizar um loop na sessão de edição dos dados "/edit/{ID}" e atualizar sua senha.

Dentro do escopo deste script, temos uma função que gera senhas seguras e aleatórias dentro dos padrões da LGPD, definindo uma senha individual para cada usuário. Nesse processo, após o sucesso da redefinição, atualizamos com a nova senha na planilha, também através da API do Google. 

## Instalação das dependências

Linux/Windows:

```sh
pip install -r requirements.txt
```

## Execução do projeto

```sh
python -m reset_project
```

<!-- Markdown link & img dfn's -->
[python-image]: https://img.shields.io/badge/python-version?style=flat&logo=python&label=v3.11.3&color=yellow
[python-url]: https://www.python.org/downloads/windows/
[pip-image]: https://img.shields.io/badge/pip-version?style=flat&logo=Pypi&label=v22.3.1&color=blue
