# PROYECTO-FINAL-MUSK

Análisis de clientes y ventas: carga datos desde un JSON y un CSV, los cruza,
realiza 10 cálculos y genera un informe final en JSON.

Proyecto final del curso de Programación en Python.

Incluye:
- POO
- Programación funcional
- Pandas
- Bucles
- Condicionales
- GitHub Actions
- Tests automáticos


## Estructura

```
data/      clients.json y sales.csv (datos de entrada, no se modifican)
src/       código del proyecto
tests/     pruebas unitarias
.github/   workflow de CI
```

| Archivo en `src/` | Contenido |
|---|---|
| `client.py` | Clase `Client` |
| `sale.py` | Clase `Sale` |
| `client_collection.py` | Consultas sobre la lista de clientes |
| `sales_collection.py` | Consultas sobre la lista de ventas |
| `functional_utils.py` | Funciones puras: filtros, extracción de importes y suma |
| `analyze.py` | Script principal: lee los datos, crea los objetos, hace los cálculos y genera el informe |


## Instalación

```
py -m pip install -r requirements.txt
```


## Uso

```
py -m src.analyze
```

El resultado se guarda en `final_report.json`, en la raíz del proyecto.

**Importante:** hay que ejecutarlo con `-m`, no como `py src/analyze.py`. Al lanzar
el archivo directamente, Python añade `src/` a la ruta de búsqueda en lugar de la
raíz del proyecto, y los imports del tipo `from src.client import Client` fallan con
`ModuleNotFoundError: No module named 'src'`.


## Tests

```
py -m pytest -q
```

## Los 10 cálculos

1. Número total de clientes → `summary.total_clients`
2. Número total de ventas → `summary.total_sales`
3. Total de ingresos por cliente → `clients[].total_spent`
4. Número de ventas por cliente → `clients[].sale_count`
5. Ingreso promedio por venta → `clients[].average_sale`
6. Cliente con mayor gasto por país → `top_client_by_country`
7. Total de ventas por categoría → `sales_by_category`
8. Cliente con más ventas en una categoría → no se exporta (ver notas)
9. Clientes que superan un gasto mínimo → `high_spending_clients`
10. Ventas acumuladas mes a mes → `monthly_sales`

Los cálculos 7 y 10 usan pandas, y el 8 las funciones puras de `functional_utils.py`.
El total de ingresos (`summary.total_revenue`) se obtiene con `map` y `reduce`.


## Notas y decisiones

### El cálculo 8 no aparece en el informe JSON

El enunciado pide el cálculo 8, pero la estructura JSON que especifica tiene 6
claves y ninguna le corresponde. Añadir una séptima rompería la validación de la CI.

Lo he implementado en `analyze.py`, combinando las dos funciones puras
`filter_sales_by_category` y `filter_sales_by_client` tal y como describe el
enunciado. Su resultado no se exporta, porque el informe no lo contempla; con los
datos de `data/` es Alice, con 2 ventas en Electronics.

### Dos decisiones de implementación

- **`sale_id` como texto.** El enunciado lo describe como `int`, pero los
  identificadores del CSV son `S1001`, `S1002`... He optado por tratarlos como
  `str` para no perder el prefijo.
- **Agrupación por mes con `strftime`.** El enunciado sugiere `dt.to_period("M")`.
  He usado `dt.strftime("%Y-%m")` porque devuelve directamente la cadena
  `"2023-07"`, que es la que esperan los tests y la única que `json.dump` admite
  como clave de diccionario.

### Sobre los tests

No he modificado ninguno de los cinco archivos de test del repositorio base,
siguiendo la instrucción del enunciado. He añadido uno nuevo,
`tests/test_functional_utils.py`, con pruebas unitarias de las dos funciones puras
de filtrado: construye sus propios datos de prueba, sin depender de `data/`, y
comprueba tanto el caso normal como el caso en que no hay resultados.


## Validación automática

Cada push ejecuta GitHub Actions para validar:

- Estructura del JSON final
- Cálculos correctos
- Código ejecutable
