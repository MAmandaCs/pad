"""Kit do Relatório 02 — A Mesa de Operações da Fortuna Capital.

Cenário: você é analista júnior na **Fortuna Capital**, uma corretora
fictícia que opera ações na B3, crédito corporativo, roteamento de ordens,
câmbio, fundos de investimento, IPOs e tributação de serviços. Cada uma
dessas oito frentes te dá um caso pessoal, derivado da sua matrícula.

O notebook do aluno usa seis funções, e é só isso::

    iniciar(matricula, nome)      liga o kit e cria os seus dados
    prever(**respostas)           carimba a sua previsão antes de revelar
    registrar(etapa, nota)        marca uma etapa no diário de bordo
    conferir(etapa, **respostas)  devolve um retorno sobre o que você resolveu
    diario()                      mostra o seu ritmo de trabalho
    assinatura()                  emite a linha de entrega

Nada aqui usa rede, arquivo externo ou biblioteca de terceiros.

**Nível de estruturas: 1** — ainda só escalares, como no Relatório 01. O que
muda são as ferramentas de decisão: `match`/`case`, condicionais aninhadas e
`try`/`except`/`raise` sobre os mesmos tipos primitivos. Continua sem listas,
laços nem funções.

⚠️ **Sobre `input()`:** as Missões usam `input()` porque alguém está sentado
no teclado. Um notebook de **entrega** roda inteiro, sem parar para digitar —
por isso quem faz o papel do teclado aqui é o kit: cada exercício recebe os
seus dados já prontos, em variáveis com o seu nome. Alguns chegam como
**texto** de propósito (`MEU_PRECO_TEXTO`, `MEU_VALOR_LANCAMENTO`, ...) —
é assim que um dado chega de um provedor externo, e a conversão continua
sendo parte do exercício.

Este arquivo é legível de propósito: se você quiser entender de onde saíram
os seus números, leia o código. A mecânica compartilhada (semente, diário,
assinatura) mora em ``core.py``.
"""

from . import core
from .core import checar_bool, checar_igual, checar_numero

ATIVIDADE = "r02"
VERSAO = "1.0"

# ---------------------------------------------------------------- o painel
# (ticker, preço-base em R$, volume-base em milhares de ações)
#
# ⚠️ Valores APROXIMADOS e didáticos, só para dar plausibilidade de mercado —
# não são cotações reais nem devem ser citados como tais.
#
# 43 linhas — número primo maior que a turma máxima prevista (40) — garante
# que cada aluno receba um ticker-foco diferente, mesmo que as matrículas da
# turma avancem em sequência.
_PAINEL_TICKERS = [
    ("PETR4", 34.50, 12850.0), ("VALE3", 61.20, 9800.0),
    ("ITUB4", 28.90, 15200.0), ("BBDC4", 13.75, 11400.0),
    ("ABEV3", 11.40, 8600.0), ("WEGE3", 38.60, 4200.0),
    ("MGLU3", 2.85, 22000.0), ("B3SA3", 10.95, 9100.0),
    ("RENT3", 47.80, 3100.0), ("SUZB3", 52.30, 2800.0),
    ("LREN3", 15.60, 5400.0), ("RADL3", 24.10, 3300.0),
    ("EQTL3", 32.40, 2600.0), ("GGBR4", 18.75, 6700.0),
    ("JBSS3", 27.90, 4800.0), ("BRFS3", 19.85, 3900.0),
    ("CSNA3", 14.20, 8200.0), ("VIVT3", 41.30, 1900.0),
    ("ELET3", 39.60, 5100.0), ("PRIO3", 44.90, 4400.0),
    ("HAPV3", 3.75, 14300.0), ("RAIL3", 20.40, 6100.0),
    ("EMBR3", 33.80, 3700.0), ("CCRO3", 11.65, 7200.0),
    ("CPLE6", 9.30, 5600.0), ("SANB11", 26.50, 2400.0),
    ("TOTS3", 29.70, 1800.0), ("UGPA3", 21.85, 3500.0),
    ("CYRE3", 17.40, 2900.0), ("MRVE3", 8.95, 6800.0),
    ("BEEF3", 6.20, 5300.0), ("YDUQ3", 16.30, 2100.0),
    ("COGN3", 2.40, 19500.0), ("ALPA4", 7.85, 3600.0),
    ("ASAI3", 9.60, 8900.0), ("CIEL3", 4.35, 11200.0),
    ("ENEV3", 13.90, 4900.0), ("GOAU4", 10.10, 5700.0),
    ("KLBN11", 22.60, 2000.0), ("MULT3", 25.80, 1700.0),
    ("NTCO3", 14.75, 3200.0), ("SLCE3", 19.20, 1500.0),
    ("TIMS3", 16.90, 2700.0),
]

_EMPRESAS_CREDITO = [
    "Construtora Alvorada", "Agropecuária Vale Verde", "Metalúrgica Sul",
    "TransLog Rodoviária", "Grupo Cerrado Alimentos", "Têxtil Nordeste",
    "Papel & Celulose Aurora", "Distribuidora Rio Claro", "Química Bahia",
    "Frigorífico Pantanal", "Cimenteira Serra Azul", "Varejo Popular Ltda",
    "Energia Solar do Sertão", "Mineradora Itacolomi", "Autopeças Vitória",
]

_FUNDOS = [
    "Fortuna Tesouro Plus", "Fortuna Ações Brasil", "Fortuna Multi Alfa",
    "Fortuna Renda Fixa DI", "Fortuna Small Caps", "Fortuna Global Macro",
    "Fortuna Dividendos", "Fortuna Crédito Privado", "Fortuna Long Bias",
    "Fortuna Previdência",
]

_EMPRESAS_IPO = [
    "TechBR Sistemas", "AgroDigital S.A.", "MedCare Diagnósticos",
    "LogiFast Transportes", "GreenPower Energia", "FinFlow Pagamentos",
    "BioSaúde Farmacêutica", "UrbanMob Mobilidade", "DataCloud Serviços",
    "NutriFoods Alimentos",
]

_PRESTADORES = [
    "Consultoria Horizonte", "TechSolve Sistemas", "Auditoria Confiança",
    "Assessoria Prisma", "DataWise Consultoria", "InovaTech Serviços",
    "Compliance Total", "Analytics Prime",
]

_CANAIS = {
    # canal: (taxa de corretagem, limite por ordem em R$)
    "homebroker": (0.0003, 1_000_000.0),
    "assessor": (0.0010, 5_000_000.0),
    "algoritmo": (0.0001, 10_000_000.0),
    "mesa": (0.0015, float("inf")),
}

_COTACOES = {"USD": 5.15, "EUR": 5.62, "GBP": 6.48}

#: Faixas de IOF sobre operação de câmbio, por valor BRUTO em R$.
FAIXAS_IOF = [(50_000.0, 0.0038), (500_000.0, 0.0110), (float("inf"), 0.0188)]

#: Alíquota-base de ISS por tipo de serviço.
ALIQUOTAS_ISS = {"consultoria": 0.05, "tecnologia": 0.03, "auditoria": 0.04}

#: Corte de volume financeiro (em mil R$) para "alta liquidez".
CORTE_ALTA_LIQUIDEZ = 200_000.0

#: Piso do IPO, em R$ milhões de receita anual.
CORTE_RECEITA_IPO = 500.0


# ------------------------------------------------------------ geração
def _gerar(matricula, ger):
    """Deriva os dados personalizados do aluno a partir da matrícula.

    A **ordem dos sorteios** é parte do contrato: mudá-la muda os dados de
    toda a turma e invalida as assinaturas já emitidas. Se precisar alterar,
    suba ``VERSAO``.
    """
    ticker, preco_base, volume_base = _PAINEL_TICKERS[
        core.indice_sem_colisao(matricula, len(_PAINEL_TICKERS))
    ]
    preco = round(core.perturbar(preco_base, ger, 0.15, minimo=1.0), 2)
    volume = round(core.perturbar(volume_base, ger, 0.20, minimo=100.0))

    ilc = round(ger.uniform(0.5, 2.5), 2)
    margem_ebitda = round(ger.uniform(-3.0, 30.0), 1)
    alavancagem = round(ger.uniform(0.5, 9.0), 1)

    canal = ger.choice(list(_CANAIS.keys()))
    valor_ordem = round(ger.uniform(50_000.0, 12_000_000.0), 2)

    valor_lancamento = round(ger.uniform(1_000.0, 900_000.0), 2)
    quantidade_lancamento = ger.randrange(10, 20_000)
    codigo_lancamento = ger.choice(["C", "V"])

    moeda = ger.choice(list(_COTACOES.keys()))
    valor_me = round(ger.uniform(1_000.0, 500_000.0), 2)
    spread_pct = round(ger.uniform(0.2, 4.8), 2)

    classe_fundo = ger.choice(["rf", "rv", "multi"])
    dados_fundo = {}
    if classe_fundo == "rf":
        dados_fundo["MEU_PRAZO_FUNDO"] = ger.randrange(10, 730)
    elif classe_fundo == "rv":
        dados_fundo["MINHA_CONCENTRACAO_FUNDO"] = round(ger.uniform(5.0, 80.0), 1)
    else:
        dados_fundo["MEU_FUNDO_ALAVANCADO"] = ger.random() < 0.5

    receita_ipo = round(ger.uniform(100.0, 1500.0), 1)
    margem_liquida = round(ger.uniform(-10.0, 30.0), 1)
    divida_ebitda_ipo = round(ger.uniform(0.5, 9.0), 1)

    tipo_servico = ger.choice(list(ALIQUOTAS_ISS.keys()))
    valor_nota = round(ger.uniform(2_000.0, 60_000.0), 2)
    regime = ger.choice(["simples", "presumido"])

    dados = {
        # Exercício 1 — painel de cotações (chega como TEXTO de propósito)
        "MEU_TICKER": ticker,
        "MEU_PRECO_TEXTO": f"{preco:.2f}",
        "MEU_VOLUME_TEXTO": str(volume),
        # Exercício 2 — risco de crédito
        "MINHA_EMPRESA_CREDITO": ger.choice(_EMPRESAS_CREDITO),
        "MEU_ILC": ilc,
        "MINHA_MARGEM_EBITDA": margem_ebitda,
        "MINHA_ALAVANCAGEM": alavancagem,
        # Exercício 3 — roteador de ordens
        "MEU_CANAL": canal,
        "MEU_VALOR_ORDEM": valor_ordem,
        # Exercício 4 — validador de lançamentos (tudo como TEXTO)
        "MEU_VALOR_LANCAMENTO": f"{valor_lancamento:.2f}",
        "MINHA_QUANTIDADE_LANCAMENTO": str(quantidade_lancamento),
        "MEU_CODIGO_LANCAMENTO": codigo_lancamento,
        # Exercício 5 — câmbio
        "MINHA_MOEDA": moeda,
        "MEU_VALOR_ME": valor_me,
        "MEU_SPREAD_PCT": spread_pct,
        # Exercício 6 — enquadramento de fundos
        "MEU_FUNDO": ger.choice(_FUNDOS),
        "MINHA_CLASSE_FUNDO": classe_fundo,
        # Exercício 7 — triagem de IPO
        "MINHA_EMPRESA_IPO": ger.choice(_EMPRESAS_IPO),
        "MINHA_RECEITA_IPO": receita_ipo,
        "MINHA_MARGEM_LIQUIDA": margem_liquida,
        "MINHA_DIVIDA_EBITDA_IPO": divida_ebitda_ipo,
        "MEU_CONSELHO_INDEPENDENTE": ger.random() < 0.5,
        "MINHA_AUDITORIA_BIG_FOUR": ger.random() < 0.5,
        "MEU_TAG_ALONG": ger.random() < 0.5,
        # Exercício 8 — auditoria fiscal de notas
        "MEU_PRESTADOR": ger.choice(_PRESTADORES),
        "MEU_TIPO_SERVICO": tipo_servico,
        "MEU_VALOR_NOTA": valor_nota,
        "MEU_REGIME": regime,
    }
    dados.update(dados_fundo)
    return dados


def _apresentar(d):
    """Imprime o briefing do analista no Passo 0."""
    print(f"📈  Painel de cotações")
    print(f"    MEU_TICKER .............. {d['MEU_TICKER']}")
    print(f"    MEU_PRECO_TEXTO ......... {d['MEU_PRECO_TEXTO']!r}  <- TEXTO")
    print(f"    MEU_VOLUME_TEXTO ........ {d['MEU_VOLUME_TEXTO']!r}  <- TEXTO")
    print()
    print(f"🏦  Crédito corporativo — {d['MINHA_EMPRESA_CREDITO']}")
    print(f"    MEU_ILC ................. {d['MEU_ILC']}")
    print(f"    MINHA_MARGEM_EBITDA ..... {d['MINHA_MARGEM_EBITDA']}%")
    print(f"    MINHA_ALAVANCAGEM ....... {d['MINHA_ALAVANCAGEM']}")
    print()
    print(f"📮  Roteador de ordens")
    print(f"    MEU_CANAL ............... {d['MEU_CANAL']}")
    print(f"    MEU_VALOR_ORDEM ......... R$ {d['MEU_VALOR_ORDEM']:.2f}")
    print()
    print(f"🧾  Lançamento do back-office (tudo TEXTO)")
    print(f"    MEU_VALOR_LANCAMENTO .... {d['MEU_VALOR_LANCAMENTO']!r}")
    print(f"    MINHA_QUANTIDADE_LANCAMENTO {d['MINHA_QUANTIDADE_LANCAMENTO']!r}")
    print(f"    MEU_CODIGO_LANCAMENTO ... {d['MEU_CODIGO_LANCAMENTO']!r}")
    print()
    print(f"💱  Câmbio")
    print(f"    MINHA_MOEDA ............. {d['MINHA_MOEDA']}")
    print(f"    MEU_VALOR_ME ............ {d['MEU_VALOR_ME']:.2f}")
    print(f"    MEU_SPREAD_PCT .......... {d['MEU_SPREAD_PCT']}%")
    print()
    print(f"💰  Fundo de investimento — {d['MEU_FUNDO']}")
    print(f"    MINHA_CLASSE_FUNDO ...... {d['MINHA_CLASSE_FUNDO']}")
    if "MEU_PRAZO_FUNDO" in d:
        print(f"    MEU_PRAZO_FUNDO ......... {d['MEU_PRAZO_FUNDO']} dias")
    if "MINHA_CONCENTRACAO_FUNDO" in d:
        print(f"    MINHA_CONCENTRACAO_FUNDO  {d['MINHA_CONCENTRACAO_FUNDO']}%")
    if "MEU_FUNDO_ALAVANCADO" in d:
        print(f"    MEU_FUNDO_ALAVANCADO .... {d['MEU_FUNDO_ALAVANCADO']}")
    print()
    print(f"🏛️  IPO — {d['MINHA_EMPRESA_IPO']}")
    print(f"    MINHA_RECEITA_IPO ....... R$ {d['MINHA_RECEITA_IPO']}M")
    print(f"    MINHA_MARGEM_LIQUIDA .... {d['MINHA_MARGEM_LIQUIDA']}%")
    print(f"    MINHA_DIVIDA_EBITDA_IPO . {d['MINHA_DIVIDA_EBITDA_IPO']}")
    print(f"    MEU_CONSELHO_INDEPENDENTE {d['MEU_CONSELHO_INDEPENDENTE']}")
    print(f"    MINHA_AUDITORIA_BIG_FOUR  {d['MINHA_AUDITORIA_BIG_FOUR']}")
    print(f"    MEU_TAG_ALONG ........... {d['MEU_TAG_ALONG']}")
    print()
    print(f"🧮  Nota fiscal — {d['MEU_PRESTADOR']}")
    print(f"    MEU_TIPO_SERVICO ........ {d['MEU_TIPO_SERVICO']}")
    print(f"    MEU_VALOR_NOTA .......... R$ {d['MEU_VALOR_NOTA']:.2f}")
    print(f"    MEU_REGIME .............. {d['MEU_REGIME']}")


# ------------------------------------------------------------ as réguas
# Estas funções são a "resposta" do professor. Existem separadas das
# checagens para que a regra fique escrita uma vez só.
def grau_risco(ilc, margem_ebitda, alavancagem):
    if ilc >= 1.5 and margem_ebitda >= 15 and alavancagem <= 3.0:
        return "AAA"
    if ilc >= 1.0 and margem_ebitda >= 10 and alavancagem <= 5.0:
        return "BBB"
    if ilc < 1.0 or margem_ebitda < 5:
        return "CCC"
    return "BB"


def decisao_credito(grau):
    if grau in ("AAA", "BBB"):
        return "✅ Crédito APROVADO"
    if grau == "BB":
        return "⚠️ Crédito com GARANTIA ADICIONAL"
    return "❌ Crédito NEGADO"


def subclasse_fundo(classe, d):
    if classe == "rf":
        prazo = d["MEU_PRAZO_FUNDO"]
        if prazo <= 60:
            return "Curto Prazo"
        if prazo <= 365:
            return "Referenciado"
        return "Longo Prazo"
    if classe == "rv":
        return "Diversificado" if d["MINHA_CONCENTRACAO_FUNDO"] <= 30 else "Concentrado"
    return "Dinâmico" if d["MEU_FUNDO_ALAVANCADO"] else "Balanceado"


def aliquota_iof(valor_bruto):
    for teto, aliquota in FAIXAS_IOF:
        if valor_bruto <= teto:
            return aliquota
    raise AssertionError("faixa não encontrada")  # pragma: no cover


def aliquota_final_iss(tipo_servico, regime, valor_nota):
    base = ALIQUOTAS_ISS[tipo_servico]
    if regime == "simples":
        return 0.02 if valor_nota <= 10_000 else base * 0.7
    return base


# ------------------------------------------------------------ checagens
def _checagens(etapa, r, d):
    """Monta a lista de checagens de uma etapa: ``[(ok, mensagem), ...]``."""

    if etapa == "exercicio-1":
        preco = float(d["MEU_PRECO_TEXTO"])
        volume = int(d["MEU_VOLUME_TEXTO"])
        financeiro = preco * volume
        return [
            checar_numero(
                "preco", r.get("preco"), preco,
                "converta MEU_PRECO_TEXTO para float.",
            ),
            checar_numero(
                "volume", r.get("volume"), volume,
                "converta MEU_VOLUME_TEXTO para int.", tolerancia=0,
            ),
            checar_numero(
                "volume_financeiro", r.get("volume_financeiro"), financeiro,
                "preço × volume — ambos já na mesma base (mil R$).",
            ),
            checar_bool(
                "alta_liquidez", r.get("alta_liquidez"),
                financeiro > CORTE_ALTA_LIQUIDEZ,
                f"o corte é {CORTE_ALTA_LIQUIDEZ:.0f} mil R$ — use comparação, sem if.",
            ),
        ]

    if etapa == "exercicio-2":
        grau = grau_risco(d["MEU_ILC"], d["MINHA_MARGEM_EBITDA"], d["MINHA_ALAVANCAGEM"])
        return [
            checar_igual(
                "grau", r.get("grau"), grau,
                f"ILC {d['MEU_ILC']}, ME {d['MINHA_MARGEM_EBITDA']}%, "
                f"ALAV {d['MINHA_ALAVANCAGEM']} — confira a ORDEM da cadeia "
                "e se usou `and`/`or` como o enunciado pede.",
            ),
            checar_igual(
                "decisao", r.get("decisao"), decisao_credito(grau),
                f"o grau {grau} leva a qual decisão?",
            ),
        ]

    if etapa == "exercicio-3":
        taxa, limite = _CANAIS[d["MEU_CANAL"]]
        aceita = d["MEU_VALOR_ORDEM"] <= limite
        corretagem = d["MEU_VALOR_ORDEM"] * taxa if aceita else 0.0
        return [
            checar_numero(
                "taxa", r.get("taxa"), taxa,
                f"canal {d['MEU_CANAL']!r} — confira a tabela.", tolerancia=1e-9,
            ),
            checar_bool(
                "aceita", r.get("aceita"), aceita,
                f"o valor da ordem é R$ {d['MEU_VALOR_ORDEM']:.2f} — compare "
                "com o limite do canal.",
            ),
            checar_numero(
                "corretagem", r.get("corretagem"), corretagem,
                "valor da ordem × taxa, só quando a ordem é aceita — "
                "senão a corretagem é 0.",
            ),
        ]

    if etapa == "exercicio-4":
        valor = float(d["MEU_VALOR_LANCAMENTO"])
        quantidade = int(d["MINHA_QUANTIDADE_LANCAMENTO"])
        codigo = d["MEU_CODIGO_LANCAMENTO"]
        preco_medio = valor / quantidade
        tipo_operacao = "COMPRA" if codigo == "C" else "VENDA"
        return [
            checar_numero(
                "preco_medio", r.get("preco_medio"), preco_medio,
                "valor da operação ÷ quantidade de ações.",
            ),
            checar_igual(
                "tipo_operacao", r.get("tipo_operacao"), tipo_operacao,
                f"MEU_CODIGO_LANCAMENTO é {codigo!r} — C é compra, V é venda.",
            ),
        ]

    if etapa == "exercicio-5":
        cotacao = _COTACOES[d["MINHA_MOEDA"]]
        valor_bruto = d["MEU_VALOR_ME"] * cotacao
        spread_valor = valor_bruto * (d["MEU_SPREAD_PCT"] / 100)
        valor_liquido = valor_bruto - spread_valor
        aliquota = aliquota_iof(valor_bruto)
        iof = valor_liquido * aliquota
        valor_final = valor_liquido - iof
        lucrativa = valor_final > 0.95 * valor_bruto
        return [
            checar_numero(
                "valor_bruto", r.get("valor_bruto"), valor_bruto,
                "valor em moeda estrangeira × cotação do dia.",
            ),
            checar_numero(
                "valor_liquido", r.get("valor_liquido"), valor_liquido,
                "valor bruto − spread (spread = valor bruto × spread% / 100).",
            ),
            checar_numero(
                "iof", r.get("iof"), iof,
                "a faixa de IOF é escolhida pelo VALOR BRUTO, mas o imposto "
                "incide sobre o valor LÍQUIDO.",
            ),
            checar_bool(
                "lucrativa", r.get("lucrativa"), lucrativa,
                "compare o valor final com 95% do valor bruto.",
            ),
        ]

    if etapa == "exercicio-6":
        classe = d["MINHA_CLASSE_FUNDO"]
        classe_nome = {"rf": "Renda Fixa", "rv": "Renda Variável", "multi": "Multimercado"}[classe]
        return [
            checar_igual(
                "classe_nome", r.get("classe_nome"), classe_nome,
                f"MINHA_CLASSE_FUNDO é {classe!r}.",
            ),
            checar_igual(
                "subclasse", r.get("subclasse"), subclasse_fundo(classe, d),
                "releia os limiares da subclasse dessa classe no enunciado.",
            ),
        ]

    if etapa == "exercicio-7":
        praticas = (
            int(d["MEU_CONSELHO_INDEPENDENTE"])
            + int(d["MINHA_AUDITORIA_BIG_FOUR"])
            + int(d["MEU_TAG_ALONG"])
        )
        porte_ok = d["MINHA_RECEITA_IPO"] >= CORTE_RECEITA_IPO
        saude_ok = d["MINHA_MARGEM_LIQUIDA"] > 0 and d["MINHA_DIVIDA_EBITDA_IPO"] <= 4
        if porte_ok and saude_ok and praticas >= 2:
            decisao = "✅ PARTICIPAR do IPO"
        else:
            decisao = "❌ RECUSAR"
        return [
            checar_numero(
                "praticas_gov", r.get("praticas_gov"), praticas,
                "some os três bools de governança com int(...).", tolerancia=0,
            ),
            checar_igual(
                "decisao", r.get("decisao"), decisao,
                f"porte OK? {porte_ok} · saúde OK? {saude_ok} · "
                f"governança {praticas}/3 — os três filtros são aninhados.",
            ),
        ]

    if etapa == "exercicio-8":
        aliquota = aliquota_final_iss(d["MEU_TIPO_SERVICO"], d["MEU_REGIME"], d["MEU_VALOR_NOTA"])
        iss = d["MEU_VALOR_NOTA"] * aliquota
        liquido = d["MEU_VALOR_NOTA"] - iss
        return [
            checar_numero(
                "aliquota_final", r.get("aliquota_final"), aliquota,
                f"tipo {d['MEU_TIPO_SERVICO']!r}, regime {d['MEU_REGIME']!r}, "
                f"nota R$ {d['MEU_VALOR_NOTA']:.2f} — confira o desconto do "
                "Simples e o corte de R$ 10.000.", tolerancia=1e-9,
            ),
            checar_numero(
                "iss", r.get("iss"), iss,
                "valor da nota × alíquota final.",
            ),
            checar_numero(
                "valor_liquido", r.get("valor_liquido"), liquido,
                "valor da nota − ISS.",
            ),
        ]

    return [(False, f"❓ etapa desconhecida: {etapa!r}")]


# ---------------------------------------------------------------- montagem
_KIT = core.Kit(
    atividade=ATIVIDADE,
    titulo="Relatório 02 — A Mesa de Operações da Fortuna Capital",
    versao=VERSAO,
    gerar_dados=_gerar,
    apresentar=_apresentar,
    checagens=_checagens,
)

iniciar = _KIT.iniciar
prever = _KIT.prever
registrar = _KIT.registrar
conferir = _KIT.conferir
diario = _KIT.diario
limpar_diario = _KIT.limpar_diario
assinatura = _KIT.assinatura
dados_de = _KIT.dados_de


def distribuicao(matriculas):
    """Mostra o caso de cada matrícula da turma. Ferramenta **do professor**::

        from scripts.kit_r02 import distribuicao
        distribuicao(["20261234500", "20261234501"])

    ⚠️ Nunca versione a lista de matrículas: é dado pessoal do aluno e este
    repositório é público.
    """
    return _KIT.distribuicao(
        matriculas,
        colunas=[
            ("ticker", "MEU_TICKER", "<8"),
            ("canal", "MEU_CANAL", "<12"),
            ("moeda", "MINHA_MOEDA", "<6"),
            ("classe fundo", "MINHA_CLASSE_FUNDO", "<6"),
            ("serviço", "MEU_TIPO_SERVICO", "<12"),
            ("regime", "MEU_REGIME", "<10"),
        ],
    )
