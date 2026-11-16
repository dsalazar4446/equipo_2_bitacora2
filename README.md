# Bitácora 2: Estructuras de Búsqueda

Repositorio para el análisis de Tabla Hash, Árboles AVL y Árboles B+.

## Requisitos
- Python 3.15+
- Dependencias: `pip install -r requirements.txt`

## Ejecución
1. Generar datos y mediciones:
   `python3 pruebas_estructuras.py`
2. Generar análisis y gráficas:
   `python3 analisis_graficas_estructuras.py`

## Control de Semillas
- Se utiliza `random.seed(42)` en `pruebas_estructuras.py` para garantizar reproducibilidad.

## Resultados Visuales

### Inserción Comparativa
![Inserción Hash vs AVL vs B+](grafica_insert_comparativa.png)

### Búsqueda Exitosa Comparativa
![Búsqueda Hash vs AVL vs B+](grafica_search_comparativa.png)

### Eliminación Comparativa
![Eliminación Hash vs AVL vs B+](grafica_delete_comparativa.png)

### Altura AVL vs B+
![Comparación de Alturas](grafica_altura_avl_bplus.png)

### Factor de Carga Hash
![Comportamiento Hash (Rehash)](grafica_factor_carga_hash.png)

### Escaneo de Rango (B+)
![Escaneo Rango B+](grafica_range_scan_bplus.png)
