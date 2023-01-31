from pathlib import Path

import extratores
import transformadores
import carregadores
from tipos import IO


ID_PROJETO = 'datalake-375813'
NOME_BUCKET_LAYER_RAW = 'bzco_layer_raw'
NOME_BUCKET_LAYER_2 = 'bzco_layer_2'
CAMINHO_PARA_ARQUIVOS_DE_CACHE = Path(__file__).parent.parent / "cache"


def reset_de_pedidos() -> IO:
    carregadores.google_planilhas.construtor_de_tabelas(
        transformadores.pedido_json.múltiplos(
            extratores.bling.todos_os_pedidos()),
        planilha="1ZYMvRXGn2-koFUTyJO2fTqp6eYf1dS91NYZhn_Y8ByY",
        intervalo="'Base do Bling'!A:AA")

    carregadores.google_planilhas.ultima_atualizacao()

    carregadores.google_cloud_storage.subir_para_o_bucket(
        caminho_do_arquivo=CAMINHO_PARA_ARQUIVOS_DE_CACHE / "todos_os_pedidos.json",
        id_projeto=ID_PROJETO,
        nome_do_bucket=NOME_BUCKET_LAYER_RAW,
        nome_do_blob="todos_os_pedidos.json")
    carregadores.google_cloud_storage.subir_para_o_bucket(
        caminho_do_arquivo=CAMINHO_PARA_ARQUIVOS_DE_CACHE / "pedidos.parquet",
        id_projeto=ID_PROJETO,
        nome_do_bucket=NOME_BUCKET_LAYER_2,
        nome_do_blob="pedidos.parquet")


if __name__ == '__main__':
    reset_de_pedidos()
