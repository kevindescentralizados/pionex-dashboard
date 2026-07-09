"""Genera dist/index.html a partir de data/operativa-futuros-pionex.xlsx (hoja "Operaciones").

No depende de los valores cacheados de las fórmulas del Excel: el PnL neto y la
rentabilidad se recalculan aquí a partir de las columnas base, así el build
funciona igual aunque el archivo se edite con Excel, Numbers o LibreOffice.
"""
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
XLSX = ROOT / "data" / "operativa-futuros-pionex.xlsx"
TEMPLATE = ROOT / "templates" / "dashboard.template.html"
OUT = ROOT / "dist" / "index.html"

COLS = {
    "fecha": "Fecha Cierre",
    "simbolo": "Símbolo",
    "lado": "Lado",
    "tipo": "Tipo",
    "promedios": "Promedios",
    "capital": "Capital Desplegado ($)",
    "pnl": "PnL Bruto ($)",
    "fee": "Comisiones ($)",
    "funding": "Funding ($)",
    "resultado": "Resultado",
}


def main() -> int:
    df = pd.read_excel(XLSX, sheet_name="Operaciones")
    missing = [c for c in COLS.values() if c not in df.columns]
    if missing:
        print(f"ERROR: faltan columnas en la hoja 'Operaciones': {missing}")
        return 1

    df = df[df[COLS["simbolo"]].notna()].copy()
    df[COLS["fecha"]] = pd.to_datetime(df[COLS["fecha"]])
    for c in ("capital", "pnl", "fee", "funding", "promedios"):
        df[COLS[c]] = pd.to_numeric(df[COLS[c]], errors="coerce").fillna(0)
    df["net"] = df[COLS["pnl"]] + df[COLS["fee"]] + df[COLS["funding"]]
    df = df.sort_values(COLS["fecha"])

    ops = []
    for _, r in df.iterrows():
        cap = float(r[COLS["capital"]])
        net = float(r["net"])
        ops.append(
            {
                "d": r[COLS["fecha"]].strftime("%Y-%m-%d %H:%M"),
                "s": str(r[COLS["simbolo"]]),
                "l": str(r[COLS["lado"]]),
                "t": str(r[COLS["tipo"]]),
                "p": int(r[COLS["promedios"]]),
                "c": round(cap, 2),
                "n": round(net, 2),
                "r": round(net / cap * 100, 2) if cap > 0 else None,
                "res": str(r[COLS["resultado"]]),
            }
        )

    html = TEMPLATE.read_text(encoding="utf-8")
    html = html.replace("__DATA__", json.dumps(ops, ensure_ascii=False))
    html = html.replace("__UPDATED__", datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M"))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(html, encoding="utf-8")

    total = sum(o["n"] for o in ops)
    dias = len({o["d"][:10] for o in ops})
    print(f"OK: {len(ops)} operaciones, {dias} días, balance {total:,.2f} $ -> {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
