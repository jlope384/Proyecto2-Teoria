# Procesador de Gramáticas Libres de Contexto

## Descripción

Este programa procesa gramáticas libres de contexto con dos funcionalidades principales:
1. **Conversión a Forma Normal de Chomsky (CNF)** - Prepara gramáticas para el algoritmo CYK
2. **Generador de Oraciones en Inglés** - Genera oraciones a partir de una gramática

## Características

El programa realiza los siguientes pasos automáticamente:

1. **Eliminación de producciones ε (epsilon)**: Elimina todas las producciones vacías manteniendo el lenguaje.
2. **Eliminación de producciones unitarias**: Elimina producciones de la forma A → B.
3. **Eliminación de símbolos inútiles**: Elimina símbolos que no generan terminales o no son alcanzables.
4. **Conversión a CNF**: Convierte todas las producciones a la forma estándar:
   - A → a (terminal)
   - A → BC (dos no-terminales)

## Formato de entrada

Los archivos de gramática deben seguir este formato:

```
S -> AB | a
A -> aA | ε
B -> bB | b
```

Características del formato:
- Una línea por no-terminal
- Símbolo no-terminal: una letra mayúscula (A-Z)
- Producciones separadas por `|`
- Los espacios entre símbolos se eliminan automáticamente
- `ε`, `e`, o `eps` se interpretan como epsilon (cadena vacía)

## Uso

### Ejecutar el programa:

```powershell
python Ejercicio2.py
```

### Menú Principal:

El programa mostrará un menú con 3 opciones:

```
======================================================================
  PROCESADOR DE GRAMÁTICAS LIBRES DE CONTEXTO
======================================================================

¿Qué desea hacer?

  1. Convertir gramática a Forma Normal de Chomsky (CNF)
  2. Generar oraciones en inglés desde gramática
  3. Salir
```

### Opción 1: Convertir a CNF

1. Selecciona esta opción
2. Elige el archivo de gramática:
   - Archivo `1.txt`
   - Archivo `1-cnf.txt`
   - Especificar otra ruta
3. El programa mostrará:
   - Gramática original
   - Trazas detalladas de cada paso
   - Gramática resultante después de cada transformación
   - Gramática final en CNF

### Opción 2: Generar Oraciones

1. Selecciona esta opción
2. El programa automáticamente:
   - Carga `gramatica_english.txt`
   - Muestra información de la gramática
   - Genera 3 oraciones en inglés con sus derivaciones:
     - "she eats"
     - "he drinks the beer"
     - "she cooks the soup with a spoon"

## Archivos incluidos

- `Ejercicio2.py`: Programa principal
- `1.txt`: Gramática de ejemplo (expresiones aritméticas)
- `1-cnf.txt`: Gramática ya en CNF de ejemplo
- `gramatica.txt`: Otro ejemplo de gramática

## Ejemplo de ejecución

```
============================================================
  CONVERSIÓN DE GRAMÁTICA A FORMA NORMAL DE CHOMSKY (CNF)
============================================================

Seleccione el archivo de gramática a procesar:

  1. Archivo 1.txt
  2. Archivo 1-cnf.txt
  3. Otro archivo (especificar ruta)

============================================================

Ingrese su opción (1, 2, o 3): 1

=== Gramática original (leída de '1.txt') ===
E -> TX
F -> (E) | id
T -> FY
X -> +TX | ε
Y -> *FY | ε
====================

[... proceso de conversión con trazas detalladas ...]

=== Gramática en Forma Normal de Chomsky ===
E -> FY | TX
F -> LX4 | TiTd
L -> (
M -> *
P -> +
R -> )
T -> FY | LX2 | TiTd
...
====================
```

## Notas técnicas

- Todos los símbolos terminales especiales (`+`, `*`, `(`, `)`, etc.) se convierten automáticamente a no-terminales en el paso de conversión a CNF.
- El programa genera variables auxiliares (`X1`, `X2`, etc.) para descomponer producciones con más de dos símbolos.
- Se muestran trazas detalladas de cada paso para comprender el proceso de transformación.
