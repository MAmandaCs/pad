"""Núcleo compartilhado dos kits das atividades avaliativas.

Este módulo é a **mecânica**: semente pessoal, diário de bordo, conferência,
previsão e assinatura de entrega. Ele não sabe nada sobre economia — quem
sabe é o *kit* de cada atividade (``kit_r01.py``, ``kit_r02.py``, ...).

    ┌─────────────────┐        ┌──────────────────────────────┐
    │    core.py      │  ←──   │  kit_rNN.py (um por relatório)│
    │  (mecânica)     │        │  painel + dados + checagens   │
    └─────────────────┘        └──────────────────────────────┘
                                          ↑
                               atividade-NN-<slug>.ipynb

> 👋 **Se você é aluno:** o arquivo que interessa a você é o `kit_rNN.py` da
> sua atividade — é lá que estão os dados e as regras. Aqui só tem
> encanamento. Mas leia se quiser: é Python comum, sem mágica.

Como um kit novo se conecta aqui está documentado em `AGENTS.md`, seção
"Atividades avaliativas".
"""

import copy
import hashlib
import json
import os
import random
import sys
import time

VERSAO_CORE = "2.1"

#: Tamanho máximo de turma previsto para a disciplina. Todo sorteio de
#: "caso pessoal" precisa ter pelo menos esta quantidade de resultados
#: distintos, senão dois alunos recebem o mesmo cenário.
TURMA_MAX = 40


# ============================================================ semente pessoal
def semente(matricula, tema):
    """Converte matrícula + tema num inteiro determinístico via SHA-256.

    O ``tema`` é o identificador da atividade (``"r01"``, ``"r02"``, ...).
    Entra no resumo criptográfico junto com a matrícula para que **cada
    atividade sorteie de forma independente**: quem pegou o município mais
    fácil no Relatório 01 não pega necessariamente o mais fácil no 02.
    """
    limpa = str(matricula).strip()
    if limpa in ("", "...") or not limpa.isdigit() or len(limpa) < 4:
        raise ValueError(
            f"Matrícula {limpa!r} não parece válida. "
            "Use a sua matrícula completa do SIGAA, só dígitos, entre aspas."
        )
    digest = hashlib.sha256(f"{limpa}::{tema}".encode("utf-8")).hexdigest()
    return int(digest[:16], 16)


def gerador(matricula, tema):
    """Devolve um ``random.Random`` semeado pela matrícula e pelo tema."""
    return random.Random(semente(matricula, tema))


def indice_sem_colisao(matricula, tamanho):
    """Escolhe uma linha de um painel a partir da matrícula, sem repetir.

    Usa o **resto da divisão** da matrícula pelo tamanho do painel, e não o
    sorteio pseudoaleatório. A razão é prática: matrículas de uma mesma turma
    costumam ser sequenciais, e o resto de números consecutivos também é
    consecutivo — então cada aluno cai numa linha diferente, sem repetição,
    até ``tamanho`` alunos.

    Um sorteio por hash distribuiria de forma uniforme, mas *independente*:
    numa turma de 20 alunos, vários receberiam o mesmo caso (é o problema do
    aniversário). Aqui isso não acontece.

    Por isso todo painel de kit precisa de ``len(painel) >= TURMA_MAX``, e de
    preferência um **número primo** de linhas: assim a distribuição continua
    sem colisão mesmo quando as matrículas avançam de 2 em 2, de 3 em 3 etc.
    """
    if tamanho < TURMA_MAX:
        raise ValueError(
            f"Painel com {tamanho} linhas é pequeno demais: a turma pode ter "
            f"até {TURMA_MAX} alunos e dois receberiam o mesmo caso."
        )
    return int(str(matricula).strip()) % tamanho


def perturbar(valor, ger, amplitude, minimo=None, maximo=None):
    """Desloca ``valor`` em até ±``amplitude`` (fração), respeitando limites.

    Os limites preservam plausibilidade econômica: um IDH nunca passa de 1,
    uma população nunca é negativa. Perturbação sem limite produz enunciado
    absurdo — e enunciado absurdo destrói a confiança do aluno no dado.
    """
    novo = valor * (1 + ger.uniform(-amplitude, amplitude))
    if minimo is not None:
        novo = max(novo, minimo)
    if maximo is not None:
        novo = min(novo, maximo)
    return novo


# ================================================================= checagens
_PENDENTE = "ainda não preenchido — a lacuna `...` continua ali."


def _vazio(valor):
    return valor is Ellipsis or valor is None


def checar_numero(rotulo, obtido, esperado, dica, tolerancia=0.01):
    """Compara um número com tolerância. Devolve ``(ok, mensagem)``."""
    if _vazio(obtido):
        return False, f"⏳ {rotulo}: {_PENDENTE}"
    if isinstance(obtido, bool):
        return False, (
            f"❌ {rotulo}: veio um bool ({obtido}), não um número. "
            "Comparação devolve True/False; conta devolve número."
        )
    try:
        distancia = abs(float(obtido) - float(esperado))
    except (TypeError, ValueError):
        return False, (
            f"❌ {rotulo}: esperava um número, veio "
            f"{type(obtido).__name__}. {dica}"
        )
    if distancia <= tolerancia:
        return True, f"✅ {rotulo}"
    return False, f"❌ {rotulo}: o valor não bate. {dica}"


def checar_igual(rotulo, obtido, esperado, dica):
    """Compara por igualdade exata (textos, inteiros). ``(ok, mensagem)``."""
    if _vazio(obtido):
        return False, f"⏳ {rotulo}: {_PENDENTE}"
    if obtido == esperado:
        return True, f"✅ {rotulo}"
    return False, f"❌ {rotulo}: veio {obtido!r}. {dica}"


def checar_bool(rotulo, obtido, esperado, dica):
    """Exige um ``bool`` de verdade, vindo de uma comparação."""
    if _vazio(obtido):
        return False, f"⏳ {rotulo}: {_PENDENTE}"
    if not isinstance(obtido, bool):
        return False, (
            f"❌ {rotulo}: esperava um bool (True/False) vindo de uma "
            f"comparação, veio {type(obtido).__name__}."
        )
    if obtido == esperado:
        return True, f"✅ {rotulo}"
    return False, f"❌ {rotulo}: veio {obtido}. {dica}"


def checar_texto_contem(rotulo, obtido, trechos, dica):
    """Verifica que um texto montado contém todos os ``trechos`` exigidos.

    Serve para f-strings: em vez de exigir formatação idêntica, exige que os
    dados certos apareçam. Cada item de ``trechos`` pode ser uma lista de
    alternativas aceitas (ex.: ``[["0.76", "0,76"]]``).
    """
    if _vazio(obtido):
        return False, f"⏳ {rotulo}: {_PENDENTE}"
    if not isinstance(obtido, str):
        return False, (
            f"❌ {rotulo}: deveria ser um texto (str) montado com f-string, "
            f"veio {type(obtido).__name__}."
        )
    for trecho in trechos:
        alternativas = trecho if isinstance(trecho, (list, tuple)) else [trecho]
        if not any(str(alt) in obtido for alt in alternativas):
            return False, (
                f"❌ {rotulo}: não encontrei {alternativas[0]!r} no texto. {dica}"
            )
    return True, f"✅ {rotulo}"


# ====================================================================== kit
class Kit:
    """Máquina de uma atividade: dados pessoais, diário, conferência e assinatura.

    Cada ``kit_rNN.py`` monta uma instância e reexporta os métodos como
    funções soltas, para que o notebook do aluno escreva ``iniciar(...)`` e
    não ``kit.iniciar(...)``.

    Parâmetros
    ----------
    atividade
        Identificador curto e estável: ``"r01"``. Entra na semente, no nome do
        arquivo de diário e na assinatura.
    titulo
        Título legível, usado só na impressão.
    versao
        Versão do kit. **Mude ao alterar a geração de dados ou as
        checagens** — assinaturas emitidas por versões diferentes não
        precisam bater entre si.
    gerar_dados
        ``f(matricula, ger) -> dict`` com as variáveis do aluno em MAIÚSCULAS.
    apresentar
        ``f(dados) -> None`` que imprime o briefing do aluno no Passo 0.
    checagens
        ``f(etapa, respostas, dados) -> [(ok, mensagem), ...]``.
    """

    def __init__(self, atividade, titulo, versao, gerar_dados, apresentar,
                 checagens):
        self.atividade = atividade
        self.titulo = titulo
        self.versao = versao
        self._gerar_dados = gerar_dados
        self._apresentar = apresentar
        self._checagens = checagens
        self._arquivo_diario = f"diario-{atividade}.json"
        self._dados = {}
        self._respostas = {}

    # ------------------------------------------------------------- dados
    def dados_de(self, matricula):
        """Devolve o dicionário de dados de uma matrícula, sem ligar o kit.

        Ferramenta do professor (ver ``distribuicao``) e dos testes.
        """
        return self._gerar_dados(matricula, gerador(matricula, self.atividade))

    def iniciar(self, matricula, nome, escopo=None):
        """Liga o kit: cria os seus dados e os deixa prontos para uso.

        Chame uma única vez, no Passo 0 do notebook::

            iniciar(matricula="20261234567", nome="Seu Nome Completo")

        Depois disso as variáveis do seu caso simplesmente **existem** no
        notebook, sem que você precise criá-las. Elas vêm da sua matrícula:
        trocar um dígito produz outro cenário inteiro. É por isso que o
        notebook do colega não serve para você — mesmo que o código dele
        esteja certo.

        O parâmetro ``escopo`` existe só para uso fora do notebook (testes).
        """
        dados = self.dados_de(matricula)

        # cópia PROFUNDA: a partir daqui `self._dados` (usado pelas
        # checagens) e as variáveis injetadas no notebook são objetos
        # independentes. A partir da Missão 4 (listas), o aluno vai mutar
        # listas em exercícios — sem esta cópia, mutar a lista global do
        # notebook corromperia silenciosamente o gabarito interno do kit,
        # porque ambos apontariam para a MESMA lista na memória.
        self._dados = copy.deepcopy(dados)
        self._dados["MATRICULA"] = str(matricula).strip()
        self._dados["NOME"] = str(nome).strip()
        self._respostas = {}

        if escopo is None:
            escopo = sys._getframe(1).f_globals
        escopo.update(copy.deepcopy(dados))

        print(f"📋 {self.titulo}  ·  kit {self.atividade} v{self.versao}")
        print(f"Analista: {self._dados['NOME']} ({self._dados['MATRICULA']})")
        print()
        self._apresentar(dados)
        print()
        print("✅ Kit ligado. As variáveis acima já existem — use-as direto.")

        self.registrar("passo-0", "kit ligado")
        return None

    def _exigir_inicio(self):
        if not self._dados:
            raise RuntimeError(
                "O kit ainda não foi ligado. Rode a célula do Passo 0 com "
                'iniciar(matricula="sua matrícula", nome="seu nome") antes '
                "de continuar."
            )

    # ------------------------------------------------------------ diário
    def _carregar_diario(self):
        if not os.path.exists(self._arquivo_diario):
            return []
        try:
            with open(self._arquivo_diario, "r", encoding="utf-8") as arquivo:
                return json.load(arquivo)
        except (ValueError, OSError):
            return []

    def _salvar_diario(self, registros):
        with open(self._arquivo_diario, "w", encoding="utf-8") as arquivo:
            json.dump(registros, arquivo, ensure_ascii=False, indent=1)

    def registrar(self, etapa, nota=""):
        """Marca no diário de bordo que você chegou a uma etapa do notebook.

        Escreva em ``nota`` uma frase curta sobre o que aconteceu ali — o que
        travou, o que você tentou, o que entendeu. É a **nota**, não o
        carimbo de hora, que vale ponto na rubrica.

        O diário fica em ``diario-<atividade>.json``, ao lado do notebook, e
        sobrevive a reinícios do kernel. Ele é seu, e você o lê quando quiser
        com ``diario()``.
        """
        registros = self._carregar_diario()
        registros.append(
            {"momento": time.time(), "etapa": str(etapa), "nota": str(nota)}
        )
        self._salvar_diario(registros)
        print(f"📓 registrado: {etapa}")

    def limpar_diario(self):
        """Apaga o diário e recomeça do zero.

        Use só se você reiniciou a atividade inteira. Um diário apagado perto
        do prazo é exatamente o tipo de padrão que a correção percebe.
        """
        if os.path.exists(self._arquivo_diario):
            os.remove(self._arquivo_diario)
        print(f"📓 diário de {self.atividade} apagado.")

    def diario(self):
        """Imprime o diário de bordo com os intervalos entre as etapas."""
        registros = self._carregar_diario()

        if not registros:
            print("📓 Diário vazio — nenhuma etapa registrada ainda.")
            print("   Chame registrar('etapa', 'sua nota') ao longo do notebook.")
            return None

        print(f"📓 DIÁRIO DE BORDO — {self.atividade}")
        print(f"{'#':>3}  {'hora':<9} {'desde a anterior':<18} etapa")
        print("-" * 78)

        anterior = None
        for indice, registro in enumerate(registros):
            momento = registro["momento"]
            hora = time.strftime("%H:%M:%S", time.localtime(momento))
            if anterior is None:
                intervalo = "        —         "
            else:
                intervalo = _intervalo(momento - anterior)
            print(f"{indice + 1:>3}  {hora:<9} {intervalo:<18} {registro['etapa']}")
            if registro["nota"]:
                print(f"{'':>3}  {'':<9} {'':<18} ↳ {registro['nota']}")
            anterior = momento

        duracao = registros[-1]["momento"] - registros[0]["momento"]
        print("-" * 78)
        print(f"{len(registros)} registros · janela de {_intervalo(duracao)}")
        return None

    # ---------------------------------------------------------- previsão
    def prever(self, **respostas):
        """Carimba a sua previsão **antes** de você rodar a célula que revela.

        Não diz se você acertou — não é para isso que serve. Ela grava no
        diário, com a hora, o que você achava que ia acontecer. A nota da
        Parte 1 vem da justificativa que você escreve em seguida, no texto:
        uma previsão errada, bem explicada, vale nota cheia.

        Uso::

            prever(linha_correta="B", valor_aproximado=1000.0)
        """
        self._exigir_inicio()
        registro = ", ".join(
            f"{chave}={valor!r}"
            for chave, valor in sorted(respostas.items())
            if not _vazio(valor)
        )
        if not registro:
            print("⚠️ Nenhuma previsão preenchida — as lacunas `...` continuam lá.")
            return None

        self._respostas["previsao"] = {
            "certos": 0, "total": 0, "valores": {"previsao": registro},
        }
        self.registrar("previsao", registro)
        print("🔮 Previsão carimbada. Agora sim: rode a célula seguinte.")
        return None

    # --------------------------------------------------------- conferir
    def conferir(self, etapa, **respostas):
        """Confere as suas respostas de uma etapa e explica o que não fecha.

        Não interrompe o notebook e não levanta exceção: imprime um retorno
        item a item. Quando algo não bate, você recebe uma **pista**, nunca a
        resposta. Pode rodar quantas vezes quiser — errar aqui não custa nada.
        """
        self._exigir_inicio()

        resultados = self._checagens(etapa, respostas, self._dados)
        print(f"🔎 CONFERÊNCIA — {etapa}")
        for _, mensagem in resultados:
            print(f"   {mensagem}")

        certos = sum(1 for ok, _ in resultados if ok)
        total = len(resultados)
        print("   " + "-" * 62)
        if certos == total:
            print(f"   🎉 {certos}/{total} — etapa fechada.")
        else:
            print(f"   {certos}/{total} conferidos. Ajuste o que falta e rode de novo.")

        self._respostas[etapa] = {
            "certos": certos,
            "total": total,
            "valores": {
                chave: repr(valor)
                for chave, valor in sorted(respostas.items())
                if not _vazio(valor)
            },
        }
        return None

    # -------------------------------------------------------- assinatura
    def assinatura(self):
        """Imprime a linha de assinatura da entrega e a devolve como texto.

        Ela resume, num só lugar: a sua matrícula, as respostas que passaram
        por ``conferir()`` e o seu diário. Como a matrícula entra no resumo
        criptográfico, a assinatura de um colega nunca bate com a sua — e o
        professor recalcula a esperada a partir da matrícula.

        Use a linha impressa como **mensagem do commit final**::

            git commit -m "ASSINATURA: ..."
            git push
        """
        self._exigir_inicio()

        partes = []
        certos = 0
        total = 0
        for etapa in sorted(self._respostas):
            registro = self._respostas[etapa]
            certos += registro["certos"]
            total += registro["total"]
            for chave in sorted(registro["valores"]):
                partes.append(f"{etapa}.{chave}={registro['valores'][chave]}")

        bruto = (
            f"{self._dados['MATRICULA']}::{self.atividade}::{self.versao}::"
            + "|".join(partes)
        )
        resumo = hashlib.sha256(bruto.encode("utf-8")).hexdigest()[:12]

        registros = self._carregar_diario()
        quantos = len(registros)
        duracao = (
            registros[-1]["momento"] - registros[0]["momento"]
            if quantos >= 2 else 0.0
        )

        linha = (
            f"ASSINATURA {self.atividade}: {self._dados['MATRICULA']} · "
            f"{resumo} · {certos}/{total} conferidos · {quantos} registros · "
            f"{int(duracao // 60)}min"
        )

        if total == 0:
            print("⚠️ Nenhuma conferência registrada — rode os conferir() antes.")
        print(linha)
        return linha

    # ------------------------------------------- apoio ao professor
    def distribuicao(self, matriculas, colunas):
        """Mostra que caso cada matrícula recebe. **Ferramenta do professor.**

        Rode localmente com a lista de matrículas da turma, antes de publicar
        a atividade, para conferir se a distribuição ficou variada e se algum
        caso repetiu::

            from scripts.kit_r01 import distribuicao
            distribuicao(["20261234500", "20261234501"])

        ``colunas`` é uma lista de ``(rótulo, chave, formato)``; a primeira é
        tratada como a chave de unicidade do caso.

        ⚠️ Nunca versione a lista de matrículas: é dado pessoal do aluno e o
        repositório é público.
        """
        matriculas = [str(m).strip() for m in matriculas]
        cabecalho = f"{'matrícula':<14}" + "".join(
            f"{rotulo:<{max(len(rotulo) + 2, 10)}}" for rotulo, _, _ in colunas
        )
        print(cabecalho)
        print("-" * len(cabecalho))

        chave_unica = colunas[0][1]
        vistos = {}
        for matricula in matriculas:
            dados = self.dados_de(matricula)
            vistos.setdefault(dados[chave_unica], []).append(matricula)
            linha = f"{matricula:<14}"
            for rotulo, chave, formato in colunas:
                largura = max(len(rotulo) + 2, 10)
                linha += f"{format(dados[chave], formato):<{largura}}"
            print(linha)

        print("-" * len(cabecalho))
        print(
            f"{len(matriculas)} alunos · {len(vistos)} casos distintos · "
            f"turma máxima prevista: {TURMA_MAX}"
        )

        repetidos = {c: ns for c, ns in vistos.items() if len(ns) > 1}
        if repetidos:
            print("\n⚠️ Casos repetidos (os indicadores ainda diferem entre eles):")
            for caso in sorted(repetidos, key=str):
                print(f"   {caso}: {', '.join(repetidos[caso])}")
        else:
            print("\n✅ Nenhum caso repetido nesta turma.")


def _intervalo(segundos):
    return f"{int(segundos // 60):>3}min {int(segundos % 60):02d}s"
