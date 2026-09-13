"""Kit do Relatório 01 — A Régua do Observatório.

Cenário: você é analista do **Observatório Econômico Municipal (OEM)** e
recebeu **um** município para acompanhar. Todas as réguas do relatório — a do
desenvolvimento humano, a do tempo, a do poder de compra, a da meta, a
fiscal — são aplicadas a ele.

O notebook do aluno usa seis funções, e é só isso::

    iniciar(matricula, nome)      liga o kit e cria os seus dados
    prever(**respostas)           carimba a sua previsão antes de revelar
    registrar(etapa, nota)        marca uma etapa no diário de bordo
    conferir(etapa, **respostas)  devolve um retorno sobre o que você resolveu
    diario()                      mostra o seu ritmo de trabalho
    assinatura()                  emite a linha de entrega

Nada aqui usa rede, arquivo externo ou biblioteca de terceiros.

**Nível de estruturas: 1** — só escalares (números e textos soltos). O
Relatório 01 cobre as Aulas 1–2, então o aluno ainda não tem listas, laços
nem funções, e o kit não pode entregar nenhuma dessas coisas.

Este arquivo é legível de propósito: se você quiser entender de onde saíram os
seus números, leia o código. A mecânica compartilhada (semente, diário,
assinatura) mora em ``core.py``.
"""

from . import core
from .core import (
    checar_bool,
    checar_igual,
    checar_numero,
    checar_texto_contem,
)

ATIVIDADE = "r01"
VERSAO = "2.0"

# ---------------------------------------------------------------- o painel
# (nome, uf, população em mil hab., PIB per capita em R$, IDH, pobreza %)
#
# ⚠️ Os valores são APROXIMAÇÕES DIDÁTICAS, arredondadas para tornar as contas
# legíveis em sala. Não são estatísticas oficiais e não devem ser citados como
# tais. Para dados reais, consulte IBGE (SIDRA), Atlas Brasil e o Tesouro
# Nacional. As seis primeiras linhas reproduzem, sem alteração, os valores
# usados nas Missões de sala, para manter a continuidade da narrativa.
#
# O painel tem **43 linhas** — um número primo maior que a turma máxima
# prevista (40). Isso garante que cada aluno receba um município diferente,
# mesmo que as matrículas da turma avancem de 2 em 2 ou de 3 em 3.
#
# A composição é deliberada e cobre os casos que os exercícios precisam
# encontrar: capitais ricas e pobres, cidades médias do interior, e três
# anomalias que valem discussão em sala — Parauapebas (mineração: PIB per
# capita altíssimo, IDH mediano), Ipojuca (porto de Suape: PIB alto, IDH
# baixo) e Bonito (município pequeno, abaixo do corte de "grande porte").
_PAINEL = [
    # as 27 capitais
    ("João Pessoa", "PB", 833.0, 27800.0, 0.760, 19.4),
    ("Recife", "PE", 1645.0, 31200.0, 0.776, 21.4),
    ("Natal", "RN", 890.0, 26800.0, 0.763, 20.1),
    ("Belém", "PA", 1500.0, 21850.0, 0.746, 24.6),
    ("São Paulo", "SP", 12300.0, 50700.0, 0.806, 5.2),
    ("Porto Alegre", "RS", 1486.0, 42950.0, 0.804, 6.8),
    ("Rio Branco", "AC", 364.0, 22000.0, 0.727, 30.2),
    ("Maceió", "AL", 957.0, 22500.0, 0.721, 31.8),
    ("Macapá", "AP", 442.0, 19000.0, 0.733, 33.5),
    ("Manaus", "AM", 2063.0, 34000.0, 0.737, 27.9),
    ("Salvador", "BA", 2418.0, 24000.0, 0.759, 26.4),
    ("Fortaleza", "CE", 2428.0, 26500.0, 0.754, 27.1),
    ("Brasília", "DF", 2817.0, 90000.0, 0.824, 10.3),
    ("Vitória", "ES", 322.0, 88000.0, 0.845, 9.1),
    ("Goiânia", "GO", 1437.0, 39000.0, 0.799, 12.4),
    ("São Luís", "MA", 1037.0, 27000.0, 0.768, 29.7),
    ("Cuiabá", "MT", 650.0, 42000.0, 0.785, 14.2),
    ("Campo Grande", "MS", 897.0, 37000.0, 0.784, 13.1),
    ("Belo Horizonte", "MG", 2315.0, 39000.0, 0.810, 11.8),
    ("Curitiba", "PR", 1773.0, 47000.0, 0.823, 8.4),
    ("Teresina", "PI", 866.0, 25000.0, 0.751, 28.3),
    ("Rio de Janeiro", "RJ", 6211.0, 55000.0, 0.799, 15.2),
    ("Porto Velho", "RO", 460.0, 30000.0, 0.736, 23.9),
    ("Boa Vista", "RR", 413.0, 27000.0, 0.752, 25.7),
    ("Florianópolis", "SC", 537.0, 48000.0, 0.847, 6.3),
    ("Aracaju", "SE", 602.0, 27000.0, 0.770, 24.8),
    ("Palmas", "TO", 313.0, 32000.0, 0.788, 18.1),
    # cidades médias do interior — o Nordeste que o PPGE estuda
    ("Campina Grande", "PB", 419.0, 21500.0, 0.720, 26.5),
    ("Caruaru", "PE", 370.0, 18500.0, 0.677, 32.0),
    ("Juazeiro do Norte", "CE", 280.0, 17800.0, 0.694, 30.5),
    ("Feira de Santana", "BA", 620.0, 20500.0, 0.712, 27.8),
    ("Petrolina", "PE", 390.0, 22800.0, 0.697, 29.4),
    ("Imperatriz", "MA", 260.0, 21000.0, 0.731, 26.9),
    ("Marabá", "PA", 285.0, 28500.0, 0.668, 33.1),
    # polos industriais e agroindustriais do Centro-Sul
    ("Uberlândia", "MG", 715.0, 45000.0, 0.789, 9.8),
    ("Ribeirão Preto", "SP", 720.0, 52000.0, 0.800, 7.5),
    ("Campinas", "SP", 1225.0, 48500.0, 0.805, 8.2),
    ("Joinville", "SC", 620.0, 51000.0, 0.809, 5.9),
    ("Caxias do Sul", "RS", 525.0, 46000.0, 0.782, 6.4),
    # as anomalias — PIB per capita alto não é sinônimo de desenvolvimento
    ("Parauapebas", "PA", 270.0, 132000.0, 0.715, 22.5),
    ("Ipojuca", "PE", 100.0, 88000.0, 0.619, 34.0),
    ("Sorriso", "MT", 105.0, 96000.0, 0.744, 11.3),
    ("Bonito", "MS", 24.0, 32000.0, 0.750, 18.0),
]

_ANOS_FOCO = [2019, 2020, 2021, 2022, 2023]
_JANELAS = [4, 5, 6]  # tamanho da série histórica do PIB per capita

#: Régua do PNUD para desenvolvimento humano.
FAIXAS_IDH = [(0.800, "muito alto"), (0.700, "alto"), (0.550, "médio")]

#: Régua do Fundo Regional de Desenvolvimento (fictício, progressivo por
#: faixa, no mesmo desenho do IRPF visto na Missão 2): teto da faixa,
#: alíquota marginal e parcela a deduzir, em R$ por habitante.
#: As parcelas são calibradas para a função ser **contínua** nos limites —
#: é exatamente isso que impede o líquido de cair ao mudar de faixa.
FAIXAS_FUNDO = [
    (18000.0, 0.000, 0.00),
    (28000.0, 0.010, 180.00),
    (45000.0, 0.025, 600.00),
    (float("inf"), 0.045, 1500.00),
]

#: Corte do IBGE para município de grande porte, em mil habitantes.
CORTE_GRANDE_PORTE = 100.0

#: Piso de contribuição, em mil R$, para o município ser considerado
#: contribuinte relevante do fundo.
PISO_RELEVANTE = 50000.0


# ------------------------------------------------------------ geração
def _gerar(matricula, ger):
    """Deriva os dados personalizados do aluno a partir da matrícula.

    A **ordem dos sorteios** abaixo é parte do contrato: mudá-la muda os
    dados de toda a turma e invalida as assinaturas já emitidas. Se precisar
    alterar, suba ``VERSAO``.
    """
    nome, uf, populacao, pib_pc, idh, pobreza = _PAINEL[
        core.indice_sem_colisao(matricula, len(_PAINEL))
    ]

    ano = _ANOS_FOCO[ger.randrange(len(_ANOS_FOCO))]
    populacao = round(core.perturbar(populacao, ger, 0.08, minimo=1.0), 1)
    pib_pc = round(core.perturbar(pib_pc, ger, 0.10, minimo=1000.0), 2)
    idh = round(core.perturbar(idh, ger, 0.06, minimo=0.400, maximo=0.949), 3)
    pobreza = round(core.perturbar(pobreza, ger, 0.12, minimo=0.5, maximo=60.0), 1)

    # série histórica: o PIB per capita de hoje, "desandado" por um
    # crescimento observado que pode ser negativo — há município brasileiro
    # que encolheu no período, e o exercício de CAGR precisa disso.
    janela = _JANELAS[ger.randrange(len(_JANELAS))]
    observado = ger.uniform(-0.015, 0.045)
    pib_pc_base = round(pib_pc / (1 + observado) ** janela, 2)

    return {
        "MEU_MUNICIPIO": nome,
        "MINHA_UF": uf,
        "MINHA_POPULACAO": populacao,
        "MEU_IDH": idh,
        "MINHA_POBREZA": pobreza,
        "MEU_ANO": ano,
        "MEU_PIB_PC": pib_pc,
        "MEU_ANO_BASE": ano - janela,
        "MEU_PIB_PC_BASE": pib_pc_base,
        "MEU_CRESCIMENTO": round(ger.uniform(0.8, 3.2), 2),
        "MINHA_META": round(pib_pc * ger.uniform(1.05, 1.45), -2),
        "MINHA_TAXA_NOMINAL": round(ger.uniform(6.0, 14.0), 2),
        "MINHA_INFLACAO": round(ger.uniform(3.0, 11.0), 2),
        "MINHAS_PARCELAS": ger.randrange(130, 281),
        "MINHA_PARCELA": round(ger.uniform(80.0, 950.0), 2),
        # chega como TEXTO de propósito: é assim que o dado sai do portal
        "MINHA_DIVIDA": f"{ger.uniform(18.0, 92.0):.1f}",
    }


def _apresentar(d):
    """Imprime o briefing do analista no Passo 0."""
    print(f"🏙️  Município foco: {d['MEU_MUNICIPIO']} ({d['MINHA_UF']})")
    print(f"    MINHA_POPULACAO ..... {d['MINHA_POPULACAO']} mil hab.")
    print(f"    MEU_IDH ............. {d['MEU_IDH']}")
    print(f"    MINHA_POBREZA ....... {d['MINHA_POBREZA']}%")
    print()
    print("📈  Série do PIB per capita")
    print(f"    MEU_ANO_BASE ........ {d['MEU_ANO_BASE']}")
    print(f"    MEU_PIB_PC_BASE ..... R$ {d['MEU_PIB_PC_BASE']:.2f}")
    print(f"    MEU_ANO ............. {d['MEU_ANO']}")
    print(f"    MEU_PIB_PC .......... R$ {d['MEU_PIB_PC']:.2f}")
    print()
    print("💹  Mercado e plano diretor")
    print(f"    MINHA_TAXA_NOMINAL .. {d['MINHA_TAXA_NOMINAL']}% a.a. "
          "(aplicação do superávit de caixa)")
    print(f"    MINHA_INFLACAO ...... {d['MINHA_INFLACAO']}% a.a.")
    print(f"    MEU_CRESCIMENTO ..... {d['MEU_CRESCIMENTO']}% a.a. "
          "(projeção do PIB per capita)")
    print(f"    MINHA_META .......... R$ {d['MINHA_META']:.2f} "
          "(PIB per capita em 2030)")
    print()
    print("🏛️  Financiamento e dívida")
    print(f"    MINHAS_PARCELAS ..... {d['MINHAS_PARCELAS']} parcelas mensais")
    print(f"    MINHA_PARCELA ....... R$ {d['MINHA_PARCELA']:.2f} mil por mês")
    print(f"    MINHA_DIVIDA ........ {d['MINHA_DIVIDA']!r}  "
          "<- repare no tipo: é TEXTO")


# ------------------------------------------------------------ as réguas
# Estas funções são a "resposta" do professor. Elas existem separadas das
# checagens para que a regra fique escrita uma vez só — e para que o gabarito
# e a conferência nunca divirjam.
def faixa_idh(idh):
    for piso, nome in FAIXAS_IDH:
        if idh >= piso:
            return nome
    return "baixo"


def fundo_regional(pib_pc):
    """Devolve ``(alíquota marginal, parcela a deduzir)`` do fundo."""
    for teto, aliquota, deduzir in FAIXAS_FUNDO:
        if pib_pc <= teto:
            return aliquota, deduzir
    raise AssertionError("faixa não encontrada")  # pragma: no cover


def semaforo_fisher(taxa_real_pct):
    if taxa_real_pct > 2:
        return "🟢 ganho real relevante"
    if taxa_real_pct > 0:
        return "🟡 ganho real modesto"
    return "🔴 perda de poder de compra"


def semaforo_divida(divida_pct):
    if divida_pct <= 40:
        return "🟢 risco baixo"
    if divida_pct <= 60:
        return "🟡 risco moderado"
    return "🔴 risco alto"


def parecer_meta(projetado, meta):
    if projetado >= meta:
        return "✅ meta alcançada"
    if projetado >= 0.90 * meta:
        return "⚠️ meta próxima, exige aceleração"
    return "❌ meta inalcançável no ritmo atual"


# ------------------------------------------------------------ checagens
def _checagens(etapa, r, d):
    """Monta a lista de checagens de uma etapa: ``[(ok, mensagem), ...]``.

    Todos os valores esperados são recalculados a partir de ``d`` — os mesmos
    números **já arredondados** que o aluno vê. Nunca a partir dos valores
    intermediários da geração, senão a conferência discorda do enunciado na
    terceira casa decimal.
    """
    pib_pc = d["MEU_PIB_PC"]
    pib_pc_base = d["MEU_PIB_PC_BASE"]
    pop = d["MINHA_POPULACAO"]
    idh = d["MEU_IDH"]
    meta = d["MINHA_META"]
    anos_serie = d["MEU_ANO"] - d["MEU_ANO_BASE"]
    horizonte = 2030 - d["MEU_ANO"]

    if etapa == "exercicio-1":
        return [
            checar_numero(
                "pib_total", r.get("pib_total"), pib_pc * pop,
                "PIB per capita × população — as duas variáveis do kit, sem "
                "converter unidade: o resultado sai em mil R$.",
            ),
            checar_bool(
                "eh_grande_porte", r.get("eh_grande_porte"),
                pop > CORTE_GRANDE_PORTE,
                "MINHA_POPULACAO já está em MIL habitantes — o corte de 100 "
                "mil habitantes vira qual número na comparação?",
            ),
            checar_texto_contem(
                "ficha", r.get("ficha"),
                [d["MEU_MUNICIPIO"], d["MINHA_UF"], f"{idh}"],
                "Use as variáveis dentro das chaves da f-string, não o texto "
                "digitado à mão.",
            ),
        ]

    if etapa == "exercicio-2":
        return [
            checar_igual(
                "faixa_idh", r.get("faixa_idh"), faixa_idh(idh),
                f"seu IDH é {idh}. Confira os limiares e a ORDEM da cadeia: "
                "ela testa de cima para baixo, do mais restritivo ao mais geral.",
            ),
            checar_numero(
                "falta_para_muito_alto", r.get("falta_para_muito_alto"),
                max(0.0, 0.800 - idh),
                "a distância nunca é negativa: quem já está na faixa "
                "'muito alto' precisa de 0.",
                tolerancia=1e-9,
            ),
        ]

    if etapa == "exercicio-3":
        razao = pib_pc / pib_pc_base
        cagr_pct = (razao ** (1 / anos_serie) - 1) * 100
        total_pct = (razao - 1) * 100
        return [
            checar_numero(
                "anos_da_serie", r.get("anos_da_serie"), anos_serie,
                f"de {d['MEU_ANO_BASE']} a {d['MEU_ANO']}: conte os "
                "INTERVALOS entre os anos, não os anos.",
                tolerancia=0,
            ),
            checar_numero(
                "crescimento_total_pct", r.get("crescimento_total_pct"),
                total_pct,
                "é a variação do período: (final / inicial − 1) × 100. "
                "Repare que ela pode ser negativa.",
            ),
            checar_numero(
                "cagr_pct", r.get("cagr_pct"), cagr_pct,
                "o expoente é FRACIONÁRIO: (final/inicial) ** (1/anos) − 1, "
                "tudo isso × 100. Cuidado com os parênteses do expoente.",
            ),
            checar_numero(
                "media_ingenua_pct", r.get("media_ingenua_pct"),
                total_pct / anos_serie,
                "é o crescimento total dividido pelo número de anos — a média "
                "aritmética que a gente quer justamente mostrar que é errada.",
            ),
            checar_bool(
                "projecao_otimista", r.get("projecao_otimista"),
                d["MEU_CRESCIMENTO"] > cagr_pct,
                "compare MEU_CRESCIMENTO (a projeção do plano diretor) com o "
                "CAGR que o município de fato entregou. Sem `if`: a "
                "comparação já devolve o bool.",
            ),
        ]

    if etapa == "exercicio-4":
        i = d["MINHA_TAXA_NOMINAL"] / 100
        infl = d["MINHA_INFLACAO"] / 100
        real_pct = ((1 + i) / (1 + infl) - 1) * 100
        aprox_pct = d["MINHA_TAXA_NOMINAL"] - d["MINHA_INFLACAO"]
        return [
            checar_numero(
                "taxa_real_pct", r.get("taxa_real_pct"), real_pct,
                "Fisher exata: (1 + i) / (1 + π) − 1, com i e π em FRAÇÃO "
                "(divida por 100 antes), e o resultado × 100 no fim.",
            ),
            checar_numero(
                "taxa_real_aproximada_pct", r.get("taxa_real_aproximada_pct"),
                aprox_pct,
                "a aproximação de bolso é a subtração simples das duas taxas, "
                "em percentual.",
            ),
            checar_numero(
                "erro_pp", r.get("erro_pp"), aprox_pct - real_pct,
                "quanto a aproximação superestima: aproximada − exata, em "
                "pontos percentuais. O sinal importa.",
            ),
            checar_igual(
                "sinal_fisher", r.get("sinal_fisher"), semaforo_fisher(real_pct),
                f"sua taxa real é {real_pct:.2f}% — confira os limiares do "
                "semáforo e a ordem da cadeia.",
            ),
        ]

    if etapa == "exercicio-5":
        projetado = pib_pc * (1 + d["MEU_CRESCIMENTO"] / 100) ** horizonte
        return [
            checar_numero(
                "horizonte", r.get("horizonte"), horizonte,
                f"de {d['MEU_ANO']} a 2030 são quantos períodos de "
                "crescimento? É o mesmo raciocínio do CAGR do Exercício 3.",
                tolerancia=0,
            ),
            checar_numero(
                "pib_projetado", r.get("pib_projetado"), projetado,
                "confira os parênteses: é (1 + g/100) elevado ao horizonte, "
                "tudo multiplicando o PIB per capita. Releia a Parte 1.",
            ),
            checar_numero(
                "percentual_da_meta", r.get("percentual_da_meta"),
                projetado / meta * 100,
                "é a projeção sobre a MINHA_META, vezes 100.",
            ),
            checar_igual(
                "parecer", r.get("parecer"), parecer_meta(projetado, meta),
                "compare a sua projeção com MINHA_META e com 90% dela.",
            ),
        ]

    if etapa == "exercicio-6":
        aliquota, deduzir = fundo_regional(pib_pc)
        por_habitante = pib_pc * aliquota - deduzir
        total = por_habitante * pop
        return [
            checar_numero(
                "aliquota", r.get("aliquota"), aliquota,
                f"seu PIB per capita é R$ {pib_pc:.2f} — em qual linha da "
                "tabela ele cai? Cuidado com os limites das faixas.",
                tolerancia=1e-9,
            ),
            checar_numero(
                "parcela_deduzir", r.get("parcela_deduzir"), deduzir,
                "é a segunda coluna da mesma linha da tabela: as duas andam "
                "sempre juntas, no mesmo ramo do if.",
            ),
            checar_numero(
                "contribuicao_por_habitante", r.get("contribuicao_por_habitante"),
                por_habitante,
                "PIB per capita × alíquota − parcela a deduzir. A parcela é "
                "subtraída DEPOIS da multiplicação.",
            ),
            checar_numero(
                "contribuicao_total", r.get("contribuicao_total"), total,
                "contribuição por habitante × população. Com a população em "
                "mil habitantes, o total sai em mil R$.",
            ),
            checar_numero(
                "aliquota_efetiva_pct", r.get("aliquota_efetiva_pct"),
                por_habitante / pib_pc * 100,
                "é o que o município DE FATO paga: contribuição por habitante "
                "sobre o PIB per capita, × 100. Não é a alíquota da tabela.",
            ),
            checar_bool(
                "contribuinte_relevante", r.get("contribuinte_relevante"),
                aliquota > 0.010 and total > PISO_RELEVANTE,
                "são duas condições unidas por `and`: alíquota ACIMA de 1,0% "
                f"e contribuição total acima de {PISO_RELEVANTE:.0f} mil R$.",
            ),
        ]

    if etapa == "exercicio-7":
        divida = float(d["MINHA_DIVIDA"])
        return [
            checar_numero(
                "divida_pct", r.get("divida_pct"), divida,
                "é o resultado de converter MINHA_DIVIDA de texto para número.",
            ),
            checar_igual(
                "sinal", r.get("sinal"), semaforo_divida(divida),
                f"sua dívida é {divida}% da receita — confira os limiares do "
                "semáforo e a ordem da cadeia.",
            ),
        ]

    return [(False, f"❓ etapa desconhecida: {etapa!r}")]


# ---------------------------------------------------------------- montagem
_KIT = core.Kit(
    atividade=ATIVIDADE,
    titulo="Relatório 01 — A Régua do Observatório",
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
    """Mostra o município e os indicadores de cada matrícula da turma.

    Ferramenta **do professor**, não do aluno::

        from scripts.kit_r01 import distribuicao
        distribuicao(["20261234500", "20261234501", "20261234502"])

    ⚠️ Nunca versione a lista de matrículas: é dado pessoal do aluno e este
    repositório é público.
    """
    return _KIT.distribuicao(
        matriculas,
        colunas=[
            ("município", "MEU_MUNICIPIO", "<18"),
            ("UF", "MINHA_UF", "<3"),
            ("PIB pc", "MEU_PIB_PC", ">10.2f"),
            ("IDH", "MEU_IDH", ">6.3f"),
            ("nominal", "MINHA_TAXA_NOMINAL", ">6.2f"),
            ("inflação", "MINHA_INFLACAO", ">6.2f"),
            ("dívida", "MINHA_DIVIDA", ">7"),
            ("ano", "MEU_ANO", ">5"),
        ],
    )
