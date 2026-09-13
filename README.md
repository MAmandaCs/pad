# 📋 Atividades avaliativas do curso de Programação e Análise de Dados com Python

**Programação e Análise de Dados com Python** · PPGE/UFPB · 2026.2

Prof. Dr. Hilton Ramalho

Este repositório-modelo é da disciplina. Seguindo as instruções abaixo, você
cria a sua própria cópia, individual, onde as atividades avaliativas são
desenvolvidas e entregues — não há upload de arquivo em lugar nenhum. A
entrega oficial só acontece quando o **link do seu repositório** é enviado no
Google Sala de Aula (veja "Instruções para realização e entrega" abaixo).

> ⚠️ **Crie o seu repositório como público.** É assim que o professor acessa
> a correção direto pelo link, sem precisar de convite. Isso também significa
> que a sua **matrícula fica visível** no notebook (você a digita no Passo 0
> de cada atividade) — é um dado que identifica só você mesmo, mas se isso te
> incomodar, fale com o professor sobre criar o repositório como privado e
> adicioná-lo como colaborador.

As atividades compõem o instrumento **"Exercícios práticos por bloco"**, que
vale **30% da nota final**.

Cada relatório tem o seu próprio tema, mas todos seguem a mesma estrutura descrita a seguir.

---

## 🚀 Instruções para realização e entrega da atividade

1. Faça login na sua conta do GitHub (crie uma gratuita em
   [github.com](https://github.com) se ainda não tiver — o botão do próximo
   passo só aparece com você **logado**). Acesse o repositório da disciplina
   e clique em **"Use this template" → "Create a new repository"**. Essa
   etapa cria um novo repositório, independente, a partir do template
   fornecido pelo professor — deixe a visibilidade como **pública**.
2. Clone o seu novo repositório para o computador e desenvolva a atividade
   utilizando sua IDE preferida, como VS Code, Antigravity ou Cursor:

   ```bash
   git clone <endereço do SEU repositório>
   cd <nome-do-seu-repositório>
   ```

3. Ao finalizar toda a atividade, salve e envie suas alterações para o
   GitHub usando os comandos do git. A última célula de cada notebook —
   `assinatura()` — imprime a linha exata que vai na mensagem do commit
   final; o passo a passo completo (o que preencher, o que rodar, em que
   ordem) está na seção "Fechando a entrega" do próprio notebook.

> 💡 **Não quer instalar nada?** GitHub Codespaces (botão _Code →
> Codespaces_ na página do repositório) e Google Colab (_File → Open
> notebook → GitHub_) também servem — no Colab, lembre de subir a pasta
> `scripts/` e de **baixar o `.ipynb` e commitá-lo** no fim, já que ele não
> dá push sozinho. Em qualquer uma das formas, o diretório de trabalho
> precisa ser a raiz do repositório (onde ficam o notebook e a pasta
> `scripts/`).

### Entrega

A entrega possui duas partes:

- **Parte 1 — GitHub:** certifique-se de que todo o código e os arquivos da
  atividade foram enviados para o seu repositório público no GitHub.
- **Parte 2 — Google Sala de Aula:** acesse a atividade no Google Sala de
  Aula e cole o link público do seu repositório no GitHub no campo de
  entrega. **É esse link que registra a entrega** — sem ele o professor não
  sabe que você terminou, mesmo que o push tenha funcionado.

> ⚠️ **Importante:** antes de enviar a atividade, verifique se o
> repositório está **público** e se todas as alterações foram efetivamente
> enviadas para o ramo `main`.

> 💡 **Commits durante o trabalho são bem-vindos.** Commit a cada exercício
> resolvido, se quiser — nada no histórico é penalizado. Vale o **último
> commit antes do prazo**; o link só precisa ser colado uma vez no Google
> Sala de Aula, mesmo que você continue commitando depois.

A correção volta como **nota e comentário no Google Sala de Aula** — é lá que
a conversa continua, e é lá que você responde se discordar de algum ponto.

---

## 🗂️ As atividades

| #   | Relatório                                                                                 | Aulas | Unidade | Prazo         |
| --- | ----------------------------------------------------------------------------------------- | ----- | ------- | ------------- |
| 01  | [A Régua do Observatório Econômico Municipal](atividade-01-a-regua-do-observatorio.ipynb) | 1–2   | U1      | dom **30/08** |
| 02  | *em breve*                                                                                 | 3–4   | U1      | dom **06/09** |
| 03  | *em breve*                                                                                 | 5–6   | U1      | dom **20/09** |

> As demais atividades são publicadas ao longo do semestre. Quando uma nova
> for liberada, o professor avisa e você sincroniza o repositório com o
> template (as instruções vêm no aviso).

---

## 🎯 Como funciona

### Os seus dados são só seus

No **Passo 0** de cada notebook você digita a sua matrícula. Ela passa por um
resumo criptográfico **SHA-256** que semeia o gerador de dados: todo o
cenário da atividade — o município, o ativo, o jogo, o consumidor, depende
do relatório — sai dali.

Trocar um único dígito da matrícula produz um cenário inteiramente diferente.
Isso tem duas consequências práticas:

- **o notebook do colega não serve para você**, mesmo que o código dele esteja
  perfeito — os números são outros;
- **o professor confere qualquer entrega** recalculando os dados a partir da
  sua matrícula.

Discutir a _lógica_ com os colegas continua sendo bem-vindo e recomendado. O
que não transfere é a resposta.

### O que vale ponto

| Critério                                | Pontos |
| --------------------------------------- | ------ |
| Correção técnica dos exercícios         | 4,0    |
| Previsão e rastreamento (Parte 1)       | 1,5    |
| Questão autoral                         | 2,0    |
| Diário de bordo + relato do obstáculo   | 1,5    |
| Reflexão obrigatória + declaração de IA | 1,0    |

O código vale **menos da metade**. Os outros 6,0 pontos estão em coisas que só
você pode produzir: o que você previu antes de rodar, o obstáculo que
realmente te travou, a questão que você inventou, a reflexão sobre o que foi
difícil.

Essa distribuição é deliberada, e a razão está dita abertamente na seção
[🤖 Sobre IA](#-sobre-ia).

### As funções do kit

Cada atividade traz o seu kit em `scripts/kit_rNN.py`. A interface é sempre a
mesma:

| Função                     | Para quê                                         |
| -------------------------- | ------------------------------------------------ |
| `iniciar(matricula, nome)` | liga o kit e cria os seus dados                  |
| `prever(...)`              | carimba a sua previsão **antes** de você revelar |
| `registrar(etapa, nota)`   | marca uma etapa no seu diário de bordo           |
| `conferir(etapa, ...)`     | devolve um retorno sobre o que você resolveu     |
| `diario()`                 | mostra o seu ritmo de trabalho                   |
| `assinatura()`             | emite a linha de entrega                         |

**O `conferir()` não tira ponto e não quebra o notebook.** Ele olha o que você
respondeu e diz, item a item, o que ainda não fecha — dando uma **pista**,
nunca a resposta. Rode quantas vezes quiser: errar ali não custa nada, é
exatamente para isso que ele existe.

**O diário de bordo é seu e está à vista.** Ele fica em `diario-rNN.json`, ao
lado do notebook, e você lê quando quiser com `diario()`. Nada é coletado às
escondidas. Na correção, o que conta são as **notas** que você escreveu em
cada `registrar()` — uma nota específica ("travei no `elif`, tinha esquecido os
dois-pontos") vale mais que dez registros vazios.

---

## 🤖 Sobre IA

A política por unidade é a do programa (§5.2):

| Unidade                         | Aulas | Política                        |
| ------------------------------- | ----- | ------------------------------- |
| **U1** — Fundamentos de lógica  | 1–10  | IA generativa **não permitida** |
| **U2** — Estruturas e dados     | 11–20 | permitida **com declaração**    |
| **U3** — Análise e visualização | 21–30 | permitida **com declaração**    |

A declaração é obrigatória em todas as atividades: de **não-uso** na U1, e em
formato de tabela na U2 e na U3 —

| ferramenta | o que pedi (prompt literal) | o que aceitei | o que rejeitei e por quê |

A coluna _"o que rejeitei"_ é a que interessa: ela exige que você tenha julgado
a saída, e não apenas colado.

### O desenho é honesto com você

Nenhuma parte desta disciplina tenta **impedir** o uso de IA — isso não
funciona e todo mundo sabe. O que estas atividades fazem é outra coisa:
**tornar o uso dela pouco útil para a nota**.

Uma LLM resolve os exercícios de código de qualquer notebook introdutório em
segundos. Por isso o código vale no máximo 4,0 de 10,0. Os outros 6,0 estão em
artefatos que ela não consegue produzir no seu lugar: dados que só existem
para a sua matrícula, o registro do seu próprio processo, o obstáculo que
_você_ enfrentou, a questão que _você_ inventou.

Quem terceirizar o código para a IA e **declarar isso honestamente** ainda
tira nota — só não tira nota alta. E o professor conversa com essa pessoa,
porque é o que faz sentido fazer.

**Os limites também são ditos abertamente:** o diário de bordo é falsificável
por quem se der o trabalho, e nenhum sinal levantado automaticamente vira
penalidade. Esses sinais servem para o professor **saber com quem conversar** —
nada além disso. As âncoras reais de verificação continuam sendo presenciais:
os **Checkpoints** (30%) e a **defesa oral** do projeto final.

A declaração honesta de uso, mesmo contrariando a política da unidade, é
tratada como questão pedagógica — a ser conversada. A declaração falsa é outra
coisa, e cai no regimento da UFPB.

---

## 🆘 Problemas comuns

**"Matrícula não parece válida"** — o `"..."` do template continua lá. Use a
sua matrícula completa do SIGAA, só dígitos, entre aspas.

**`ModuleNotFoundError: No module named 'scripts'`** — o notebook está sendo
rodado de outro diretório. Abra-o a partir da raiz do seu repositório (onde
ficam o notebook e a pasta `scripts/`).

**`unsupported format string passed to ellipsis.__format__`** — algum `...` de
`# TODO` ainda não foi preenchido, e um `print()` mais abaixo tentou formatá-lo.
Procure o `...` que sobrou na célula.

**"Apaguei meu diário sem querer"** — `limpar_diario()` recomeça do zero. Não é
o fim do mundo: conte o que aconteceu no campo do obstáculo, com as suas
palavras. Honestidade nunca custou ponto aqui.

**Travei de verdade** — use o fórum da turma no Google Sala de Aula, ou traga
para a aula. Pedir ajuda de forma bem descrita é uma habilidade avaliada, não
um demérito.
