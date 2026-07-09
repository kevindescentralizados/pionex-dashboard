# Dashboard Operativa Futuros — Pionex

Pipeline automático: exportas los CSV de Pionex, los arrastras al repo y GitHub Actions analiza toda la operativa (promedios, liquidaciones, fees, funding) y regenera el dashboard y el Excel. No hay que editar ningún Excel a mano.

## Estructura

```
data/position_futures.csv        ← export de Pionex (posiciones cerradas)
data/raw-trading-details.csv     ← export de Pionex (fills)
data/others.csv                  ← export de Pionex (funding, RiskCoverage)
data/operaciones-manuales.csv    ← operaciones aún no incluidas en el export (opcional)
scripts/build_dashboard.py       ← análisis completo + generación de salidas
templates/dashboard.template.html
.github/workflows/deploy.yml     ← build + deploy a GitHub Pages en cada push
dist/                            ← salida del pipeline (no se versiona)
```

## Flujo de trabajo

1. En Pionex: exporta el histórico (los mismos CSV de siempre).
2. En github.com, entra en la carpeta `data/` → **Add file → Upload files** → arrastra `position_futures.csv`, `raw-trading-details.csv` y `others.csv` (mismos nombres, se sobrescriben) → **Commit changes**.
3. En ~1-2 minutos el dashboard está actualizado en GitHub Pages, con el Excel de reporte descargable desde el propio dashboard (botón "Descargar Excel").

El script hace en cada build el análisis completo: asigna los fills a cada posición, cuenta los promedios, detecta liquidaciones vía RiskCoverage, separa bots de operaciones manuales y calcula rentabilidad sobre capital desplegado.

## Operaciones que aún no están en el export

Si cierras operaciones después de tu último export y quieres verlas ya en el dashboard, añádelas como filas en `data/operaciones-manuales.csv`:

```
symbol,side,open_time,close_time,pnl,fee,funding,capital,promedios,liquidada
EVAA,short,2026-07-09 12:05:44,2026-07-09 12:44:09,200.32,0,0,1000,0,no
```

Cuando reexportes los CSV y ya incluyan esas operaciones, el script las deduplica solo (mismo símbolo y cierre a menos de 2 minutos) — no hace falta borrarlas del CSV manual.

## Probar en local

```bash
pip install -r requirements.txt
python scripts/build_dashboard.py
open dist/index.html
```
