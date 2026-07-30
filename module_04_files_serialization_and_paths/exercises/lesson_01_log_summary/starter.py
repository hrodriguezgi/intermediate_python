from pathlib import Path


def summarize_log(path: Path) -> dict:
    """
    Lee archivo de logs y retorna conteo de líneas por nivel.

    Args:
        path: Ruta al archivo de logs

    Returns:
        Dict con conteos: {"INFO": int, "WARNING": int, "ERROR": int}

    Hint: Usa read_text() para leer el archivo con encoding="utf-8"
    """
    # TODO: Implementa la función
    diccionario = {"INFO": 0, "WARNING": 0, "ERROR": 0}
    contenido = path.read_text(encoding="utf-8")

    for linea in contenido.splitlines():
        for nivel in diccionario.keys():
            if linea.startswith(nivel):
                diccionario[nivel] += 1
                break

    return diccionario


if __name__ == "__main__":
    log_path = Path(__file__).resolve().parents[2] / "data" / "sample_log.txt"
    print(summarize_log(log_path))
