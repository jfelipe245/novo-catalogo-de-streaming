
import sqlite3

DB = "instance/afroedu_streaming.db"
ARQUIVO = "relatorio_banco.txt"

privados = {
    "cpf", "email", "telefone", "senha",
    "rua", "bairro", "endereco", "data_nascimento"
}

provisorios = {
    "não informado",
    "nao informado",
    "descrição pendente de revisão",
    "descricao pendente de revisao",
    "a definir",
    "pendente"
}

conexao = sqlite3.connect(DB)
cursor = conexao.cursor()

with open(ARQUIVO, "w", encoding="utf-8") as relatorio:

    tabelas = cursor.execute("""
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        AND name NOT LIKE 'sqlite_%'
    """).fetchall()

    for (tabela,) in tabelas:
        relatorio.write(f"\n{'=' * 60}\n")
        relatorio.write(f"TABELA: {tabela}\n")
        relatorio.write(f"{'=' * 60}\n")

        colunas = cursor.execute(
            f'PRAGMA table_info("{tabela}")'
        ).fetchall()

        registros = cursor.execute(
            f'SELECT * FROM "{tabela}"'
        ).fetchall()

        relatorio.write(
            f"Total de registros: {len(registros)}\n"
        )

        for coluna in colunas:
            nome = coluna[1]

            if nome.lower() in privados:
                continue

            vazios = []
            provis = []

            for registro in registros:
                valor = registro[coluna[0]]

                if valor is None or (
                    isinstance(valor, str) and not valor.strip()
                ):
                    vazios.append(registro[0])

                elif isinstance(valor, str) and (
                    valor.strip().lower() in provisorios
                ):
                    provis.append(registro[0])

            if vazios or provis:
                relatorio.write(f"\nCampo: {nome}\n")

                if vazios:
                    relatorio.write(
                        f"  Vazios: {len(vazios)}\n"
                    )
                    relatorio.write(
                        f"  IDs: {vazios}\n"
                    )

                if provis:
                    relatorio.write(
                        f"  Provisórios: {len(provis)}\n"
                    )
                    relatorio.write(
                        f"  IDs: {provis}\n"
                    )

print("Verificação concluída!")
print(f"Relatório salvo em: {ARQUIVO}")

conexao.close()
