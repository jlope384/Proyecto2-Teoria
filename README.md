# Procesador de Gramáticas Libres de Contexto y Algoritmo CYK

## 📋 Descripción

Este programa implementa un procesador completo de gramáticas libres de contexto con tres funcionalidades principales:

1. **Conversión a Forma Normal de Chomsky (CNF)** - Transforma cualquier gramática a formato CNF
2. **Validador de Oraciones con Algoritmo CYK** - Verifica si oraciones pertenecen al lenguaje usando programación dinámica
3. **Generador de Oraciones en Inglés** - Genera ejemplos de oraciones válidas desde una gramática

## 🎯 Características Principales

### ✅ Algoritmo CYK con Programación Dinámica
- **Validación sintáctica** de oraciones en inglés
- **Tabla de memoización** P[i][j] para optimización
- **Complejidad O(n³·|G|)** garantizada
- **Construcción de árbol de parseo** (parse tree) completo
- **Medición de tiempo** en milisegundos
- **Modo de depuración** con visualización de gramática CNF y tabla CYK

### ✅ Conversión a Forma Normal de Chomsky (CNF)

El programa aplica automáticamente estos 4 pasos:

1. **Eliminación de producciones ε (epsilon)**: Elimina todas las producciones vacías manteniendo el lenguaje
2. **Eliminación de producciones unitarias**: Elimina producciones de la forma A → B
3. **Eliminación de símbolos inútiles**: Elimina símbolos que no generan terminales o no son alcanzables
4. **Conversión a CNF estricta**: Convierte todas las producciones a la forma:
   - A → a (un terminal)
   - A → BC (dos no-terminales)

Cada paso muestra **trazas detalladas** del proceso de transformación.

### ✅ Validador CYK (Cocke-Younger-Kasami)

**¿Qué hace?**
- Verifica si una oración en inglés pertenece al lenguaje definido por la gramática
- Utiliza **programación dinámica** para optimización
- Construye un **árbol de parseo** si la oración es válida

**Salida del algoritmo:**
- ✅ **SÍ/NO**: Indica si la oración es sintácticamente correcta
- ⏱️ **Tiempo**: Medición en milisegundos
- 🌲 **Parse Tree**: Árbol sintáctico en formato bracket notation

**Modo de depuración:**
- Visualización de la **gramática CNF** generada
- **Tabla de parseo CYK** completa (matriz P[i][j])
- Tokens de la oración analizada

### ✅ Generador de Oraciones

Genera ejemplos de oraciones válidas en inglés con sus derivaciones completas:
- "she eats"
- "he drinks the beer"
- "she cooks the soup with a spoon"

## 📝 Formato de Entrada

### Archivos de Gramática

Los archivos deben seguir este formato:

```
S -> NP VP
VP -> VP PP | V NP | cooks | drinks | eats
PP -> P NP
NP -> Det N | he | she
V -> cooks | drinks | eats
P -> in | with
N -> cat | dog | beer | cake | soup | fork | knife
Det -> a | the
```

**Características del formato:**
- Una línea por no-terminal
- No-terminal: letra(s) mayúscula(s) (S, NP, VP, Det, etc.)
- Producciones separadas por `|`
- Terminales: palabras en minúsculas o símbolos
- Espacios entre tokens permitidos (se procesan correctamente)
- `ε`, `e`, o `eps` se interpretan como epsilon (cadena vacía)

## 🚀 Uso del Programa

### Ejecutar el programa principal:

```powershell
python Proyecto2.py
```

### Menú Principal:

```
======================================================================
  PROCESADOR DE GRAMÁTICAS LIBRES DE CONTEXTO
======================================================================

¿Qué desea hacer?

  1. Convertir gramática a Forma Normal de Chomsky (CNF)
  2. Validar oración en inglés (CYK con programación dinámica)
  3. Generar oraciones en inglés (demo)
  4. Salir

======================================================================
```

---

## 📖 Guía de Opciones

### Opción 1: Convertir Gramática a CNF

**Uso:**
1. Selecciona opción `1`
2. El programa usa el archivo `gramatica_english.txt` automáticamente
3. El programa mostrará:
   - ✅ Gramática original
   - 📋 Trazas detalladas de cada paso de conversión
   - 📊 Gramática resultante después de cada transformación
   - ✨ Gramática final en Forma Normal de Chomsky

**Ejemplo de salida:**
```
=== Gramática original ===
S -> NP VP
VP -> VP PP | V NP | cooks | drinks
...

########### Paso 1: Eliminación de ε ############
[Trazas detalladas...]

########### Paso 2: Eliminación de producciones unitarias ############
[Trazas detalladas...]

########### Paso 3: Eliminación de símbolos inútiles ############
[Trazas detalladas...]

########### Paso 4: Conversión a Forma Normal de Chomsky ############
[Trazas detalladas...]

=== Gramática en Forma Normal de Chomsky ===
S -> NP VP
VP -> VP PP | V NP
V -> Tcooks | Tdrinks | Teats
Tcooks -> cooks
...
```

---

### Opción 2: Validar Oración con CYK

**Uso:**
1. Selecciona opción `2`
2. Ingresa una oración en inglés (ejemplo: "she eats a cake with a fork")
3. El programa mostrará los resultados de validación

**Salida:**
```
======================================================================
  RESULTADO DE LA VALIDACIÓN
======================================================================

Oración analizada: "she eats a cake with a fork"

¿Pertenece al lenguaje? SÍ ✓
Tiempo de ejecución: 1.27 ms

----------------------------------------------------------------------
  ÁRBOL DE PARSEO (Parse Tree)
----------------------------------------------------------------------
(S (NP 'she') (VP (VP (V 'eats') (NP (Det 'a') (N 'cake'))) 
               (PP (P 'with') (NP (Det 'a') (N 'fork')))))
----------------------------------------------------------------------
```

**Ejemplos de oraciones válidas:**
- ✅ "she eats"
- ✅ "he drinks the beer"
- ✅ "she cooks the soup with a spoon"
- ✅ "the cat eats the cake"
- ✅ "he cuts the meat with a knife"

**Ejemplos de oraciones inválidas:**
- ❌ "eats she" (orden incorrecto)
- ❌ "she the eats cake" (determinante mal ubicado)
- ❌ "he she drinks" (doble sujeto)

---

### Opción 3: Generar Oraciones (Demo)

**Uso:**
1. Selecciona opción `3`
2. El programa generará automáticamente 3 oraciones de ejemplo con sus derivaciones completas

**Salida:**
```
======================================================================
  GENERADOR DE ORACIONES EN INGLÉS
======================================================================

Oración 1:
----------------------------------------------------------------------
Derivación:
  S → NP VP
  NP → she
  VP → eats

✓ Oración generada: "she eats"
======================================================================

[Más ejemplos...]
```

---

## 📊 Algoritmo CYK: Detalles Técnicos

### Programación Dinámica

El algoritmo CYK implementa **programación dinámica** de la siguiente manera:

**Tabla de memoización:**
- `P[i][j]` = conjunto de no-terminales que pueden generar la subcadena `w[i..j]`

**Principio:**
1. **Subproblemas**: Dividir el problema en subcadenas más pequeñas
2. **Recurrencia**: `P[i][j]` se calcula combinando `P[i][k]` y `P[k+1][j]`
3. **Memoización**: Guardar resultados para evitar recálculos

**Complejidad:**
- ⏱️ **Tiempo**: O(n³ · |G|) donde n = longitud de la oración
- 💾 **Espacio**: O(n² · |G|)

### Interpretación de la Tabla CYK

```
P[0]: [{'NP'}, {'S'}, set(), {'S'}, ...]
      └─────┘  └───┘              └───┘
      w[0:0]  w[0:1]          w[0:n-1]
      "she"   "she eats"   oración completa
```

- **P[0][0]**: Palabra individual "she" es un NP
- **P[0][1]**: "she eats" forma una oración completa (S)
- **P[0][n-1]**: Si contiene S, la oración completa es válida ✓

---

## 📁 Archivos del Proyecto

- **`Proyecto2.py`**: Programa principal con menú interactivo (929 líneas)
- **`gramatica_english.txt`**: Gramática en inglés usada por el programa
- **`README.md`**: Este archivo - Documentación completa del proyecto

---

## 🎓 Conceptos Teóricos

### Forma Normal de Chomsky (CNF)

Una gramática está en **CNF** si todas sus producciones tienen una de estas formas:
- **A → a** (terminal)
- **A → BC** (dos no-terminales)
- **S → ε** (solo para el símbolo inicial, si acepta cadena vacía)

**¿Por qué es importante?**
- Requerida por el algoritmo CYK
- Simplifica el análisis sintáctico
- Permite división binaria del problema

### Algoritmo CYK

**Cocke-Younger-Kasami (CYK)** es un algoritmo de **análisis sintáctico ascendente** que:
- Determina si una cadena pertenece a un lenguaje libre de contexto
- Construye el árbol de parseo si la cadena es válida
- Usa programación dinámica para optimización

**Ventajas:**
- ✅ Complejidad polinómica garantizada O(n³)
- ✅ Funciona para cualquier gramática en CNF
- ✅ Encuentra todas las derivaciones posibles

**Limitación:**
- ⚠️ Requiere que la gramática esté en CNF

---

## 💡 Ejemplo Completo de Ejecución

### Escenario: Validar "she eats a cake"

**Paso 1: Ejecutar programa**
```powershell
python Proyecto2.py
```

**Paso 2: Seleccionar opción 2**
```
Ingrese su opción (1, 2, 3 o 4): 2
```

**Paso 3: Ingresar oración**
```
Ingrese una oración en inglés: she eats a cake
```

**Paso 4: Ver resultado**
```
======================================================================
  RESULTADO DE LA VALIDACIÓN
======================================================================

Oración analizada: "she eats a cake"

¿Pertenece al lenguaje? SÍ ✓
Tiempo de ejecución: 0.85 ms

----------------------------------------------------------------------
  ÁRBOL DE PARSEO (Parse Tree)
----------------------------------------------------------------------
(S (NP 'she') (VP (V 'eats') (NP (Det 'a') (N 'cake'))))
----------------------------------------------------------------------
```

**Interpretación del árbol:**
```
         S
        / \
      NP   VP
      |    / \
    'she' V   NP
          |   / \
       'eats' Det N
              |   |
             'a' 'cake'
```

---

## 🔧 Requisitos Técnicos

- **Python**: 3.8 o superior
- **Módulos estándar**: `re`, `sys`, `time`, `typing`, `itertools`
- **Sistema operativo**: Windows, Linux, macOS

### Instalación

No se requieren dependencias externas. Solo Python estándar.

```powershell
# Clonar el repositorio
git clone https://github.com/jlope384/Proyecto2-Teoria.git

# Navegar al directorio
cd Proyecto2-Teoria

# Ejecutar el programa
python Proyecto2.py
```

---

## 🐛 Solución de Problemas

### Error: "No se encontró el archivo 'gramatica_english.txt'"

**Solución:** Asegúrate de que el archivo esté en el mismo directorio que `Proyecto2.py`

### Error: "UnicodeEncodeError" en Windows

**Solución:** El programa usa codificación UTF-8. Si ves caracteres extraños, ejecuta:
```powershell
chcp 65001
python Proyecto2.py
```

### La oración válida es rechazada

**Posibles causas:**
1. Falta vocabulario en la gramática (añadir palabras a `gramatica_english.txt`)
2. Estructura no soportada por la gramática (verificar reglas)
3. Puntuación no eliminada correctamente (el programa remueve `.`, `,`, `!`, `?` automáticamente)

---

## 📚 Referencias

- **Algoritmo CYK**: J. Cocke, D. Younger, T. Kasami (1965)
- **Forma Normal de Chomsky**: Noam Chomsky (1959)
- **Teoría de Lenguajes Formales**: Hopcroft, Motwani, Ullman

---

## 👥 Autores

**Proyecto 2 - Teoría de la Computación**  
Universidad del Valle de Guatemala (UVG)  
2025

---

## 📄 Licencia

Este proyecto es material académico para el curso de Teoría de la Computación.

---

## 📞 Soporte

Para más información sobre el código fuente:
- **Comentarios en el código**: Explicaciones detalladas en `Proyecto2.py`
- **Modo de depuración**: Activa `debug=True` en la función `cyk_validate()`

---

## ✨ Características Destacadas

- 🚀 **Conversión automática a CNF** - No necesitas preparar la gramática manualmente
- 🧮 **Programación dinámica** - Optimización garantizada con memoización
- 🌲 **Árboles de parseo** - Visualización completa de la estructura sintáctica
- ⏱️ **Medición de rendimiento** - Tiempo de ejecución en milisegundos
- 🔍 **Modo de depuración** - Visualiza tablas CYK y gramáticas CNF (en código)
- 📊 **Trazas detalladas** - Comprende cada paso del proceso de conversión
- ✅ **Validación completa** - Verifica sintaxis de oraciones en inglés

---

**¡Gracias por usar el Procesador de Gramáticas Libres de Contexto!** 🎉

## 📝 Formato de Entrada

### Archivos de Gramática

Los archivos deben seguir este formato:

```
S -> NP VP
VP -> VP PP | V NP | cooks | drinks | eats
PP -> P NP
NP -> Det N | he | she
V -> cooks | drinks | eats
P -> in | with
N -> cat | dog | beer | cake | soup | fork | knife
Det -> a | the
```

**Características del formato:**
- Una línea por no-terminal
- No-terminal: letra(s) mayúscula(s) (S, NP, VP, Det, etc.)
- Producciones separadas por `|`
- Terminales: palabras en minúsculas o símbolos
- Espacios entre tokens permitidos (se procesan correctamente)
- `ε`, `e`, o `eps` se interpretan como epsilon (cadena vacía)

## 🚀 Uso del Programa

### Ejecutar el programa principal:

```powershell
python Proyecto2.py
```

### Menú Principal:

```
======================================================================
  PROCESADOR DE GRAMÁTICAS LIBRES DE CONTEXTO
======================================================================

¿Qué desea hacer?

  1. Convertir gramática a Forma Normal de Chomsky (CNF)
  2. Validar oración en inglés (CYK con programación dinámica)
  3. Generar oraciones en inglés (demo)
  4. Salir

======================================================================
```

---

## 📖 Guía de Opciones

### Opción 1: Convertir Gramática a CNF

**Uso:**
1. Selecciona opción `1`
2. Usa el archivo predeterminado `gramatica_english.txt`
3. El programa mostrará:
   - ✅ Gramática original
   - 📋 Trazas detalladas de cada paso de conversión
   - 📊 Gramática resultante después de cada transformación
   - ✨ Gramática final en Forma Normal de Chomsky

**Ejemplo de salida:**
```
=== Gramática original ===
S -> NP VP
VP -> VP PP | V NP | cooks | drinks
...

########### Paso 1: Eliminación de ε ############
[Trazas detalladas...]

########### Paso 2: Eliminación de producciones unitarias ############
[Trazas detalladas...]

########### Paso 3: Eliminación de símbolos inútiles ############
[Trazas detalladas...]

########### Paso 4: Conversión a Forma Normal de Chomsky ############
[Trazas detalladas...]

=== Gramática en Forma Normal de Chomsky ===
S -> NP VP
VP -> VP PP | V NP
V -> Tcooks | Tdrinks | Teats
Tcooks -> cooks
...
```

---

### Opción 2: Validar Oración con CYK

**Uso:**
1. Selecciona opción `2`
2. Ingresa una oración en inglés (ejemplo: "she eats a cake with a fork")
3. Opcionalmente, activa el modo de depuración para ver:
   - Gramática CNF generada
   - Tabla de parseo CYK completa

**Salida:**
```
======================================================================
  RESULTADO DE LA VALIDACIÓN
======================================================================

Oración analizada: "she eats a cake with a fork"

¿Pertenece al lenguaje? SÍ ✓
Tiempo de ejecución: 1.27 ms

----------------------------------------------------------------------
  ÁRBOL DE PARSEO (Parse Tree)
----------------------------------------------------------------------
(S (NP 'she') (VP (VP (V 'eats') (NP (Det 'a') (N 'cake'))) 
               (PP (P 'with') (NP (Det 'a') (N 'fork')))))
----------------------------------------------------------------------
```

**Modo de depuración (opcional):**
```
======================================================================
  GRAMÁTICA CNF GENERADA
======================================================================
S -> [['NP', 'VP']]
VP -> [['VP', 'PP'], ['V', 'NP'], ['cooks'], ['drinks'], ['eats']]
NP -> [['Det', 'N'], ['he'], ['she']]
...

======================================================================
  TABLA DE PARSEO CYK
======================================================================
Oración tokenizada: ['she', 'eats', 'a', 'cake', 'with', 'a', 'fork']

P[0]: [{'NP'}, {'S'}, set(), {'S'}, set(), set(), {'S'}]
P[1]: [{'VP', 'V'}, set(), {'VP'}, set(), set(), {'VP'}]
P[2]: [{'Det'}, {'NP'}, set(), set(), set()]
P[3]: [{'N'}, set(), set(), set()]
P[4]: [{'P'}, set(), {'PP'}]
P[5]: [{'Det'}, {'NP'}]
P[6]: [{'N'}]
```

**Ejemplos de oraciones válidas:**
- ✅ "she eats"
- ✅ "he drinks the beer"
- ✅ "she cooks the soup with a spoon"
- ✅ "the cat eats the cake"
- ✅ "he cuts the meat with a knife"

**Ejemplos de oraciones inválidas:**
- ❌ "eats she" (orden incorrecto)
- ❌ "she the eats cake" (determinante mal ubicado)
- ❌ "he she drinks" (doble sujeto)

---

### Opción 3: Generar Oraciones (Demo)

**Uso:**
1. Selecciona opción `3`
2. El programa generará automáticamente 3 oraciones de ejemplo con sus derivaciones completas

**Salida:**
```
======================================================================
  GENERADOR DE ORACIONES EN INGLÉS
======================================================================

Oración 1:
----------------------------------------------------------------------
Derivación:
  S → NP VP
  NP → she
  VP → eats

✓ Oración generada: "she eats"
======================================================================

[Más ejemplos...]
```

---

## 🧪 Scripts de Prueba

### test_cyk.py - Pruebas sin depuración

Ejecuta validación de múltiples oraciones (válidas e inválidas):

```powershell
python test_cyk.py
```

### test_cyk_debug.py - Pruebas con depuración completa

Ejecuta validación mostrando gramática CNF y tabla CYK:

```powershell
python test_cyk_debug.py
```

---

## 📊 Algoritmo CYK: Detalles Técnicos

### Programación Dinámica

El algoritmo CYK implementa **programación dinámica** de la siguiente manera:

**Tabla de memoización:**
- `P[i][j]` = conjunto de no-terminales que pueden generar la subcadena `w[i..j]`

**Principio:**
1. **Subproblemas**: Dividir el problema en subcadenas más pequeñas
2. **Recurrencia**: `P[i][j]` se calcula combinando `P[i][k]` y `P[k+1][j]`
3. **Memoización**: Guardar resultados para evitar recálculos

**Complejidad:**
- ⏱️ **Tiempo**: O(n³ · |G|) donde n = longitud de la oración
- 💾 **Espacio**: O(n² · |G|)

### Interpretación de la Tabla CYK

```
P[0]: [{'NP'}, {'S'}, set(), {'S'}, ...]
      └─────┘  └───┘              └───┘
      w[0:0]  w[0:1]          w[0:n-1]
      "she"   "she eats"   oración completa
```

- **P[0][0]**: Palabra individual "she" es un NP
- **P[0][1]**: "she eats" forma una oración completa (S)
- **P[0][n-1]**: Si contiene S, la oración completa es válida ✓

---

## 📁 Archivos del Proyecto

- **`Proyecto2.py`**: Programa principal con menú interactivo (929 líneas)
- **`test_cyk.py`**: Script de pruebas automáticas (sin depuración)
- **`test_cyk_debug.py`**: Script con depuración completa (muestra tabla CYK)
- **`gramatica_english.txt`**: Gramática en inglés (archivo principal usado por el programa)
- **`README.md`**: Este archivo - Documentación completa del proyecto
- **`README_CYK.md`**: Documentación técnica detallada del algoritmo CYK
- **`QUICKSTART.md`**: Guía rápida de inicio en 3 pasos

---

---

## 🎓 Conceptos Teóricos

### Forma Normal de Chomsky (CNF)

Una gramática está en **CNF** si todas sus producciones tienen una de estas formas:
- **A → a** (terminal)
- **A → BC** (dos no-terminales)
- **S → ε** (solo para el símbolo inicial, si acepta cadena vacía)

**¿Por qué es importante?**
- Requerida por el algoritmo CYK
- Simplifica el análisis sintáctico
- Permite división binaria del problema

### Algoritmo CYK

**Cocke-Younger-Kasami (CYK)** es un algoritmo de **análisis sintáctico ascendente** que:
- Determina si una cadena pertenece a un lenguaje libre de contexto
- Construye el árbol de parseo si la cadena es válida
- Usa programación dinámica para optimización

**Ventajas:**
- ✅ Complejidad polinómica garantizada O(n³)
- ✅ Funciona para cualquier gramática en CNF
- ✅ Encuentra todas las derivaciones posibles

**Limitación:**
- ⚠️ Requiere que la gramática esté en CNF

---

## 💡 Ejemplo Completo de Ejecución

### Escenario: Validar "she eats a cake"

**Paso 1: Ejecutar programa**
```powershell
python Proyecto2.py
```

**Paso 2: Seleccionar opción 2**
```
Ingrese su opción (1, 2, 3 o 4): 2
```

**Paso 3: Ingresar oración**
```
Ingrese una oración en inglés: she eats a cake
```

**Paso 4: Ver resultado**
```
======================================================================
  RESULTADO DE LA VALIDACIÓN
======================================================================

Oración analizada: "she eats a cake"

¿Pertenece al lenguaje? SÍ ✓
Tiempo de ejecución: 0.85 ms

----------------------------------------------------------------------
  ÁRBOL DE PARSEO (Parse Tree)
----------------------------------------------------------------------
(S (NP 'she') (VP (V 'eats') (NP (Det 'a') (N 'cake'))))
----------------------------------------------------------------------
```

**Interpretación del árbol:**
```
         S
        / \
      NP   VP
      |    / \
    'she' V   NP
          |   / \
       'eats' Det N
              |   |
             'a' 'cake'
```

---

## 🔧 Requisitos Técnicos

- **Python**: 3.8 o superior
- **Módulos estándar**: `re`, `sys`, `time`, `typing`, `itertools`
- **Sistema operativo**: Windows, Linux, macOS

### Instalación

No se requieren dependencias externas. Solo Python estándar.

```powershell
# Clonar el repositorio
git clone https://github.com/jlope384/Proyecto2-Teoria.git

# Navegar al directorio
cd Proyecto2-Teoria

# Ejecutar el programa
python Proyecto2.py
```

---

## 🐛 Solución de Problemas

### Error: "No se encontró el archivo 'gramatica_english.txt'"

**Solución:** Asegúrate de que el archivo esté en el mismo directorio que `Proyecto2.py`

### Error: "UnicodeEncodeError" en Windows

**Solución:** El programa usa codificación UTF-8. Si ves caracteres extraños, ejecuta:
```powershell
chcp 65001
python Proyecto2.py
```

### La oración válida es rechazada

**Posibles causas:**
1. Falta vocabulario en la gramática (añadir palabras a `gramatica_english.txt`)
2. Estructura no soportada por la gramática (verificar reglas)
3. Puntuación no eliminada correctamente (el programa remueve `.`, `,`, `!`, `?` automáticamente)

---

## 📚 Referencias

- **Algoritmo CYK**: J. Cocke, D. Younger, T. Kasami (1965)
- **Forma Normal de Chomsky**: Noam Chomsky (1959)
- **Teoría de Lenguajes Formales**: Hopcroft, Motwani, Ullman

---

## 👥 Autores

**Proyecto 2 - Teoría de la Computación**  
Universidad del Valle de Guatemala (UVG)  
2025

---

## 📄 Licencia

Este proyecto es material académico para el curso de Teoría de la Computación.

---

## 📞 Soporte

Para más información técnica sobre el algoritmo CYK, consulta:
- **`README_CYK.md`**: Documentación técnica detallada
- **Comentarios en el código**: Explicaciones línea por línea en `Proyecto2.py`

---

## ✨ Características Destacadas

- 🚀 **Conversión automática a CNF** - No necesitas preparar la gramática manualmente
- 🧮 **Programación dinámica** - Optimización garantizada con memoización
- 🌲 **Árboles de parseo** - Visualización completa de la estructura sintáctica
- ⏱️ **Medición de rendimiento** - Tiempo de ejecución en milisegundos
- 🔍 **Modo de depuración** - Visualiza tablas CYK y gramáticas CNF
- 📊 **Trazas detalladas** - Comprende cada paso del proceso de conversión
- ✅ **Validación completa** - Verifica sintaxis de oraciones en inglés

---

**¡Gracias por usar el Procesador de Gramáticas Libres de Contexto!** 🎉
