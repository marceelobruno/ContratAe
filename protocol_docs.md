# Securitas Protocol ContratAe (SPC) - Documentação

## Descrição
O **Securitas Protocol ContratAe (SPC)** é um conjunto de mensagens e ações desenvolvidas para facilitar a comunicação entre o servidor e as aplicações do sistema ContratAe. Este protocolo visa o compartilhamento eficiente de informações relacionadas a oportunidades de empregos e estágios, simplificando a interação entre talentos e recrutadores.

### Conhecendo o Servidor - (SPC)
O servidor ContratAe utiliza o **SPC** para comunicação, adotando o formato JSON para a troca de dados. Os status codes também são retornados em JSON. Algumas ações suportadas incluem: login, criar, verCandidaturas, verVagas, verPerfil, criarVaga, candidatar, cancelarCandidatura, verificar, e completarPerfil.

# Mensagens do Protocolo

Ao interagir com o protocolo do nosso projeto, você pode encontrar as seguintes mensagens:

- **200 OK**: Indica que a solicitação foi bem-sucedida. A resposta incluirá os detalhes necessários.

- **201 Created**: Indica que a solicitação foi bem-sucedida e resultou na criação de um novo recurso.
  
- **203 Complete**: Indica que o perfil do candidato está completo.

- **400 Bad Request**: Indica que a solicitação do cliente foi inválida ou malformada. O servidor não pode ou não processará a solicitação.

- **401 Unauthorized**: Indica que a autenticação não foi autorizada. 

- **403 Incomplete**: Indica que o perfil do candidato está incompleto. 

- **404 Not Found**: Indica que o recurso solicitado não foi encontrado no servidor.

Esses códigos de mensagem são usados para fornecer informações sobre o estado das solicitações e respostas no contexto do protocolo SPC.

# Mensagens de Protocolo e Seus Parâmetros

## Login
Formato de Esperado:
```json
{
  "protocol_msg": "login",
  "type": "r",
  "cpf": "12345678901",
  "senha": "senha"
}
```

O parâmetro `type` especifica o tipo de usuário, podendo ser "Recrutador" (`r`) ou "Candidato" (`c`).

#### Resposta do Servidor em Caso de Sucesso:

```json
{
    "status": "200 OK",
    "message": "Usuário autenticado.",
    "data": "cpf"
}

```

#### Menssagens de Erro:
```json
{
    "status": "401 Unauthorized",
    "message": "Senha inválida!"
}

{
    "status": "404 Not Found",
    "message": "Usuário não encontrado!"
}
```
## Criar Usuário
Formato de Esperado:
```json
{
  "protocol_msg": "criar",
  "nome": "João da Silva",
  "email": "joao.da.silva@example.com",
  "cpf": "12345678902",
  "type": "c",
  "senha": "senha"
}

{
  "protocol_msg": "criar",
  "nome": "John Doe",
  "email": "JohnDoea@example.com",
  "cpf": "12345675432",
  "type": "r",
  "senha": "senha",
  "empresa": "Securitas Inc"
}
```
O parâmetro empresa é necessário apenas para usuários recrutadores (`r`).

#### Respostas do Servidor:

```json
{
    "status": "201 Created",
    "message": "Usuário criado.",
    "data": "cpf"
}
```
#### Menssagens de Erro:
```json
{
    "status": "400 Bad Request",
    "message": "CPF já cadastrado."
}
```
## Ver Candidaturas
Formato Esperado:
```json
{
    "protocol_msg": "verCandidaturas",
    "type": "type",
    "cpf": "cpf"
}
```
#### Respostas do Servidor:
```json
{
    "status": "200 OK",
    "data": "Lista de vagas"
}

{
    "status": "200 OK",
    "data": "Lista de candidatos"
}
```
#### Menssagens de Erro:
```json
{
    "status": "404 Not Found",
    "message": "Você não se candidatou a nenhuma vaga."
}

{
    "status": "404 Not Found",
    "message": "A vaga não possui candidaturas"
}
````
## Ver Perfil
Formato esperado
```json
{
    "protocol_msg": "verPerfil",
    "cpf": "cpf"
}
```
#### Respostas do Servidor:
```json
{
    "status": "200 OK",
    "data": "usuario_info"
}
```
#### Menssagens de Erro:
```json
{
    "status": "404 Not Found",
    "message": "Usuário não encontrado!"
}
```
## Ver Vagas
Formato esperado
```json
{
    "protocol_msg": "verVagas",
    "type": "type",
    "cpf": "cpf"
}
```
#### Respostas do Servidor:
```json
{
    "status": "200 OK",
    "data": "Lista de Vagas"
}
```
#### Menssagens de Erro:
```json
{
    "status": "404 Not Found",
    "message": "Não há vagas..."
}
```
## Candidatar-se a uma Vaga
Formato esperado
```json
{
    "protocol_msg": "candidatar",
    "idVaga": "7265",
    "cpf": "cpf"
}
```
#### Respostas do Servidor:
```json
{
    "status": "200 OK",
    "message": "Candidatura registrada com sucesso!"
}
```
#### Menssagens de Erro:
```json
{
    "status": "400 Bad Request",
    "message": "Limite de candidaturas alcançado."
}
{
    "status": "400 Bad Request",
    "message": "Você já se candidatou a essa vaga."
}
{
    "status": "404 Not Found",
    "message": "Vaga não encontrada."
}
```
## Criar Vaga
Formato esperado
```json
{
    "protocol_msg": "criar_vaga",
    "cpf": "cpf",
    "vaga_info": {
        "nome_vaga": "Desenvolvedor Python",
        "area_vaga": "Back End",
        "descricao_vaga": "Breve descrição da vaga",
        "quant_candidaturas": "25",
        "salario_vaga": "12000",
        "requisitos": "[Python, Flask, Banco de Dados, Scrum]"
    }
}

```
#### Respostas do Servidor:
```json
{
    "status": "201 Created",
    "message": "Vaga criada!",
    "data": "ID da vaga"
}
```
## Cancelar Candidatura
formato esperado
```json
{
    "protocol_msg": "cancelarCandidatura",
    "idVaga": "3422",
    "cpf": "cpf"
}
```
#### Respostas do Servidor:
```json
{
    "status": "200 OK",
    "message": "Cancelamento efetuado com sucesso."
}

```
#### Menssagens de Erro:
```json
{
    "status": "404 Not Found",
    "message": "Vaga não encontrada."
}
```
## Recuperar Vaga Recrutador
Formato esperado
```json
{
    "protocol_msg": "recuperarVaga",
    "cpf": "cpf"
}
```
#### Respostas do Servidor:
```json
{
    "status": "200 OK",
    "message": "Seu perfil está completo."
}
```
#### Menssagens de Erro:
```json
{
    "status": "404 Not Found",
    "message": "Não há vaga registrada para esse CPF."
}
```
## Completar Perfil
Formato esperado
```json
{
    "protocol_msg": "completarPerfil",
    "cpf": "8364720362",
    "area": "Desenvolvedor Python",
    "descricao": "Breve descrição",
    "skills": "[Python, Flask, Java]",
    "cidade": "João Pessoa",
    "uf": "PB"
}
```
#### Respostas do Servidor:
```json
{
    "status": "201 Created",
    "message": "Seu perfil está completo."
}
```

