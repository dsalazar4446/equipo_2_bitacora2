#!/usr/bin/env python3
"""
Pruebas empíricas Estructuras de Búsqueda: Hash, AVL, B+
Equipo 2 – Bitácora 2
Genera resultados_estructuras.csv con mediciones reales
"""

import time
import random
import csv
import sys
import math

# ============================================================
# 1. TABLA HASH CON ENCADENAMIENTO + REHASHING
# ============================================================
class TablaHash:
    def __init__(self, M=1009):
        self.M = self._next_prime(M)
        self.tabla = [[] for _ in range(self.M)]
        self.n = 0

    def _next_prime(self, n):
        def is_prime(x):
            if x < 2: return False
            if x % 2 == 0: return x == 2
            for i in range(3, int(math.sqrt(x)) + 1, 2):
                if x % i == 0: return False
            return True
        p = n | 1
        while not is_prime(p): p += 2
        return p

    def _rehash(self):
        old = self.tabla
        self.M = self._next_prime(self.M * 2)
        self.tabla = [[] for _ in range(self.M)]
        self.n = 0
        for bucket in old:
            for k in bucket:
                self.insert(k)

    def _hash(self, k): return k % self.M

    def insert(self, k):
        if self.n / self.M > 0.75:
            self._rehash()
        i = self._hash(k)
        if k not in self.tabla[i]:
            self.tabla[i].append(k)
            self.n += 1

    def search(self, k):
        i = self._hash(k)
        return k in self.tabla[i]

    def delete(self, k):
        i = self._hash(k)
        if k in self.tabla[i]:
            self.tabla[i].remove(k)
            self.n -= 1

# ============================================================
# 2. ÁRBOL AVL COMPLETO
# ============================================================
class NodoAVL:
    __slots__ = ('key', 'left', 'right', 'height')
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVL:
    def __init__(self):
        self.root = None

    def _height(self, n): return n.height if n else 0
    def _balance(self, n): return self._height(n.left) - self._height(n.right) if n else 0

    def _rotate_right(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self._height(y.left), self._height(y.right))
        x.height = 1 + max(self._height(x.left), self._height(x.right))
        return x

    def _rotate_left(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = 1 + max(self._height(x.left), self._height(x.right))
        y.height = 1 + max(self._height(y.left), self._height(y.right))
        return y

    def insert(self, key):
        self.root = self._insert(self.root, key)

    def _insert(self, node, key):
        if not node: return NodoAVL(key)
        if key < node.key: node.left = self._insert(node.left, key)
        elif key > node.key: node.right = self._insert(node.right, key)
        else: return node

        node.height = 1 + max(self._height(node.left), self._height(node.right))
        balance = self._balance(node)

        if balance > 1 and key < node.left.key: return self._rotate_right(node)
        if balance < -1 and key > node.right.key: return self._rotate_left(node)
        if balance > 1 and key > node.left.key:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance < -1 and key < node.right.key:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        while node:
            if key == node.key: return True
            elif key < node.key: node = node.left
            else: node = node.right
        return False

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if not node: return node
        if key < node.key: node.left = self._delete(node.left, key)
        elif key > node.key: node.right = self._delete(node.right, key)
        else:
            if not node.left: return node.right
            elif not node.right: return node.left
            temp = self._min_node(node.right)
            node.key = temp.key
            node.right = self._delete(node.right, temp.key)

        if not node: return node
        node.height = 1 + max(self._height(node.left), self._height(node.right))
        balance = self._balance(node)

        if balance > 1 and self._balance(node.left) >= 0: return self._rotate_right(node)
        if balance > 1 and self._balance(node.left) < 0:
            node.left = self._rotate_left(node.left)
            return self._rotate_right(node)
        if balance < -1 and self._balance(node.right) <= 0: return self._rotate_left(node)
        if balance < -1 and self._balance(node.right) > 0:
            node.right = self._rotate_right(node.right)
            return self._rotate_left(node)
        return node

    def _min_node(self, node):
        while node.left: node = node.left
        return node

# ============================================================
# 3. ÁRBOL B+ COMPLETO (orden m)
# ============================================================
class NodoBPlus:
    __slots__ = ('keys', 'children', 'leaf', 'next_leaf')
    def __init__(self, leaf=False):
        self.keys = []
        self.children = []
        self.leaf = leaf
        self.next_leaf = None

class BPlus:
    def __init__(self, m=100):
        self.m = m
        self.root = NodoBPlus(leaf=True)

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        if node.leaf:
            return i < len(node.keys) and node.keys[i] == key
        return self._search(node.children[i], key)

    def insert(self, key):
        root = self.root
        if len(root.keys) == self.m - 1:
            new_root = NodoBPlus()
            new_root.children.append(root)
            self._split_child(new_root, 0)
            self.root = new_root
        self._insert_non_full(self.root, key)

    def _insert_non_full(self, node, key):
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append(0)
            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = key
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == self.m - 1:
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1
            self._insert_non_full(node.children[i], key)

    def _split_child(self, parent, i):
        m = self.m
        child = parent.children[i]
        new_node = NodoBPlus(leaf=child.leaf)
        mid = m // 2

        if child.leaf:
            new_node.keys = child.keys[mid:]
            child.keys = child.keys[:mid]
            new_node.next_leaf = child.next_leaf
            child.next_leaf = new_node
            parent.keys.insert(i, new_node.keys[0])
        else:
            new_node.keys = child.keys[mid + 1:]
            child.keys = child.keys[:mid + 1]
            new_node.children = child.children[mid + 1:]
            child.children = child.children[:mid + 1]
            parent.keys.insert(i, child.keys.pop())

        parent.children.insert(i + 1, new_node)

    def delete(self, key):
        self._delete(self.root, key)
        if not self.root.keys and not self.root.leaf:
            self.root = self.root.children[0]

    def _delete(self, node, key):
        idx = 0
        while idx < len(node.keys) and key > node.keys[idx]:
            idx += 1
        if node.leaf:
            if idx < len(node.keys) and node.keys[idx] == key:
                node.keys.pop(idx)
            return
        if idx < len(node.keys) and node.keys[idx] == key:
            pred = self._get_predecessor(node, idx)
            node.keys[idx] = pred
            self._delete(node.children[idx], pred)
        else:
            self._delete(node.children[idx], key)

        if len(node.children[idx].keys) < (self.m - 1) // 2:
            self._rebalance(node, idx)

    def _get_predecessor(self, node, idx):
        cur = node.children[idx]
        while not cur.leaf:
            cur = cur.children[-1]
        return cur.keys[-1]

    def _rebalance(self, parent, idx):
        child = parent.children[idx]
        if idx > 0 and len(parent.children[idx - 1].keys) > (self.m - 1) // 2:
            self._borrow_from_left(parent, idx)
        elif idx < len(parent.children) - 1 and len(parent.children[idx + 1].keys) > (self.m - 1) // 2:
            self._borrow_from_right(parent, idx)
        elif idx > 0:
            self._merge(parent, idx - 1)
        else:
            self._merge(parent, idx)

    def _borrow_from_left(self, parent, idx):
        child = parent.children[idx]
        sibling = parent.children[idx - 1]
        if child.leaf:
            child.keys.insert(0, sibling.keys.pop())
            parent.keys[idx - 1] = child.keys[0]
        else:
            child.keys.insert(0, parent.keys[idx - 1])
            parent.keys[idx - 1] = sibling.keys.pop()
            child.children.insert(0, sibling.children.pop())

    def _borrow_from_right(self, parent, idx):
        child = parent.children[idx]
        sibling = parent.children[idx + 1]
        if child.leaf:
            child.keys.append(sibling.keys.pop(0))
            parent.keys[idx] = sibling.keys[0]
        else:
            child.keys.append(parent.keys[idx])
            parent.keys[idx] = sibling.keys.pop(0)
            child.children.append(sibling.children.pop(0))

    def _merge(self, parent, idx):
        left = parent.children[idx]
        right = parent.children.pop(idx + 1)
        if left.leaf:
            left.keys.extend(right.keys)
            left.next_leaf = right.next_leaf
        else:
            left.keys.append(parent.keys.pop(idx))
            left.keys.extend(right.keys)
            left.children.extend(right.children)
        if not parent.keys and not parent.leaf:
            self.root = left

    def range_scan(self, start_key, count):
        """Escanea 'count' claves a partir de start_key"""
        results = []
        node = self.root
        # Bajar a hoja
        while not node.leaf:
            i = 0
            while i < len(node.keys) and start_key > node.keys[i]:
                i += 1
            node = node.children[i]
        # Buscar posición en hoja
        i = 0
        while i < len(node.keys) and node.keys[i] < start_key:
            i += 1
        # Recorrer hojas
        while node and len(results) < count:
            while i < len(node.keys) and len(results) < count:
                results.append(node.keys[i])
                i += 1
            node = node.next_leaf
            i = 0
        return results

# ============================================================
# FUNCIONES DE MEDICIÓN
# ============================================================
def medir_tiempo(func, *args, reps=1):
    """Mide tiempo en nanosegundos, retorna mediana de reps ejecuciones"""
    times = []
    for _ in range(reps):
        start = time.perf_counter_ns()
        func(*args)
        end = time.perf_counter_ns()
        times.append(end - start)
    times.sort()
    return times[len(times) // 2]

def generar_claves(n, max_val=10**9):
    """Genera n claves únicas aleatorias"""
    return random.sample(range(max_val), n)

# ============================================================
# MAIN
# ============================================================
def main():
    # Tamaños de prueba
    sizes = [1000, 5000, 10000, 50000, 100000, 200000, 500000, 1000000]
    repeticiones = 10  # repeticiones por medición (cada una es mediana de 5 runs internos)

    print(f"Iniciando pruebas para tamaños: {sizes}")
    print(f"Repeticiones por caso: {repeticiones}")
    print("=" * 60)

    with open('resultados_estructuras.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['n', 'estructura', 'operacion', 'caso', 'tiempo_ns'])

        total_mediciones = 0
        for n in sizes:
            print(f"\n--- n = {n} ---")
            claves = generar_claves(n)
            claves_busqueda = claves[:n//2]  # para búsqueda exitosa
            claves_no_exist = [10**9 + i for i in range(1000)]  # no existen

            # ---------- TABLA HASH ----------
            print("  Hash...", end=" ", flush=True)
            h = TablaHash()

            # Inserción masiva (medir tiempo total, luego dividir)
            start = time.perf_counter_ns()
            for k in claves:
                h.insert(k)
            end = time.perf_counter_ns()
            t_insert = (end - start) / n
            writer.writerow([n, 'Hash', 'insert', 'masivo', int(t_insert)])
            total_mediciones += 1

            # Búsqueda exitosa
            for k in random.sample(claves_busqueda, min(50, len(claves_busqueda))):
                t = medir_tiempo(h.search, k, reps=5)
                writer.writerow([n, 'Hash', 'search', 'hit', t])
                total_mediciones += 1

            # Búsqueda fallida
            for k in random.sample(claves_no_exist, 50):
                t = medir_tiempo(h.search, k, reps=5)
                writer.writerow([n, 'Hash', 'search', 'miss', t])
                total_mediciones += 1

            # Eliminación
            for k in random.sample(claves_busqueda, min(50, len(claves_busqueda))):
                t = medir_tiempo(h.delete, k, reps=1)
                writer.writerow([n, 'Hash', 'delete', 'exitoso', t])
                total_mediciones += 1
            print("OK")

            # ---------- ÁRBOL AVL ----------
            print("  AVL...", end=" ", flush=True)
            avl = AVL()

            start = time.perf_counter_ns()
            for k in claves:
                avl.insert(k)
            end = time.perf_counter_ns()
            t_insert = (end - start) / n
            writer.writerow([n, 'AVL', 'insert', 'masivo', int(t_insert)])
            total_mediciones += 1

            for k in random.sample(claves_busqueda, min(50, len(claves_busqueda))):
                t = medir_tiempo(avl.search, k, reps=5)
                writer.writerow([n, 'AVL', 'search', 'hit', t])
                total_mediciones += 1

            for k in random.sample(claves_no_exist, 50):
                t = medir_tiempo(avl.search, k, reps=5)
                writer.writerow([n, 'AVL', 'search', 'miss', t])
                total_mediciones += 1

            for k in random.sample(claves_busqueda, min(50, len(claves_busqueda))):
                t = medir_tiempo(avl.delete, k, reps=1)
                writer.writerow([n, 'AVL', 'delete', 'exitoso', t])
                total_mediciones += 1
            print("OK")

            # ---------- ÁRBOL B+ ----------
            print("  B+...", end=" ", flush=True)
            bplus = BPlus(m=100)

            start = time.perf_counter_ns()
            for k in claves:
                bplus.insert(k)
            end = time.perf_counter_ns()
            t_insert = (end - start) / n
            writer.writerow([n, 'BPlus', 'insert', 'masivo', int(t_insert)])
            total_mediciones += 1

            for k in random.sample(claves_busqueda, min(50, len(claves_busqueda))):
                t = medir_tiempo(bplus.search, k, reps=5)
                writer.writerow([n, 'BPlus', 'search', 'hit', t])
                total_mediciones += 1

            for k in random.sample(claves_no_exist, 50):
                t = medir_tiempo(bplus.search, k, reps=5)
                writer.writerow([n, 'BPlus', 'search', 'miss', t])
                total_mediciones += 1

            for k in random.sample(claves_busqueda, min(50, len(claves_busqueda))):
                t = medir_tiempo(bplus.delete, k, reps=1)
                writer.writerow([n, 'BPlus', 'delete', 'exitoso', t])
                total_mediciones += 1

            # Range scan (solo B+)
            start_key = claves[n//2]
            t = medir_tiempo(bplus.range_scan, start_key, 1000, reps=3)
            writer.writerow([n, 'BPlus', 'range_scan', '1000_keys', t])
            total_mediciones += 1
            print("OK")

    print(f"\n{'='*60}")
    print(f"Total mediciones: {total_mediciones}")
    print("Resultados guardados en 'resultados_estructuras.csv'")

if __name__ == "__main__":
    main()