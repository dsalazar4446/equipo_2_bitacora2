import sys
import os
import pytest
from hypothesis import given, strategies as st

# Añadir src al path para importar
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))
from estructuras_busqueda import TablaHash, AVL, BPlus

# --- 1. Pruebas Unitarias (Casos Límite) ---
def test_tabla_hash_limites():
    h = TablaHash()
    h.insert(10)
    assert h.search(10) == True
    h.delete(10)
    assert h.search(10) == False
    assert h.search(999) == False # Clave no existente

# --- 2. Pruebas con Hypothesis (Propiedades) ---
@given(st.lists(st.integers(), min_size=1, unique=True))
def test_avl_propiedad_orden(claves):
    tree = AVL()
    for k in claves:
        tree.insert(k)
    # Verificar orden BST (ejecutando búsqueda de todos)
    for k in claves:
        assert tree.search(k) == True

# --- 3. Prueba Diferencial ---
def test_hash_diferencial():
    claves = [1, 5, 2, 8, 3]
    h = TablaHash()
    ref = set()
    for k in claves:
        h.insert(k)
        ref.add(k)
    
    for k in claves:
        assert h.search(k) == (k in ref)
    
    assert h.search(100) == (100 in ref)

if __name__ == "__main__":
    pytest.main([__file__])
