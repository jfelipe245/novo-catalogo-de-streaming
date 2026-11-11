python - <<'PY'
import sqlite3

c = sqlite3.connect("instance/afroedu_streaming.db")

for tabela in ["Usuarios", "Obras", "Favoritos", "Saiba_Mais"]:
    print("\n==========", tabela, "==========")
    print("COLUNAS:")

    for coluna in c.execute(f'PRAGMA table_info("{tabela}")'):
        print(coluna)

    print("ÍNDICES:")
    for indice in c.execute(f'PRAGMA index_list("{tabela}")'):
        print(indice)

c.close()
PY