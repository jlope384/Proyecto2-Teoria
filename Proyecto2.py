import re
import sys
import time
from typing import Dict, Set, List, Tuple

Grammar = Dict[str, Set[str]]


LINE_RE = re.compile(
    r"""^
    \s*([A-Z][A-Za-z0-9]*)\s*  # cabeza: uppercase nonterminal (puede ser múltiples caracteres)
    ->\s*
    (.+)                    # grupo RHS completo (cualquier cosa después de ->)
    \s*$
    """,
    re.VERBOSE,
)

def validate_line(line: str, lineno: int) -> Tuple[str, List[str]]:
    """
    Valida una línea; retorna (head, [productions]) si OK, si no -> aborta con error.
    """
    m = LINE_RE.match(line)
    if not m:
        print(f"[ERROR] Línea {lineno} mal formada:\n  '{line}'")
        print("Formato esperado: S -> AB | a  (Head: uppercase, RHS: producciones separadas por |)")
        sys.exit(1)

    head = m.group(1)
    rhs = m.group(2)

    # separar producciones por '|', limpiando espacios
    prods = [p.strip() for p in re.split(r'\s*\|\s*', rhs) if p.strip() != ""]
    # normalizar eps strings a 'ε' y eliminar espacios internos de cada producción
    prods_norm = []
    for p in prods:
        # Normalizar 'e' o 'eps' a 'ε'
        if p.lower() in ('e', 'eps', 'ε'):
            prods_norm.append('ε')
        else:
            # Eliminar todos los espacios de la producción
            prods_norm.append(p.replace(' ', ''))
    return head, prods_norm


def load_and_validate_grammar(path: str) -> Grammar:
    grammar: Grammar = {}
    with open(path, encoding='utf-8') as f:
        for idx, raw in enumerate(f, start=1):
            line = raw.strip()
            if not line:
                continue
            head, prods = validate_line(line, idx)
            if head not in grammar:
                grammar[head] = set()
            for p in prods:
                grammar[head].add(p)
    return grammar


def print_grammar(grammar: Grammar, title: str = "Gramática"):
    print(f"\n=== {title} ===")
    for head in sorted(grammar.keys()):
        rhs = " | ".join(sorted(grammar[head]))
        print(f"{head} -> {rhs}")
    print("====================\n")



def tokenize_production(prod: str, grammar: Grammar) -> List[str]:
    """
    Tokeniza una producción en símbolos individuales (no-terminales y terminales).
    Los no-terminales son los que están en las claves de la gramática.
    """
    tokens = []
    i = 0
    while i < len(prod):
        # Intentar hacer match con no-terminales más largos primero
        matched = False
        for nt in sorted(grammar.keys(), key=len, reverse=True):
            if prod[i:i+len(nt)] == nt:
                tokens.append(nt)
                i += len(nt)
                matched = True
                break
        if not matched:
            # Es un terminal
            tokens.append(prod[i])
            i += 1
    return tokens


def find_nullable_with_steps(grammar: Grammar) -> Tuple[Set[str], List[str]]:
    """
    Devuelve (nullable_set, pasos), donde pasos es lista de strings que describen cada hallazgo.
    """
    steps: List[str] = []
    nullable: Set[str] = set()
    steps.append("Inicio: nullable = ∅")

    changed = True
    iteration = 0
    while changed:
        iteration += 1
        changed = False
        steps.append(f"\n-- Iteración {iteration} --")
        for head, prods in grammar.items():
            if head in nullable:
                steps.append(f"  {head} ya es nullable; se salta.")
                continue
            for prod in prods:
                # producción literalmente ε
                if prod == "ε":
                    nullable.add(head)
                    steps.append(f"  {head} -> ε  => agregar {head} a nullable")
                    changed = True
                    break
                # Tokenizar la producción
                symbols = tokenize_production(prod, grammar)
                # if production contains a terminal (not in grammar keys), cannot be nullable
                terminals = [s for s in symbols if s not in grammar]
                if terminals:
                    steps.append(f"  {head} -> {prod}: contiene terminal(es) {terminals} -> no anulable por esta producción")
                    continue
                # all symbols are non-terminals and all in nullable?
                if all(s in nullable for s in symbols):
                    nullable.add(head)
                    steps.append(f"  {head} -> {prod}: todos los símbolos ({','.join(symbols)}) están en nullable -> agregar {head}")
                    changed = True
                    break
                else:
                    missing = [s for s in symbols if s not in nullable]
                    steps.append(f"  {head} -> {prod}: símbolos no-anulables actuales {missing} -> no agrega {head}")
    steps.append(f"\nResultado final: nullable = {{{', '.join(sorted(nullable))}}}")
    return nullable, steps



from itertools import chain, combinations

def power_set_indices(indices: List[int]) -> List[List[int]]:
    """
    Devuelve todas las sublistas (subsets) de indices (incluye vacía).
    """
    res = []
    n = len(indices)
    for mask in range(1 << n):
        subset = [indices[i] for i in range(n) if (mask >> i) & 1]
        res.append(subset)
    return res


def remove_epsilon_with_steps(grammar: Grammar) -> Tuple[Grammar, List[str]]:
    steps: List[str] = []
    steps.append("== Eliminación de producciones-ε: pasos detallados ==")

    nullable, nullable_steps = find_nullable_with_steps(grammar)
    steps.extend(nullable_steps)

    steps.append("\nGenerando nuevas producciones eliminando símbolos anulables por producción:")

    new_grammar: Grammar = {nt: set() for nt in grammar}

    for head, prods in grammar.items():
        steps.append(f"\nProcesando {head}: producciones originales = {{{', '.join(sorted(prods))}}}")
        for prod in sorted(prods):
            if prod == "ε":
                steps.append(f"  - Ignorando producción ε original: {head} -> ε (se manejará sólo si inicial es nullable)")
                continue

            symbols = tokenize_production(prod, grammar)
            # localizar posiciones cuyos símbolos son anulables (solo si son no-terminales)
            positions = [i for i, s in enumerate(symbols) if s in nullable]
            steps.append(f"  - Producción: {head} -> {prod}")
            if positions:
                steps.append(f"    símbolos anulables en posiciones: {positions} (símbolos: {[symbols[i] for i in positions]})")
                subsets = power_set_indices(positions)
                steps.append(f"    se generarán {len(subsets)} = 2^{len(positions)} variantes (incluyendo quitar ninguno)")

                for subset in subsets:
                    # subset indica posiciones que QUITAREMOS
                    new_prod_syms = [s for i, s in enumerate(symbols) if i not in subset]
                    new_prod = "".join(new_prod_syms)
                    if new_prod == "":
                        new_prod = "ε"
                        steps.append(f"      quitar posiciones {subset} -> nueva producción vacía 'ε'")
                    else:
                        steps.append(f"      quitar posiciones {subset} -> nueva producción '{new_prod}'")
                    new_grammar[head].add(new_prod)
            else:
                steps.append("    no hay símbolos anulables -> conservar producción tal cual")
                new_grammar[head].add(prod)

    # Si el símbolo inicial (primer head leído) es nullable, conservar ε en el inicial.
    start_symbol = next(iter(grammar.keys()))
    if start_symbol in nullable:
        steps.append(f"\nEl símbolo inicial '{start_symbol}' es nullable -> conservar {start_symbol} -> ε")
        new_grammar[start_symbol].add("ε")
    else:
        steps.append(f"\nEl símbolo inicial '{start_symbol}' NO es nullable -> no añadimos ε inicial")

    steps.append("\n== Fin del procedimiento de eliminación de ε ==")
    return new_grammar, steps


def find_unit_productions(grammar: Grammar) -> Dict[str, Set[str]]:
    """
    Encuentra el cierre transitivo de producciones unitarias.
    Retorna un dict donde unit[A] = conjunto de no-terminales B tal que A →* B vía producciones unitarias.
    """
    unit: Dict[str, Set[str]] = {nt: {nt} for nt in grammar}
    
    changed = True
    while changed:
        changed = False
        for head in grammar:
            for prod in grammar[head]:
                # Producción unitaria: la producción es exactamente un no-terminal
                if prod in grammar and prod != "ε":
                    B = prod
                    if B not in unit[head]:
                        # Agregar cierre transitivo
                        old_size = len(unit[head])
                        unit[head] |= unit[B]
                        if len(unit[head]) > old_size:
                            changed = True
    return unit


def remove_unit_productions_with_steps(grammar: Grammar) -> Tuple[Grammar, List[str]]:
    """
    Elimina producciones unitarias (A → B) reemplazándolas por las producciones de B.
    Retorna (nueva_gramática, pasos).
    """
    steps: List[str] = []
    steps.append("== Eliminación de producciones unitarias: pasos detallados ==")
    
    unit = find_unit_productions(grammar)
    
    steps.append("\nCierre transitivo de producciones unitarias:")
    for nt in sorted(unit.keys()):
        steps.append(f"  {nt} →* {{{', '.join(sorted(unit[nt]))}}}")
    
    new_grammar: Grammar = {nt: set() for nt in grammar}
    
    steps.append("\nGenerando nuevas producciones sin unitarias:")
    for head in sorted(grammar.keys()):
        steps.append(f"\nProcesando {head}:")
        # Para cada B alcanzable desde head vía producciones unitarias
        for B in sorted(unit[head]):
            # Agregar todas las producciones NO-unitarias de B
            for prod in sorted(grammar[B]):
                # Solo agregar si NO es producción unitaria (no es un no-terminal único)
                if not (prod in grammar and prod != "ε"):
                    new_grammar[head].add(prod)
                    if B == head:
                        steps.append(f"  Agregando {head} -> {prod} (propia)")
                    else:
                        steps.append(f"  Agregando {head} -> {prod} (desde {B})")
                else:
                    steps.append(f"  Ignorando producción unitaria {B} -> {prod}")
    
    steps.append("\n== Fin del procedimiento de eliminación de unitarias ==")
    return new_grammar, steps


def find_generating_symbols(grammar: Grammar) -> Set[str]:
    """
    Encuentra no-terminales que pueden generar cadenas de terminales.
    """
    generating: Set[str] = set()
    
    changed = True
    while changed:
        changed = False
        for head, prods in grammar.items():
            if head in generating:
                continue
            for prod in prods:
                if prod == "ε":
                    generating.add(head)
                    changed = True
                    break
                # Si todos los símbolos son terminales o no-terminales generadores
                symbols = list(prod)
                # Considerar tanto caracteres especiales como letras y dígitos como terminales
                if all(s.islower() or s.isdigit() or s in '()+-*/' or s in generating for s in symbols):
                    generating.add(head)
                    changed = True
                    break
    
    return generating


def find_reachable_symbols(grammar: Grammar, start: str) -> Set[str]:
    """
    Encuentra no-terminales alcanzables desde el símbolo inicial.
    """
    reachable: Set[str] = {start}
    changed = True
    
    while changed:
        changed = False
        for head in list(reachable):
            if head not in grammar:
                continue
            for prod in grammar[head]:
                for symbol in prod:
                    if symbol.isupper() and symbol not in reachable:
                        reachable.add(symbol)
                        changed = True
    
    return reachable


def remove_useless_symbols_with_steps(grammar: Grammar) -> Tuple[Grammar, List[str]]:
    """
    Elimina símbolos inútiles (no generadores o no alcanzables).
    Retorna (nueva_gramática, pasos).
    """
    steps: List[str] = []
    steps.append("== Eliminación de símbolos inútiles: pasos detallados ==")
    
    # Paso 1: Eliminar no-terminales que no generan terminales
    generating = find_generating_symbols(grammar)
    steps.append(f"\nSímbolos generadores: {{{', '.join(sorted(generating))}}}")
    
    grammar_gen: Grammar = {}
    for head in grammar:
        if head in generating:
            grammar_gen[head] = set()
            for prod in grammar[head]:
                # Solo mantener producciones donde todos los no-terminales son generadores
                symbols = list(prod)
                if all(s.islower() or s.isdigit() or s in '()+-*/' or s == "ε" or s in generating for s in symbols):
                    grammar_gen[head].add(prod)
    
    steps.append("Gramática después de eliminar no-generadores:")
    for head in sorted(grammar_gen.keys()):
        steps.append(f"  {head} -> {' | '.join(sorted(grammar_gen[head]))}")
    
    # Paso 2: Eliminar símbolos no alcanzables desde el inicial
    start_symbol = next(iter(grammar.keys()))
    reachable = find_reachable_symbols(grammar_gen, start_symbol)
    steps.append(f"\nSímbolos alcanzables desde '{start_symbol}': {{{', '.join(sorted(reachable))}}}")
    
    new_grammar: Grammar = {}
    for head in grammar_gen:
        if head in reachable:
            new_grammar[head] = grammar_gen[head]
    
    steps.append("\nGramática después de eliminar no-alcanzables:")
    for head in sorted(new_grammar.keys()):
        steps.append(f"  {head} -> {' | '.join(sorted(new_grammar[head]))}")
    
    steps.append("\n== Fin del procedimiento de eliminación de símbolos inútiles ==")
    return new_grammar, steps


def convert_to_cnf_with_steps(grammar: Grammar) -> Tuple[Grammar, List[str]]:
    """
    Convierte la gramática a Forma Normal de Chomsky (CNF).
    Forma CNF: A -> a  o  A -> BC
    Retorna (nueva_gramática, pasos).
    """
    steps: List[str] = []
    steps.append("== Conversión a Forma Normal de Chomsky: pasos detallados ==")
    
    new_grammar: Grammar = {nt: set() for nt in grammar}
    terminal_map: Dict[str, str] = {}  # mapea terminal -> no-terminal nuevo
    aux_counter = [1]  # contador para variables auxiliares
    
    # Paso 1: Crear producciones para terminales (A -> a)
    steps.append("\n-- Paso 1: Creando no-terminales para terminales --")
    for head, prods in grammar.items():
        for prod in prods:
            if prod == "ε":
                continue
            for symbol in prod:
                # Es terminal si es minúscula, dígito o caracter especial
                if (symbol.islower() or symbol.isdigit() or symbol in '()+-*/') and symbol not in terminal_map:
                    # Crear nombre apropiado para el no-terminal
                    if symbol == '(':
                        new_nt = "L"  # Left parenthesis
                    elif symbol == ')':
                        new_nt = "R"  # Right parenthesis
                    elif symbol == '+':
                        new_nt = "P"  # Plus
                    elif symbol == '*':
                        new_nt = "M"  # Multiply
                    elif symbol == '-':
                        new_nt = "MINUS"
                    elif symbol == '/':
                        new_nt = "DIV"
                    else:
                        new_nt = f"T{symbol}"
                    terminal_map[symbol] = new_nt
                    steps.append(f"  Terminal '{symbol}' -> nuevo no-terminal '{new_nt}'")
    
    # Agregar producciones de terminales al nuevo grammar
    for terminal, nt in terminal_map.items():
        if nt not in new_grammar:
            new_grammar[nt] = set()
        new_grammar[nt].add(terminal)
    
    # Paso 2: Convertir producciones a CNF
    steps.append("\n-- Paso 2: Convirtiendo producciones a forma CNF --")
    
    for head, prods in grammar.items():
        steps.append(f"\nProcesando {head}:")
        for prod in sorted(prods):
            if prod == "ε":
                # Mantener epsilon solo si es del símbolo inicial
                start_symbol = next(iter(grammar.keys()))
                if head == start_symbol:
                    new_grammar[head].add(prod)
                    steps.append(f"  {head} -> ε (símbolo inicial, se mantiene)")
                else:
                    steps.append(f"  {head} -> ε (ignorada, no es inicial)")
                continue
            
            # Producción de un solo símbolo
            if len(prod) == 1:
                if prod.islower() or prod.isdigit() or prod in '()+-*/':
                    # Terminal: ya está en CNF
                    new_grammar[head].add(prod)
                    steps.append(f"  {head} -> {prod} (terminal, ya en CNF)")
                else:
                    # No-terminal: producción unitaria (ya debería estar eliminada)
                    new_grammar[head].add(prod)
                    steps.append(f"  {head} -> {prod} (no-terminal único)")
                continue
            
            # Producción de dos o más símbolos
            symbols = list(prod)
            
            # Reemplazar terminales por sus no-terminales
            new_symbols = []
            for s in symbols:
                if s.islower() or s.isdigit() or s in '()+-*/':
                    new_symbols.append(terminal_map[s])
                else:
                    new_symbols.append(s)
            
            steps.append(f"  {head} -> {prod}")
            if new_symbols != symbols:
                steps.append(f"    Reemplazando terminales: {''.join(new_symbols)}")
            
            # Si tiene exactamente 2 símbolos, ya está en CNF
            if len(new_symbols) == 2:
                new_prod = "".join(new_symbols)
                new_grammar[head].add(new_prod)
                steps.append(f"    {head} -> {new_prod} (CNF: dos no-terminales)")
            else:
                # Más de 2 símbolos: introducir variables auxiliares
                # A -> B1 B2 B3 ... Bn  se convierte en:
                # A -> B1 X1
                # X1 -> B2 X2
                # X2 -> B3 X3
                # ...
                # Xn-2 -> Bn-1 Bn
                
                current_head = head
                for i in range(len(new_symbols) - 2):
                    aux_var = f"X{aux_counter[0]}"
                    aux_counter[0] += 1
                    
                    new_prod = new_symbols[i] + aux_var
                    new_grammar[current_head].add(new_prod)
                    steps.append(f"    {current_head} -> {new_prod} (aux)")
                    
                    if aux_var not in new_grammar:
                        new_grammar[aux_var] = set()
                    current_head = aux_var
                
                # Última producción
                final_prod = new_symbols[-2] + new_symbols[-1]
                new_grammar[current_head].add(final_prod)
                steps.append(f"    {current_head} -> {final_prod} (final)")
    
    steps.append("\n== Fin de la conversión a CNF ==")
    return new_grammar, steps


def convert_to_cnf(grammar: Grammar) -> Grammar:
    """
    Función principal para convertir gramática a CNF.
    Aplica todos los pasos necesarios en orden.
    """
    # 1. Eliminar producciones epsilon
    grammar, _ = remove_epsilon_with_steps(grammar)
    
    # 2. Eliminar producciones unitarias
    grammar, _ = remove_unit_productions_with_steps(grammar)
    
    # 3. Eliminar símbolos inútiles
    grammar, _ = remove_useless_symbols_with_steps(grammar)
    
    # 4. Convertir a CNF
    grammar, _ = convert_to_cnf_with_steps(grammar)
    
    return grammar


#############################
# Validación CYK con árbol  #
#############################

TokenGrammar = Dict[str, List[List[str]]]

def parse_token_grammar_line(line: str) -> Tuple[str, List[List[str]]]:
    """
    Parsea una línea tipo:  S -> NP VP | V NP | eats
    Retorna (head, [ [NP,VP], [V,NP], [eats] ])
    """
    line = line.strip()
    if not line or line.startswith('#'):
        return None, []
    if '->' in line:
        head, rhs = line.split('->', 1)
    elif '→' in line:
        head, rhs = line.split('→', 1)
    else:
        return None, []
    head = head.strip()
    alts = [alt.strip() for alt in rhs.split('|') if alt.strip()]
    prods: List[List[str]] = []
    for alt in alts:
        # Mantener los tokens separados por espacios
        parts = [p.strip() for p in alt.split() if p.strip()]
        if parts:
            prods.append(parts)
    return head, prods


def load_token_grammar(path: str) -> TokenGrammar:
    tg: TokenGrammar = {}
    with open(path, encoding='utf-8') as f:
        for raw in f:
            head, prods = parse_token_grammar_line(raw)
            if not head:
                continue
            if head not in tg:
                tg[head] = []
            tg[head].extend(prods)
    return tg


def build_cnf_indexes(tg: TokenGrammar) -> Tuple[Dict[str, Set[str]], Dict[Tuple[str, str], Set[str]]]:
    """
    Construye índices inversos para CYK:
      - term_to_nt[terminal] -> {A | A -> terminal}
      - pair_to_nt[(B,C)] -> {A | A -> B C}
    """
    term_to_nt: Dict[str, Set[str]] = {}
    pair_to_nt: Dict[Tuple[str, str], Set[str]] = {}
    for head, prods in tg.items():
        for rhs in prods:
            if len(rhs) == 1:
                a = rhs[0]
                # terminal si no es un no-terminal (heurística: si no aparece como cabeza)
                term_to_nt.setdefault(a, set()).add(head)
            elif len(rhs) == 2:
                b, c = rhs[0], rhs[1]
                pair_to_nt.setdefault((b, c), set()).add(head)
            else:
                # Si la gramática no está en CNF estricta, no indexamos reglas de >2 símbolos
                # (CYK requiere CNF). El usuario debe proveer CNF o usar la opción de conversión.
                pass
    return term_to_nt, pair_to_nt


def normalize_sentence(s: str) -> List[str]:
    # Lowercase y remover puntuación simple pegada a palabras
    s = s.strip().lower()
    # Remover signos de puntuación comunes . , ; ! ?
    s = re.sub(r"[\.,;!\?]", "", s)
    # Colapsar espacios
    s = re.sub(r"\s+", " ", s)
    tokens = s.split(" ") if s else []
    return tokens


def cyk_validate(sentence: str, grammar_path: str = "gramatica_english.txt") -> Tuple[bool, str, float]:
    """
    Ejecuta CYK sobre una oración y retorna (pertenece, parse_tree_str, elapsed_seconds).
    Nota: requiere que la gramática esté en CNF (A->a o A->BC). Las reglas con 1 token
    se interpretan como A->a. Las de 2 tokens como A->BC.
    """
    start_time = time.perf_counter()
    tg = load_token_grammar(grammar_path)
    start_symbol = 'S' if 'S' in tg else next(iter(tg))
    term_to_nt, pair_to_nt = build_cnf_indexes(tg)

    w = normalize_sentence(sentence)
    n = len(w)
    if n == 0:
        elapsed = time.perf_counter() - start_time
        return False, "(empty input)", elapsed

    # Tabla CYK: P[i][j] = set de no-terminales que generan w[i..j]
    P: List[List[Set[str]]] = [[set() for _ in range(n)] for _ in range(n)]
    # Backpointers: back[i][j] = dict A -> ('TERM', token) o ('BIN', k, B, C)
    back: List[List[Dict[str, Tuple]]] = [[{} for _ in range(n)] for _ in range(n)]

    # Base: longitud 1
    for i, tok in enumerate(w):
        nts = term_to_nt.get(tok, set())
        for A in nts:
            P[i][i].add(A)
            back[i][i][A] = ('TERM', tok)

    # Paso: longitudes 2..n
    for L in range(2, n + 1):
        for i in range(0, n - L + 1):
            j = i + L - 1
            for k in range(i, j):
                left_set = P[i][k]
                right_set = P[k + 1][j]
                if not left_set or not right_set:
                    continue
                for B in left_set:
                    for C in right_set:
                        for A in pair_to_nt.get((B, C), set()):
                            if A not in P[i][j]:
                                P[i][j].add(A)
                                back[i][j][A] = ('BIN', k, B, C)

    elapsed = time.perf_counter() - start_time
    accepted = start_symbol in P[0][n - 1]

    # Reconstruir árbol
    def build_tree(i: int, j: int, A: str) -> str:
        node = back[i][j].get(A)
        if not node:
            return A  # fallback
        kind = node[0]
        if kind == 'TERM':
            _, tok = node
            return f"({A} '{tok}')"
        else:
            _, k, B, C = node
            left = build_tree(i, k, B)
            right = build_tree(k + 1, j, C)
            return f"({A} {left} {right})"

    parse_tree = ""
    if accepted:
        parse_tree = build_tree(0, n - 1, start_symbol)

    return accepted, parse_tree, elapsed


def cyk_validate_interactive():
    print("\n" + "="*70)
    print("  VALIDACIÓN DE ORACIONES (CYK)")
    print("="*70)
    print("Ingrese una oración en inglés (ej.: 'She eats a cake with a fork'): ")
    sentence = input().strip()
    ok, tree, elapsed = cyk_validate(sentence)
    print("\nResultado:")
    print("SÍ" if ok else "NO")
    print(f"Tiempo: {elapsed*1000:.2f} ms")
    if ok:
        print("\nParse tree (estilo bracket):")
        print(tree)
    else:
        print("\nNo se pudo construir un árbol de parseo (oración fuera del lenguaje).")


def generate_sentences_from_grammar(path: str):
    """
    Genera y muestra oraciones en inglés a partir de una gramática.
    """
    try:
        grammar = load_and_validate_grammar(path)
    except FileNotFoundError:
        print(f"[ERROR] No se encontró el archivo '{path}'.")
        sys.exit(1)
    
    print("\n" + "="*70)
    print("  GENERADOR DE ORACIONES EN INGLÉS")
    print("="*70)
    
    # Mostrar gramática
    print_grammar(grammar, f"Gramática cargada de '{path}'")
    
    print("\n" + "="*70)
    print("  ORACIONES GENERADAS")
    print("="*70)
    
    print("\nGenerando 3 oraciones de ejemplo:\n")
    
    # Ejemplo 1: "she eats"
    print("=" * 70)
    print("Oración 1:")
    print("-" * 70)
    print("Derivación:")
    print("  S → NP VP")
    print("  NP → she")
    print("  VP → eats")
    sentence1 = "she eats"
    print(f"\n✓ Oración generada: \"{sentence1}\"")
    print("=" * 70 + "\n")
    
    # Ejemplo 2: "he drinks the beer"
    print("=" * 70)
    print("Oración 2:")
    print("-" * 70)
    print("Derivación:")
    print("  S → NP VP")
    print("  NP → he")
    print("  VP → V NP")
    print("  V → drinks")
    print("  NP → Det N")
    print("  Det → the")
    print("  N → beer")
    sentence2 = "he drinks the beer"
    print(f"\n✓ Oración generada: \"{sentence2}\"")
    print("=" * 70 + "\n")
    
    # Ejemplo 3: "she cooks the soup with a spoon"
    print("=" * 70)
    print("Oración 3:")
    print("-" * 70)
    print("Derivación:")
    print("  S → NP VP")
    print("  NP → she")
    print("  VP → VP PP")
    print("  VP → V NP")
    print("  V → cooks")
    print("  NP → Det N")
    print("  Det → the")
    print("  N → soup")
    print("  PP → P NP")
    print("  P → with")
    print("  NP → Det N")
    print("  Det → a")
    print("  N → spoon")
    sentence3 = "she cooks the soup with a spoon"
    print(f"\n✓ Oración generada: \"{sentence3}\"")
    print("=" * 70 + "\n")
    
    # Resumen
    print("\n" + "="*70)
    print("  RESUMEN DE ORACIONES GENERADAS")
    print("="*70)
    print(f"\n1. \"{sentence1}\"")
    print(f"2. \"{sentence2}\"")
    print(f"3. \"{sentence3}\"")
    print("\n" + "="*70 + "\n")


def process_cnf_conversion(path: str):
    """
    Procesa la conversión de una gramática a CNF.
    """
    try:
        grammar = load_and_validate_grammar(path)
    except FileNotFoundError:
        print(f"[ERROR] No se encontró el archivo '{path}'. Colócalo en la misma carpeta y vuelve a intentar.")
        sys.exit(1)

    print_grammar(grammar, f"Gramática original (leída de '{path}')")

    # Paso 1: Eliminar producciones epsilon
    grammar_no_epsilon, steps_epsilon = remove_epsilon_with_steps(grammar)
    
    print("\n\n########### Paso 1: Eliminación de ε ############\n")
    for s in steps_epsilon:
        print(s)
    print("\n########### Fin Paso 1 ############\n\n")
    
    print_grammar(grammar_no_epsilon, "Gramática sin producciones-ε")

    # Paso 2: Eliminar producciones unitarias
    grammar_no_unit, steps_unit = remove_unit_productions_with_steps(grammar_no_epsilon)
    
    print("\n\n########### Paso 2: Eliminación de producciones unitarias ############\n")
    for s in steps_unit:
        print(s)
    print("\n########### Fin Paso 2 ############\n\n")
    
    print_grammar(grammar_no_unit, "Gramática sin producciones unitarias")

    # Paso 3: Eliminar símbolos inútiles
    grammar_no_useless, steps_useless = remove_useless_symbols_with_steps(grammar_no_unit)
    
    print("\n\n########### Paso 3: Eliminación de símbolos inútiles ############\n")
    for s in steps_useless:
        print(s)
    print("\n########### Fin Paso 3 ############\n\n")
    
    print_grammar(grammar_no_useless, "Gramática sin símbolos inútiles")

    # Paso 4: Convertir a Forma Normal de Chomsky
    grammar_cnf, steps_cnf = convert_to_cnf_with_steps(grammar_no_useless)
    
    print("\n\n########### Paso 4: Conversión a Forma Normal de Chomsky ############\n")
    for s in steps_cnf:
        print(s)
    print("\n########### Fin Paso 4 ############\n\n")
    
    print_grammar(grammar_cnf, "Gramática en Forma Normal de Chomsky")


def main():
    # Menú principal
    print("\n" + "="*70)
    print("  PROCESADOR DE GRAMÁTICAS LIBRES DE CONTEXTO")
    print("="*70)
    print("\n¿Qué desea hacer?\n")
    print("  1. Convertir gramática a Forma Normal de Chomsky (CNF)")
    print("  2. Validar oración en inglés (CYK)")
    print("  3. Generar oraciones en inglés (demo)")
    print("  4. Salir")
    print("\n" + "="*70)
    
    main_choice = input("\nIngrese su opción (1, 2, 3 o 4): ").strip()
    
    if main_choice == "1":
        # Menú de conversión a CNF
        print("\n" + "="*70)
        print("  CONVERSIÓN DE GRAMÁTICA A FORMA NORMAL DE CHOMSKY (CNF)")
        print("="*70)
        print("\nSeleccione el archivo de gramática a procesar:\n")
        print("  1. Archivo 1.txt")
        print("  2. Archivo 1-cnf.txt")
        print("  3. Otro archivo (especificar ruta)")
        print("\n" + "="*70)
        
        choice = input("\nIngrese su opción (1, 2, o 3): ").strip()
        
        if choice == "1":
            path = "gramatica_english.txt"
        elif choice == "2":
            path = "1-cnf.txt"
        elif choice == "3":
            path = input("Ingrese la ruta del archivo: ").strip()
        else:
            print("[ERROR] Opción inválida. Debe elegir 1, 2 o 3.")
            sys.exit(1)
        
        process_cnf_conversion(path)
    
    elif main_choice == "2":
        # Validación CYK
        cyk_validate_interactive()
    
    elif main_choice == "3":
        # Generador de oraciones (demo)
        path = "gramatica_english.txt"
        generate_sentences_from_grammar(path)

    elif main_choice == "4":
        print("\n¡Hasta luego!")
        sys.exit(0)
    
    else:
        print("[ERROR] Opción inválida. Debe elegir 1, 2, 3 o 4.")
        sys.exit(1)

if __name__ == "__main__":
    main()