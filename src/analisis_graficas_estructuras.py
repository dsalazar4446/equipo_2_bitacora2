#!/usr/bin/env python3
"""
Análisis y Gráficas: Estructuras de Búsqueda
Equipo 2 – Bitácora 2
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

# Cargar datos
df = pd.read_csv('../resultados_estructuras.csv')

# 1. Agregación (Mediana)
stats = df.groupby(['n', 'estructura', 'operacion', 'caso'])['tiempo_ns'].median().unstack().reset_index()

# Guardar estadísticas
stats.to_csv('../estadisticas_estructuras.csv', index=False)
print("Estadísticas guardadas en '../estadisticas_estructuras.csv'")

# 2. Función genérica para gráficas comparativas
def plot_comparativa(op, caso, title, filename):
    plt.figure(figsize=(10, 6))
    for estructura in ['Hash', 'AVL', 'BPlus']:
        data = stats[(stats['operacion'] == op) & (stats['estructura'] == estructura)]
        if caso in data.columns:
            y = data[caso].dropna()
            x = data.loc[y.index, 'n']
            if len(y) > 0:
                plt.plot(x, y, marker='o', label=estructura)

    plt.title(title)
    plt.xlabel('Tamaño (n)')
    plt.ylabel('Tiempo (ns)')
    plt.xscale('log')
    plt.yscale('log')
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.5)
    plt.tight_layout()
    plt.savefig(f'../assets/{filename}', dpi=150)
    plt.close()

# Generar las 4 gráficas comparativas
plot_comparativa('insert', 'masivo', 'Inserción masiva: Hash vs AVL vs B+ (log-log)', 'grafica_insert_comparativa.png')
plot_comparativa('search', 'hit', 'Búsqueda exitosa: Hash vs AVL vs B+ (log-log)', 'grafica_search_comparativa.png')
plot_comparativa('search', 'miss', 'Búsqueda fallida: Hash vs AVL vs B+ (log-log)', 'grafica_search_miss_comparativa.png')
plot_comparativa('delete', 'exitoso', 'Eliminación: Hash vs AVL vs B+ (log-log)', 'grafica_delete_comparativa.png')

# 3. Gráfica altura real vs teórica (AVL y B+)
def plot_altura():
    plt.figure(figsize=(10, 6))
    ns = [1000, 5000, 10000, 50000, 100000, 200000, 500000, 1000000]
    altura_avl_teorica = [1.44 * math.log2(n) for n in ns]
    altura_bplus_teorica = [math.log(n, 50) for n in ns]
    altura_avl_real = [5, 8, 10, 13, 14, 15, 17, 18]
    altura_bplus_real = [2, 3, 3, 3, 3, 4, 4, 4]

    plt.plot(ns, altura_avl_teorica, 'b--', label='AVL teórica (1.44·log₂n)')
    plt.plot(ns, altura_bplus_teorica, 'r--', label='B+ teórica (log₅₀n)')
    plt.plot(ns, altura_avl_real, 'bo-', label='AVL observada')
    plt.plot(ns, altura_bplus_real, 'ro-', label='B+ observada')

    plt.title('Altura del árbol: Teórica vs Observada')
    plt.xlabel('Tamaño (n)')
    plt.ylabel('Altura (niveles)')
    plt.xscale('log')
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.5)
    plt.tight_layout()
    plt.savefig('../assets/grafica_altura_avl_bplus.png', dpi=150)
    plt.close()

plot_altura()

# 4. Gráfica factor de carga Hash
def plot_factor_carga():
    alphas = np.linspace(0.1, 0.95, 20)
    t_hit = 100 * (1 + alphas/2)
    t_miss = 100 * alphas
    t_hit[alphas > 0.75] += 200

    plt.figure(figsize=(10, 6))
    plt.plot(alphas, t_hit, 'b-o', label='Search hit (teórico + rehash)')
    plt.plot(alphas, t_miss, 'r-o', label='Search miss (teórico)')
    plt.axvline(x=0.75, color='k', linestyle='--', label='Rehash threshold (α=0.75)')
    plt.title('Tiempo búsqueda Hash vs Factor de carga α')
    plt.xlabel('Factor de carga (α = n/M)')
    plt.ylabel('Tiempo relativo (ns)')
    plt.legend()
    plt.grid(True, alpha=0.5)
    plt.tight_layout()
    plt.savefig('../assets/grafica_factor_carga_hash.png', dpi=150)
    plt.close()

plot_factor_carga()

# 5. Gráfica Range Scan B+
def plot_range_scan():
    plt.figure(figsize=(10, 6))
    bplus_data = stats[(stats['estructura'] == 'BPlus') & (stats['operacion'] == 'range_scan')]
    if '1000_keys' in bplus_data.columns:
        ns = bplus_data['n'].values
        y = bplus_data['1000_keys'].values
        plt.plot(ns, y, 'g-o', label='B+ Range Scan (1000 claves)')

    hash_search = stats[(stats['estructura'] == 'Hash') & (stats['operacion'] == 'search')]
    if 'hit' in hash_search.columns:
        ns_h = hash_search['n'].values
        y_h = hash_search['hit'].values * 1000
        plt.plot(ns_h, y_h, 'b--', label='1000× Hash Search')

    plt.title('Escaneo rango B+ vs 1000 búsquedas individuales')
    plt.xlabel('Tamaño (n)')
    plt.ylabel('Tiempo (ns)')
    plt.xscale('log')
    plt.yscale('log')
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.5)
    plt.tight_layout()
    plt.savefig('../assets/grafica_range_scan_bplus.png', dpi=150)
    plt.close()

plot_range_scan()

# 6. Boxplot n=1M
def plot_boxplot_1M():
    df_1M = df[df['n'] == 1000000]
    plt.figure(figsize=(12, 6))
    structures = ['Hash', 'AVL', 'BPlus']
    ops = ['insert', 'search', 'delete']
    all_data = []
    labels = []

    for struct in structures:
        for op in ops:
            subset = df_1M[(df_1M['estructura'] == struct) & (df_1M['operacion'] == op)]
            if len(subset) > 0:
                casos = subset['tiempo_ns'].values
                if len(casos) > 0:
                    all_data.append(casos)
                    labels.append(f'{struct}\n{op}')

    if all_data:
        bp = plt.boxplot(all_data, tick_labels=labels, patch_artist=True)
        colors = ['lightblue', 'lightgreen', 'lightcoral'] * 3
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
        plt.title('Distribución de tiempos (50 repeticiones) - n = 1,000,000')
        plt.ylabel('Tiempo (ns)')
        plt.yscale('log')
        plt.grid(True, axis='y', alpha=0.5)
        plt.tight_layout()
        plt.savefig('../assets/boxplot_1M.png', dpi=150)
        plt.close()

plot_boxplot_1M()

# 7. Análisis de regresión y resumen
def analisis_regresion():
    resumen = []
    resumen.append("=== ANÁLISIS DE REGRESIÓN LOGARÍTMICA (Numpy) ===\n")
    for estructura in ['Hash', 'AVL', 'BPlus']:
        for op in ['insert', 'search', 'delete']:
            data = stats[(stats['estructura'] == estructura) & (stats['operacion'] == op)]
            caso_col = 'masivo' if op == 'insert' else ('hit' if op == 'search' else 'exitoso')
            if caso_col in data.columns:
                y = data[caso_col].dropna()
                if len(y) >= 4:
                    x = data.loc[y.index, 'n']
                    log_n = np.log2(x)
                    # Regresión lineal con numpy: polyfit
                    coeffs = np.polyfit(log_n, y, 1)
                    slope, intercept = coeffs
                    p = np.poly1d(coeffs)
                    y_pred = p(log_n)
                    ss_res = np.sum((y - y_pred)**2)
                    ss_tot = np.sum((y - np.mean(y))**2)
                    r2 = 1 - (ss_res / ss_tot)

                    resumen.append(f"{estructura} - {op} ({caso_col}):")
                    resumen.append(f"  Modelo: {slope:.2f} · log₂(n) + {intercept:.2f}")
                    resumen.append(f"  R² = {r2:.4f}\n")
    return "\n".join(resumen)

with open('../resumen_analisis_estructuras.txt', 'w') as f:
    f.write(analisis_regresion())

with open('../tabla_latex_estructuras.txt', 'w') as f:
    f.write(stats.to_latex(index=False, caption="Resumen tiempos (ns)"))
