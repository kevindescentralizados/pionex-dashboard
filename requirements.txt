# Dashboard Operativa Futuros — Pionex

Pipeline automático: modificas el Excel, lo subes al repo y GitHub Actions regenera y publica el dashboard HTML. Sin pasos manuales intermedios.

## Estructura

```
data/operativa-futuros-pionex.xlsx   ← el único archivo que tocas
scripts/build_dashboard.py           ← lee el Excel y genera el HTML
templates/dashboard.template.html    ← plantilla con el sistema visual Descentralizados
.github/workflows/deploy.yml         ← build + deploy a GitHub Pages en cada push
dist/index.html                      ← salida (la genera el pipeline, no se versiona)
```

## Puesta en marcha (una sola vez, ~3 minutos)

1. Crea un repo en GitHub (recomendado **privado** — ver nota de privacidad abajo) y sube todo el contenido de esta carpeta.
2. En el repo: **Settings → Pages → Build and deployment → Source: GitHub Actions**.
3. Haz cualquier push a `main` (o lanza el workflow desde **Actions → Actualizar dashboard → Run workflow**).
4. En 1-2 minutos el dashboard queda publicado en `https://<usuario>.github.io/<repo>/`.

## Flujo de trabajo diario

1. Edita `data/operativa-futuros-pionex.xlsx` (hoja **Operaciones**): añade filas, corrige datos, etc.
2. Súbelo al repo. Dos opciones:
   - **Sin terminal:** en github.com entra en `data/`, botón **Add file → Upload files**, arrastra el Excel y **Commit changes**.
   - **Con terminal:** `git add data/ && git commit -m "update" && git push`
3. GitHub Actions se dispara solo. En ~1 minuto el dashboard está actualizado con sello de fecha/hora.

El script recalcula PnL neto y rentabilidad desde las columnas base (PnL Bruto + Comisiones + Funding), así que da igual con qué programa edites el Excel — no depende de que las fórmulas estén recalculadas.

Columnas que el script necesita en la hoja "Operaciones": `Fecha Cierre`, `Símbolo`, `Lado`, `Tipo`, `Promedios`, `Capital Desplegado ($)`, `PnL Bruto ($)`, `Comisiones ($)`, `Funding ($)`, `Resultado`. Puedes añadir columnas extra sin romper nada.

## Nota de privacidad

GitHub Pages publica el HTML en una URL **pública** aunque el repo sea privado. La URL no está indexada ni es adivinable fácilmente, pero cualquiera con el enlace ve los datos. Si quieres el dashboard protegido con contraseña, la alternativa es desplegar `dist/` en Netlify (que ya usáis) y activar **Site protection → Password**: basta con cambiar el último paso del workflow por `netlify deploy --prod --dir=dist` con los secrets `NETLIFY_AUTH_TOKEN` y `NETLIFY_SITE_ID`.

## Probar en local

```bash
pip install -r requirements.txt
python scripts/build_dashboard.py
open dist/index.html
```
