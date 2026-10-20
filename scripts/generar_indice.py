#!/usr/bin/env python3
"""
Genera el índice de writeups del README, agrupado por categoría.

Lee cada archivo .md dentro de writeups/ (excepto README.md) y toma:
  - El título: primera línea que empieza con "# ".
  - Los metadatos: primera línea en negrita con el formato
    **Plataforma / Categoría principal, otras categorías / Dificultad / Fecha**

Luego reemplaza el contenido entre los marcadores
<!-- INDICE:INICIO --> y <!-- INDICE:FIN --> del README.md.

Solo usa la biblioteca estándar de Python.
"""
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
README = RAIZ / "README.md"
CARPETA = RAIZ / "writeups"
INICIO, FIN = "<!-- INDICE:INICIO -->", "<!-- INDICE:FIN -->"

MESES = {m: i for i, m in enumerate(
    ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
     "agosto", "septiembre", "octubre", "noviembre", "diciembre"], start=1)}
MESES["setiembre"] = 9


def leer_fecha(texto):
    """Acepta '19 de octubre de 2026', 'octubre de 2026' o 'Abril 2026'."""
    t = texto.strip().lower()
    m = re.fullmatch(r"(?:(\d{1,2})\s+de\s+)?([a-záéíóú]+)(?:\s+de)?\s+(\d{4})", t)
    if not m or m.group(2) not in MESES:
        return None
    return date(int(m.group(3)), MESES[m.group(2)], int(m.group(1) or 1))


def leer_writeup(ruta):
    titulo, meta = None, None
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if titulo is None and linea.startswith("# "):
            titulo = linea[2:].strip()
        elif meta is None and re.fullmatch(r"\*\*.+\*\*", linea):
            meta = linea.strip("*").strip()
        if titulo and meta:
            break
    partes = [p.strip() for p in meta.split(" / ")] if meta else []
    if not titulo or len(partes) != 4:
        print(f"AVISO: {ruta} no tiene título o metadatos con 4 partes; se omite.", file=sys.stderr)
        return None
    plataforma, categorias, dificultad, fecha_txt = partes
    categorias = [c.strip() for c in categorias.split(",") if c.strip()]
    fecha = leer_fecha(fecha_txt)
    if fecha is None:
        print(f"AVISO: fecha no reconocida en {ruta}: '{fecha_txt}'", file=sys.stderr)
    return {
        "titulo": titulo, "plataforma": plataforma, "categoria": categorias[0],
        "otras": categorias[1:], "dificultad": dificultad, "fecha_txt": fecha_txt,
        "fecha": fecha or date.min, "ruta": ruta.relative_to(RAIZ).as_posix(),
    }


def generar_indice(writeups):
    grupos = defaultdict(list)
    for w in writeups:
        grupos[w["categoria"]].append(w)
    orden = sorted(grupos, key=lambda c: (-len(grupos[c]), c.lower()))

    lineas = [f"**{len(writeups)} writeups** en {len(grupos)} categorías: "
              + " · ".join(f"[{c}](#{ancla(c)}) ({len(grupos[c])})" for c in orden), ""]
    for c in orden:
        lineas += [f"### {c}", "",
                   "| Nombre | Plataforma | Otros temas | Dificultad | Fecha |",
                   "|---|---|---|---|---|"]
        for w in sorted(grupos[c], key=lambda w: w["fecha"], reverse=True):
            otras = ", ".join(w["otras"]) or "—"
            lineas.append(f"| [{w['titulo']}]({w['ruta']}) | {w['plataforma']} | {otras} "
                          f"| {w['dificultad']} | {w['fecha_txt']} |")
        lineas.append("")
    return "\n".join(lineas).rstrip()


def ancla(texto):
    """Reproduce cómo GitHub genera el ancla de un título."""
    t = texto.strip().lower()
    t = re.sub(r"[^\w\- ]", "", t)
    return t.replace(" ", "-")


def main():
    rutas = sorted(p for p in CARPETA.rglob("*.md") if p.name.lower() != "readme.md")
    writeups = [w for w in map(leer_writeup, rutas) if w]
    contenido = README.read_text(encoding="utf-8")
    if INICIO not in contenido or FIN not in contenido:
        sys.exit(f"ERROR: faltan los marcadores {INICIO} y {FIN} en README.md")
    antes, resto = contenido.split(INICIO, 1)
    _, despues = resto.split(FIN, 1)
    nuevo = f"{antes}{INICIO}\n{generar_indice(writeups)}\n{FIN}{despues}"
    if nuevo != contenido:
        README.write_text(nuevo, encoding="utf-8")
        print(f"Índice actualizado: {len(writeups)} writeups.")
    else:
        print("El índice ya estaba al día.")


if __name__ == "__main__":
    main()
