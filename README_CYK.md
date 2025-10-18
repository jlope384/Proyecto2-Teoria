# Proyecto 2 - Teoría de la Computación
## Algoritmo CYK con Programación Dinámica

### 📋 Descripción General

Este proyecto implementa el **algoritmo CYK (Cocke-Younger-Kasami)** para validar si una oración en inglés pertenece al lenguaje definido por una gramática libre de contexto.

### 🎯 Características Principales

1. **Conversión Automática a CNF**: El programa convierte automáticamente cualquier gramática a **Forma Normal de Chomsky (CNF)** antes de ejecutar el algoritmo CYK.

2. **Programación Dinámica**: Implementa CYK usando programación dinámica con complejidad **O(n³ · |G|)**.

3. **Construcción de Árbol de Parseo**: Genera el árbol sintáctico completo para oraciones válidas.

4. **Medición de Tiempo**: Reporta el tiempo de ejecución en milisegundos.

---

## 📚 Forma Normal de Chomsky (CNF)

### ¿Qué es CNF?

Una gramática está en **Forma Normal de Chomsky** si todas sus producciones tienen una de estas dos formas:

- **A → a** (un no-terminal produce un terminal)
- **A → BC** (un no-terminal produce exactamente dos no-terminales)

### ¿Por qué CYK requiere CNF?

El algoritmo CYK **requiere obligatoriamente** que la gramática esté en CNF porque:

1. **Subdivisión binaria**: Las reglas de la forma A → BC permiten dividir el problema en exactamente dos subproblemas (izquierda y derecha).

2. **Tabla de programación dinámica**: La estructura binaria permite construir la tabla P[i][j] combinando resultados de P[i][k] y P[k+1][j].

3. **Eliminación de ambigüedad**: CNF elimina producciones epsilon y unitarias que complicarían el algoritmo.

---

## 🔄 Proceso de Conversión a CNF

El programa aplica **automáticamente** estos 4 pasos:

### Paso 1: Eliminación de Producciones ε
- Identifica símbolos anulables (que pueden derivar en ε)
- Genera todas las variantes de producciones eliminando símbolos anulables
- Ejemplo: `A → BC` donde B es anulable → añadir `A → C`

### Paso 2: Eliminación de Producciones Unitarias
- Elimina reglas de la forma `A → B` (un no-terminal a otro)
- Las reemplaza por las producciones de B
- Calcula el cierre transitivo de producciones unitarias

### Paso 3: Eliminación de Símbolos Inútiles
- Elimina no-terminales que no generan cadenas de terminales
- Elimina símbolos no alcanzables desde el símbolo inicial

### Paso 4: Conversión a Forma CNF Estricta
- Crea no-terminales auxiliares para terminales (ej: `Ti → i`)
- Descompone producciones largas usando variables auxiliares:
  ```
  A → B1 B2 B3 B4  se convierte en:
  A → B1 X1
  X1 → B2 X2
  X2 → B3 B4
  ```

---

## 🧮 Algoritmo CYK con Programación Dinámica

### Principio de Programación Dinámica

El algoritmo CYK usa **programación dinámica** para evitar recalcular subproblemas:

1. **Subproblemas**: P[i][j] = conjunto de no-terminales que pueden generar w[i..j]

2. **Caso Base**: P[i][i] = {A | A → w[i]} (palabras individuales)

3. **Recurrencia**:
   ```
   P[i][j] = {A | existe k tal que B ∈ P[i][k], C ∈ P[k+1][j], y A → BC}
   ```

4. **Memoización**: Los resultados se almacenan en la tabla P para no recalcularlos.

### Complejidad Temporal

- **Tiempo**: O(n³ · |G|)
  - 3 bucles anidados: longitud L, posición inicial i, punto de división k
  - |G| = tamaño de la gramática (número de reglas)

- **Espacio**: O(n² · |G|)
  - Tabla P[n][n] donde cada celda puede contener múltiples no-terminales

### Interpretación de la Tabla CYK

La tabla `P[i][j]` es una **matriz triangular superior** donde:

- **P[i][j]**: Conjunto de no-terminales que pueden generar la subcadena `w[i..j]`
- **Diagonal (i=j)**: Palabras individuales (caso base)
- **P[0][n-1]**: Si contiene el símbolo inicial S, la oración es aceptada

**Ejemplo**: Para "she eats a cake with a fork":
```
P[0]: [{'NP'}, {'S'}, set(), {'S'}, set(), set(), {'S'}]
      └─────┘  └───┘                              └───┘
      w[0:0]  w[0:1]                            w[0:6]
      "she"   "she eats"                   oración completa
```

- `P[0][0] = {'NP'}`: "she" es un NP
- `P[0][1] = {'S'}`: "she eats" forma una oración completa (S)
- `P[0][6] = {'S'}`: La oración completa es válida ✓

### Pseudocódigo

```
CYK(w[1..n], G):
  // Caso base: palabras individuales
  for i = 1 to n:
    P[i][i] = {A | A → w[i] ∈ G}
  
  // Inducción: subcadenas de longitud L
  for L = 2 to n:
    for i = 1 to n - L + 1:
      j = i + L - 1
      for k = i to j - 1:
        for each B ∈ P[i][k]:
          for each C ∈ P[k+1][j]:
            for each A → BC ∈ G:
              P[i][j] = P[i][j] ∪ {A}
  
  return S ∈ P[1][n]  // ¿El símbolo inicial genera toda la cadena?
```

---

## 🚀 Uso del Programa

### Opción 1: Menú Interactivo

```bash
python Proyecto2.py
```

Seleccione la opción 2 para validar oraciones con CYK.

**Modo de depuración**: El programa preguntará si desea ver detalles adicionales:
- Gramática CNF generada (formato de lista de producciones)
- Tabla de parseo CYK completa (matriz P[i][j])

### Opción 2: Script de Prueba

```bash
python test_cyk.py        # Ejemplos sin depuración
python test_cyk_debug.py  # Con depuración completa
```

Este script ejecuta ejemplos de oraciones **válidas** e **inválidas** automáticamente.

---

## 📝 Ejemplos

### Oraciones VÁLIDAS (sintácticamente correctas)

✅ **"she eats"**
- Derivación: S → NP VP → she eats
- Parse tree: `(S (NP 'she') (VP 'eats'))`

✅ **"he drinks the beer"**
- Derivación: S → NP VP → he (V NP) → he drinks (Det N)
- Parse tree: `(S (NP 'he') (VP (V 'drinks') (NP (Det 'the') (N 'beer'))))`

✅ **"she cooks the soup with a spoon"**
- Con preposición (PP)
- Parse tree muestra estructura completa con VP → VP PP

### Oraciones INVÁLIDAS (sintácticamente incorrectas)

❌ **"eats she"** - Orden incorrecto (verbo antes del sujeto)

❌ **"the beer drinks"** - Falta el sujeto

❌ **"she the eats cake"** - Determinante mal ubicado

---

## 📊 Salida del Programa

```
======================================================================
  RESULTADO DE LA VALIDACIÓN
======================================================================

Oración analizada: "she eats a cake with a fork"

¿Pertenece al lenguaje? SÍ ✓
Tiempo de ejecución: 12.45 ms

----------------------------------------------------------------------
  ÁRBOL DE PARSEO (Parse Tree)
----------------------------------------------------------------------
(S (NP 'she') (VP (VP (V 'eats') (NP (Det 'a') (N 'cake'))) 
               (PP (P 'with') (NP (Det 'a') (N 'fork')))))
----------------------------------------------------------------------
```

---

## 🔍 Validación de Requisitos

### ✅ Conversión a CNF
- El programa convierte **automáticamente** la gramática a CNF antes de ejecutar CYK
- Se aplican los 4 pasos de conversión (ε, unitarias, inútiles, CNF)
- El usuario no necesita proporcionar la gramática en CNF

### ✅ Programación Dinámica
- Implementado con tabla P[i][j] de memoización
- Evita recalcular subproblemas
- Complejidad O(n³ · |G|) garantizada

### ✅ Salida Completa
- **SÍ/NO**: Indica si la oración pertenece al lenguaje
- **Tiempo**: Medido en milisegundos con `time.perf_counter()`
- **Parse Tree**: Árbol sintáctico completo en formato bracket

### ✅ Validación Sintáctica
- Las oraciones aceptadas son **sintácticamente correctas**
- No se garantiza corrección semántica (ej: "the fork drinks the soup" puede ser sintácticamente válido pero semánticamente absurdo)

---

## 📁 Archivos del Proyecto

- **Proyecto2.py**: Programa principal con menú interactivo
- **test_cyk.py**: Script de prueba con ejemplos automáticos
- **gramatica_english.txt**: Gramática en inglés (será convertida a CNF automáticamente)
- **README_CYK.md**: Este documento

---

## 🎓 Referencias

- **Algoritmo CYK**: J. Cocke, D. Younger, T. Kasami (1965)
- **Forma Normal de Chomsky**: Noam Chomsky (1959)
- **Complejidad**: Análisis basado en estructura de bucles y tamaño de gramática

---

## 👥 Autores

Proyecto 2 - Curso de Teoría de la Computación
Universidad del Valle de Guatemala (UVG)

---

**Nota Importante**: Este programa convierte **cualquier** gramática libre de contexto a CNF automáticamente. No es necesario que el usuario proporcione la gramática ya en CNF.
