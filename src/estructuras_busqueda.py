#!/usr/bin/env python3
"""
Implementaciones de Estructuras de Búsqueda
Equipo 2 – Bitácora 2
"""

# 1. Tabla Hash
class TablaHash:
    def __init__(self, M=1009):
        self.M = M
        self.tabla = [[] for _ in range(M)]
        self.n = 0

    def _hash(self, k): return k % self.M

    def insert(self, k):
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

# 2. Árbol AVL (Simplificado para ilustración)
class NodoAVL:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1

class AVL:
    def get_height(self, n): return n.height if n else 0
    def get_balance(self, n): return self.get_height(n.left) - self.get_height(n.right) if n else 0

    def rotate_right(self, y):
        x = y.left
        T2 = x.right
        x.right = y
        y.left = T2
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        return x

    def rotate_left(self, x):
        y = x.right
        T2 = y.left
        y.left = x
        x.right = T2
        x.height = 1 + max(self.get_height(x.left), self.get_height(x.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def insert(self, root, key):
        if not root: return NodoAVL(key)
        if key < root.key: root.left = self.insert(root.left, key)
        else: root.right = self.insert(root.right, key)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        if balance > 1 and key < root.left.key: return self.rotate_right(root)
        if balance < -1 and key > root.right.key: return self.rotate_left(root)
        if balance > 1 and key > root.left.key:
            root.left = self.rotate_left(root.left)
            return self.rotate_right(root)
        if balance < -1 and key < root.right.key:
            root.right = self.rotate_right(root.right)
            return self.rotate_left(root)
        return root

    def search(self, root, key):
        if not root or root.key == key: return root is not None
        if root.key < key: return self.search(root.right, key)
        return self.search(root.left, key)

# 3. Árbol B+ (Simplificado para ilustración)
class NodoBPlus:
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.children = []

class BPlus:
    def __init__(self, t=50): self.root = NodoBPlus(True); self.t = t

    def search(self, k): return self._search(self.root, k)

    def _search(self, node, k):
        i = 0
        while i < len(node.keys) and k > node.keys[i]: i += 1
        if node.leaf: return i < len(node.keys) and node.keys[i] == k
        return self._search(node.children[i], k)

    def insert(self, k):
        # Implementación completa de B+ es extensa;
        # para propósitos de bitácora, esta es la interfaz.
        # En una entrega real, usaría una implementación completa o librería balanceada.
        pass
