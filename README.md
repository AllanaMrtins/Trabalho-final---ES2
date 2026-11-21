# Afim Quest

## Plataforma Gamificada para o Ensino de Função Afim

> **Implementação do back-end do projeto final de Engenharia de Software II**

![Status](https://img.shields.io/badge/status-conclu%C3%ADdo-5f8f55)
![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-REST-009688?logo=fastapi&logoColor=white)
![Testes](https://img.shields.io/badge/testes-30%20aprovados-65a30d)

---

## Identificação do projeto

**Instituição:** Universidade Federal do Piauí — UFPI
**Campus:** Senador Helvídio Nunes de Barros — Picos
**Curso:** Bacharelado em Sistemas de Informação
**Disciplina:** Engenharia de Software II
**Professor:** Raí Araújo de Miranda
**Ano:** 2026

### Integrantes

- **Allana**

- **Camily**

- **Janiele**

- **Ana Carolina**

---

## Sobre o projeto

O **Afim Quest** é uma plataforma educacional gamificada para apoiar o ensino e a prática de função afim. A proposta transforma os exercícios de Matemática em uma jornada de missões, na qual o aluno resolve desafios, recebe feedback, acumula experiência, desbloqueia conquistas e acompanha sua evolução.

O sistema também oferece recursos para professores criarem e gerenciarem atividades. A aplicação foi desenvolvida com uma API REST em FastAPI, persistência em banco de dados SQLite e uma interface web integrada para demonstrar o funcionamento da solução.

### Objetivo

Desenvolver uma solução que facilite a aprendizagem de função afim por meio de atividades interativas, correção automática e elementos de gamificação, como XP, níveis, sequência de acertos, conquistas e ranking.

### Problema tratado

Em atividades tradicionais, o estudante muitas vezes recebe apenas uma resposta certa ou errada, sem acompanhar sua evolução ou receber motivação para continuar praticando. O Afim Quest busca melhorar esse processo oferecendo retorno imediato e uma progressão visual baseada em desafios.

---

## Principais funcionalidades

### Para alunos

- Cadastro e autenticação com e-mail e senha.

- Visualização de missões de função afim.

- Filtro de atividades por nível de dificuldade.

- Resolução de questões com correção automática.

- Feedback com dicas relacionadas ao tipo de erro.

- Histórico de respostas.

- Cálculo de desempenho e recomendação de nível.

- Acúmulo de XP no primeiro acerto de cada missão.

- Progressão por níveis.

- Sequência atual e maior sequência de acertos.

- Conquistas desbloqueáveis.

- Ranking com preservação do primeiro nome dos participantes.

- Laboratório interativo com representações algébrica, tabular, gráfica e contextual.

### Para professores

- Cadastro com perfil de professor.

- Criação de atividades.

- Definição do nível da missão.

- Escolha da representação e do tipo de pergunta.

- Consulta das atividades cadastradas.

- Atualização de atividades.

- Exclusão de atividades próprias.

- Visualização do gabarito no painel administrativo.

---

## Tecnologias utilizadas

| Tecnologia | Finalidade |
| --- | --- |
| Python | Linguagem principal do back-end |
| FastAPI | Construção da API REST |
| Uvicorn | Servidor da aplicação |
| SQLAlchemy | Mapeamento objeto-relacional — ORM |
| SQLite | Banco de dados persistente local |
| Pydantic | Validação dos dados de entrada e saída |
| PyJWT | Geração e validação dos tokens JWT |
| Pytest | Testes automatizados |
| HTML, CSS e JavaScript | Interface web gamificada |

---

## Arquitetura do sistema

O projeto utiliza uma **arquitetura em camadas**, organizada para separar responsabilidades e facilitar a manutenção.

```
┌─────────────────────────────────────────┐
│ Interface Web — HTML, CSS e JavaScript  │
└──────────────────┬──────────────────────┘
                   │ HTTP / JSON
┌──────────────────▼──────────────────────┐
│ API — FastAPI e rotas                    │
│ autenticação, atividades, respostas      │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│ Services — casos de uso                  │
│ regras de aplicação e autorização        │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│ Repositories — acesso aos dados         │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│ Models / SQLAlchemy                      │
└──────────────────┬──────────────────────┘
                   │
┌──────────────────▼──────────────────────┐
│ SQLite — funcao_afim.db                  │
└─────────────────────────────────────────┘
```

### Organização das pastas

```
app/
├── api/             Rotas HTTP e dependências de autenticação
├── core/            Configuração, banco, segurança e exceções
├── domain/          Regras puras de função afim e gamificação
├── repositories/    Operações de acesso ao banco de dados
├── services/        Casos de uso e regras de aplicação
├── static/          Interface web do Afim Quest
├── main.py          Inicialização da aplicação FastAPI
├── models.py        Entidades persistidas com SQLAlchemy
└── schemas.py       Validação e contratos da API

tests/               Testes unitários e de integração
public/               Manifesto das rotas da aplicação
```

### Justificativa da arquitetura

A arquitetura em camadas foi escolhida porque o projeto possui regras de negócio, persistência, autenticação e uma interface que precisam evoluir de forma independente. As rotas recebem as requisições, os services coordenam os casos de uso, os repositories isolam o acesso ao banco e o domínio concentra as regras matemáticas e de gamificação.

Essa organização melhora a testabilidade, reduz o acoplamento entre as partes e facilita uma futura troca do SQLite por PostgreSQL. Como limitação, a arquitetura possui mais arquivos e camadas do que uma aplicação pequena em arquivo único, exigindo maior organização da equipe.

---

## Banco de dados e persistência

O projeto utiliza **SQLite** com **SQLAlchemy**. O arquivo `funcao_afim.db` é criado automaticamente na primeira execução da aplicação.

### Entidades principais

#### `usuarios`

Armazena alunos e professores, incluindo nome, e-mail, senha protegida por hash, perfil e data de cadastro.

#### `atividades`

Armazena as missões criadas pelos professores, seus enunciados, níveis, representações, tipos de pergunta, coeficientes e resposta esperada.

#### `respostas`

Registra cada tentativa do aluno, o valor informado, se a resposta estava correta e o momento da tentativa.

### Relacionamentos

- Um usuário pode ser aluno ou professor.

- Um professor pode criar várias atividades.

- Um aluno pode enviar várias respostas.

- Uma atividade pode receber várias respostas.

- Usuários e atividades se relacionam por meio dos registros de respostas.

O sistema oferece operações de cadastro, consulta, atualização e exclusão de atividades. Respostas são registradas como histórico e usuários possuem operações de cadastro, autenticação e consulta do próprio perfil.

---

## Requisitos funcionais implementados

| Requisito | Funcionalidade | Principais rotas |
| --- | --- | --- |
| RF01 | Cadastro de usuário aluno ou professor | `POST /usuarios` |
| RF02 | Autenticação com JWT | `POST /login` |
| RF03 | Gestão de atividades | `POST`, `GET`, `PUT` e `DELETE /atividades` |
| RF04 | Representações da função afim | `POST /funcoes/representacoes` |
| RF05 | Resolução e correção automática | `POST /atividades/{id}/respostas` |
| RF06 | Histórico de respostas | `GET /respostas` |
| RF07 | Desempenho e nível recomendado | `GET /desempenho` |
| RF08 | XP, níveis, conquistas e ranking | `GET /gamificacao` e `GET /ranking` |

### Validação e tratamento de erros

A API valida entradas com Pydantic. Entre as validações implementadas estão e-mail válido, senha com tamanho mínimo, coeficiente angular diferente de zero, tipos de pergunta permitidos e campos obrigatórios conforme o tipo da atividade.

As respostas de erro utilizam códigos HTTP adequados, como `401` para falta de autenticação, `403` para acesso não autorizado, `404` para recurso inexistente, `409` para conflito de cadastro e `422` para dados inválidos.

---

## Sistema de gamificação

A progressão do aluno é baseada em XP:

- Missão de nível 1: **10 XP**.

- Missão de nível 2: **20 XP**.

- Missão de nível 3: **30 XP**.

- O XP é concedido apenas no primeiro acerto de cada atividade.

- A cada **100 XP**, o jogador avança um nível.

### Conquistas

| Conquista | Critério |
| --- | --- |
| Primeiro Passo | Acertar a primeira missão |
| Em Chamas | Conseguir 3 acertos seguidos |
| Imparável | Conseguir 5 acertos seguidos |
| Explorador | Tentar 5 missões diferentes |
| Mestre da Reta | Acertar uma missão de nível 3 |

---

## Como executar o projeto

### Pré-requisitos

- Python 3.10 ou superior;

- `pip` instalado;

- Terminal ou prompt de comando.

### Linux e macOS

```bash
git clone URL_DO_REPOSITORIO
cd funcao-afim-api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

### Windows

```
git clone URL_DO_REPOSITORIO
cd funcao-afim-api
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Depois de iniciar o servidor, abra no navegador:

- **Aplicação web:** [http://127.0.0.1:8000](http://127.0.0.1:8000)

- **Documentação Swagger:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

- **Verificação de saúde:** [http://127.0.0.1:8000/saude](http://127.0.0.1:8000/saude)

Para permitir acesso por outros computadores da mesma rede, execute:

```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Em seguida, acesse pelo IP do computador servidor, por exemplo: `http://192.168.1.25:8000`.

### Variáveis opcionais

- `SECRET_KEY`: chave utilizada na criação dos tokens JWT.

- `DATABASE_URL`: URL alternativa de banco de dados.

- `TOKEN_MINUTES`: tempo de expiração do token de autenticação.

---

## Testes e qualidade

O projeto possui testes unitários para as regras matemáticas e de gamificação, além de testes de integração para as rotas da API, autenticação, autorização, persistência, atividades, respostas, desempenho e ranking.

Para executar:

```bash
python -m pytest -v
```

### Resultado atual

**30 testes aprovados.**

| Caso | Cenário | Resultado esperado | Resultado obtido | Situação |
| --- | --- | --- | --- | --- |
| TC01 | Cadastro válido | Usuário criado sem expor senha | HTTP 201 e senha protegida | Aprovado |
| TC02 | Login válido e inválido | Token para credencial válida e erro para inválida | HTTP 200 e HTTP 401 | Aprovado |
| TC03 | Representação da função | Retornar expressão, raiz e tabela | Dados matemáticos corretos | Aprovado |
| TC04 | Controle de atividades | Professor cria e aluno não cria | HTTP 201 e HTTP 403 | Aprovado |
| TC05 | Resposta de atividade | Corrigir e gerar feedback | Acerto, erro e dica retornados | Aprovado |
| TC06 | Gamificação | Conceder XP apenas no primeiro acerto | XP e nível calculados corretamente | Aprovado |
| TC07 | Rota protegida | Bloquear acesso sem token | HTTP 401 | Aprovado |
| TC08 | Validação | Rejeitar dados inválidos | HTTP 422 | Aprovado |

### Atributos de qualidade

#### Segurança

A autenticação utiliza tokens JWT e as senhas não são armazenadas em texto puro. O sistema também separa permissões de aluno e professor, impedindo que alunos criem ou alterem atividades.

A avaliação pode ser realizada por meio dos testes de login, acesso sem token, controle de perfil e verificação de que senhas não aparecem nas respostas da API.

#### Manutenibilidade

A separação entre rotas, services, repositories, domínio e modelos reduz responsabilidades concentradas em um único módulo. As regras de função afim e gamificação não dependem diretamente do FastAPI ou do banco de dados.

A avaliação pode ser realizada verificando a organização das pastas, a facilidade de localizar cada regra e a execução dos testes após alterações.

#### Testabilidade

As regras matemáticas e de gamificação foram implementadas em funções puras, permitindo testes sem banco de dados. A API também possui testes de integração com banco em memória.

A avaliação é feita executando a suíte automatizada com `pytest` e conferindo o resultado dos cenários unitários e de integração.

#### Usabilidade

A interface apresenta missões, níveis, progresso, feedback, conquistas e ranking de forma visual. Os estados de acerto, erro e evolução são comunicados ao aluno imediatamente.

A avaliação pode ser realizada observando o fluxo de cadastro, login, escolha de missão, resposta e consulta do progresso em diferentes tamanhos de tela.

---

## Limitações atuais

- O SQLite é adequado para demonstração e uso pequeno, mas não é a melhor opção para muitos acessos simultâneos.

- Ainda não existe um sistema completo de turmas e vinculação entre professor e grupo de alunos.

- O ranking atual é geral e não possui filtros por turma.

- A recuperação de senha e a confirmação de e-mail não foram implementadas.

- O sistema não possui publicação em produção neste repositório.

- O histórico não possui uma tela detalhada com gráficos de evolução ao longo do tempo.

## Funcionalidades futuras

- Migração para PostgreSQL em ambiente de produção.

- Cadastro e gerenciamento de turmas.

- Relatórios de desempenho por aluno e por turma.

- Gráficos de evolução e comparação de tentativas.

- Recuperação de senha por e-mail.

- Sistema de trilhas e fases de aprendizagem.

- Mais tipos de exercícios e conteúdos de Matemática.

- Publicação em serviço de hospedagem com domínio próprio.

---

## Gerenciamento de configuração

O projeto deve ser mantido em um repositório Git. Recomenda-se registrar cada entrega em commits pequenos e descritivos, por exemplo:

```bash
git init
git add .
git commit -m "feat: estrutura inicial da API"
git checkout -b feature/atividades
git add .
git commit -m "feat: implementar gerenciamento de atividades"
```

As branches podem ser utilizadas para separar funcionalidades, correções e melhorias da interface. O repositório final deve conter o histórico de commits e a participação dos integrantes **Allana, Camily, Janiele e Ana Carolina**.

---

## Licença acadêmica

Projeto desenvolvido para fins acadêmicos na disciplina de Engenharia de Software II da Universidade Federal do Piauí — UFPI.