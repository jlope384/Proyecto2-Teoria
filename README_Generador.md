# Generador de Oraciones en Inglés

## Descripción

Este programa genera oraciones en inglés a partir de una gramática libre de contexto. Utiliza el símbolo inicial `S` (oración) para expandir recursivamente las producciones y generar oraciones gramaticalmente correctas según las reglas definidas.

## Características

- **Carga gramática**: Lee un archivo de gramática con formato simple
- **Genera oraciones específicas**: Muestra 3 oraciones de ejemplo con sus derivaciones completas
- **Generación aleatoria**: Opción para generar oraciones aleatorias adicionales
- **Muestra derivaciones**: Presenta paso a paso cómo se genera cada oración

## Gramática incluida

La gramática modela oraciones simples en inglés con la siguiente estructura:

```
S → NP VP                    (Oración = Frase Nominal + Frase Verbal)
VP → VP PP | V NP | ...      (Frase Verbal)
PP → P NP                     (Frase Preposicional)
NP → Det N | he | she        (Frase Nominal)
V → cooks | drinks | eats | cuts
P → in | with
N → cat | dog | beer | cake | juice | meat | soup | fork | knife | oven | spoon
Det → a | the
```

### Ejemplos de oraciones generadas:

1. **"she eats"** (oración simple)
2. **"he drinks the beer"** (con objeto directo)
3. **"she cooks the soup with a spoon"** (con frase preposicional)

## Formato del archivo de gramática

El archivo `gramatica_english.txt` usa el siguiente formato:

```
S -> NP VP
VP -> VP PP | V NP | cooks
NP -> Det N | he | she
Det -> a | the
N -> cat | dog | beer
```

Características:
- Una línea por no-terminal (pueden haber múltiples líneas para el mismo no-terminal)
- Usa `->` o `→` como separador
- Producciones múltiples separadas por `|`
- Espacios entre símbolos en las producciones

## Uso

### Ejecutar el programa:

```powershell
python GeneradorOraciones.py
```

### Flujo del programa:

1. **Carga la gramática** desde `gramatica_english.txt`
2. **Muestra información** sobre la gramática (terminales, no-terminales, producciones)
3. **Genera 3 oraciones de ejemplo** con derivaciones detalladas
4. **Pregunta** si deseas generar oraciones aleatorias adicionales
5. Si aceptas, pregunta cuántas oraciones generar

### Ejemplo de ejecución:

```
======================================================================
  GENERADOR DE ORACIONES EN INGLÉS A PARTIR DE GRAMÁTICA
======================================================================

======================================================================
  GRAMÁTICA CARGADA
======================================================================

Símbolo inicial: S

No-terminales (8): Det, N, NP, P, PP, S, V, VP

Terminales (21): a, beer, cake, cat, cooks, cuts, dog, drinks, eats...

Producciones:
  Det → a | the
  N → cat | dog | beer | cake | juice | meat | soup | fork | knife...
  NP → Det N | he | she
  ...

======================================================================
  ORACIONES GENERADAS
======================================================================

Generando 3 oraciones de ejemplo:

======================================================================
Oración 1:
----------------------------------------------------------------------
Derivación:
  S → NP VP
  NP → she
  VP → eats

✓ Oración generada: "she eats"
======================================================================

[... más oraciones ...]

======================================================================
  RESUMEN DE ORACIONES GENERADAS
======================================================================

1. "she eats"
2. "he drinks the beer"
3. "she cooks the soup with a spoon"

======================================================================

¿Desea generar oraciones aleatorias adicionales? (s/n): s

¿Cuántas oraciones aleatorias desea generar? 5

======================================================================
  ORACIONES ALEATORIAS
======================================================================

1. "the knife cuts he"
2. "he cuts"
3. "she cooks"
4. "a knife cooks"
5. "she drinks she"

======================================================================

¡Programa finalizado!
```

## Archivos incluidos

- `GeneradorOraciones.py`: Programa principal para generar oraciones
- `gramatica_english.txt`: Archivo de gramática en formato ASCII
- `gramatica.txt`: Gramática original con caracteres Unicode

## Notas técnicas

- El programa usa **expansión recursiva** para generar oraciones
- Incluye protección contra **recursión infinita** con profundidad máxima
- Las oraciones aleatorias pueden no tener sentido semántico perfecto, pero son gramaticalmente válidas según las reglas
- El generador aleatorio usa `random.choice()` para seleccionar producciones

## Diferencias con Ejercicio2.py

- **Ejercicio2.py**: Convierte gramáticas a Forma Normal de Chomsky (CNF)
- **GeneradorOraciones.py**: Genera oraciones en inglés a partir de la gramática

Ambos programas son complementarios y trabajan con gramáticas libres de contexto.
