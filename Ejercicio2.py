import re
import sys
from typing import Dict, Set, List, Tuple

Grammar = Dict[str, Set[str]]


LINE_RE = re.compile(
    r"""^
    \s*([A-Z])\s*          # cabeza: single uppercase nonterminal (capturado)
    ->\s*
    (                       # grupo RHS completo
        (?:                 # una producción:
            (?:[A-Za-z0-9]|ε|eps)+   # secuencia de símbolos terminales/no-term (o epsilon)
        )
        (?:\s*\|\s*         # posiblemente seguidas por | producción
            (?:[A-Za-z0-9]|ε|eps)+
        )*
    )
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
        print("Formato esperado: S -> 0A0 | 1B1 | BB  (Head: single uppercase, RHS: producciones separadas por |)")
        sys.exit(1)

    head = m.group(1)
    rhs = m.group(2)

    # separar producciones por '|', limpiando espacios
    prods = [p.strip() for p in re.split(r'\s*\|\s*', rhs) if p.strip() != ""]
    # normalizar eps strings a 'ε'
    prods_norm = [("ε" if p.lower() == "eps" else p) for p in prods]
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
                # si todos los símbolos de prod son no-terminales presentes en nullable
                # recordamos convención: cada símbolo en prod es un char
                symbols = list(prod)
                # if production contains a terminal (lowercase or digit), cannot be nullable
                if any(re.match(r'[a-z0-9]', s) for s in symbols):
                    steps.append(f"  {head} -> {prod}: contiene terminal(es) -> no anulable por esta producción")
                    continue
                # all symbols uppercase and all in nullable?
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

            symbols = list(prod)
            # localizar posiciones cuyos símbolos son anulables (solo si son mayúsculas)
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


def main():
    path = "gramatica.txt"
    try:
        grammar = load_and_validate_grammar(path)
    except FileNotFoundError:
        print(f"[ERROR] No se encontró el archivo '{path}'. Colócalo en la misma carpeta y vuelve a intentar.")
        sys.exit(1)

    print_grammar(grammar, "Gramática original (leída y validada)")

    new_grammar, steps = remove_epsilon_with_steps(grammar)

    # Mostrar pasos (puede ser extenso)
    print("\n\n########### Trazas detalladas (pasos) ############\n")
    for s in steps:
        print(s)
    print("\n########### Fin de trazas ############\n\n")

    print_grammar(new_grammar, "Gramática resultante (sin producciones-ε)")

main()