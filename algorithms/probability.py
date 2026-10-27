"""Punto 1. Distribuciones discretas y decisiones de respuesta."""
import math


def normalize(weights: dict) -> dict:
    """Retorna un diccionario nuevo cuyas probabilidades suman uno.

    Entrada: weights = {resultado: peso}.
    Salida: {resultado: probabilidad}, con las mismas claves.

    Tips:
    - Conserve las claves y su orden; no modifique weights.
    - Rechace pesos negativos, no finitos, diccionarios vacíos y suma cero.
    """
    
    if not weights:
        raise ValueError("Diccionario vacío")
    if any(not math.isfinite(w) or w < 0 for w in weights.values()):
        raise ValueError("Pesos negativos o no finitos")
    total = sum(weights.values())
    if total == 0:
        raise ValueError("La suma de los pesos es cero")
    pesos = 0
    for resultado in weights.keys():
        pesos += weights[resultado]
    
    dicc_resultado = {}
    for resultado in weights.keys():
        dicc_resultado[resultado] = weights[resultado]/pesos
            
    
    return dicc_resultado
    #raise NotImplementedError("Complete este bloque TODO")
    # FIN DEL BLOQUE DEL ESTUDIANTE


def expected_utility(distribution: dict, utilities: dict) -> float:
    """Calcula sum_s P(s) U(s) para una acción.

    Entradas: distribution = {resultado: probabilidad} y
    utilities = {resultado: utilidad} para una sola acción.
    Salida: un número con la utilidad esperada.

    Tips:
    - distribution ya debe estar normalizada; no normalice utilidades.
    - Ambas tablas deben contener los mismos resultados posibles.
    """
    # Validación de las entradas; no modificar.
    if set(distribution) != set(utilities) or not distribution:
        raise ValueError("Probabilidades y utilidades deben tener las mismas claves")
    if any(not math.isfinite(p) or p < 0 for p in distribution.values()):
        raise ValueError("Distribución inválida")
    if not math.isclose(sum(distribution.values()), 1, abs_tol=1e-9):
        raise ValueError("La distribución debe sumar uno")
    if any(not math.isfinite(u) for u in utilities.values()):
        raise ValueError("Utilidades no finitas")
    
    utilidad_esperada = 0
    for resultado in distribution.keys():
        utilidad_esperada += distribution[resultado] * utilities[resultado]
    return utilidad_esperada
    #raise NotImplementedError("Complete este bloque TODO")
    # FIN DEL BLOQUE DEL ESTUDIANTE


def best_action(distribution: dict, actions: dict) -> tuple[str, dict]:
    """Retorna (nombre de acción, utilidades esperadas por acción).

    Entradas: distribution = {resultado: probabilidad} y
    actions = {acción: {resultado: utilidad}}.
    Salida: (acción elegida, {acción: utilidad esperada}).

    Tips:
    - actions asocia cada acción con su tabla de utilidades.
    - Reutilice expected_utility y conserve la primera acción en los empates.
    
    
    Primera version:
    
    if not actions:
            raise ValueError("Se requiere al menos una acción")
        
        mejor_accion = ''
        valor_mejor_accion = 0
        for accion in actions.keys():
            utilidad_esperada = expected_utility(actions[accion], distribution)
            if utilidad_esperada > valor_mejor_accion:
                mejor_accion = accion
                valor_mejor_accion = utilidad_esperada
        return {mejor_accion : valor_mejor_accion}
        
    Iteracion Con Ia:
    
    
    """
    
    values = {}
    for accion, utilidades in actions.items():
        values[accion] = expected_utility(distribution, utilidades)
    mejor = next(iter(values))
    for accion, eu in values.items():
        if eu > values[mejor]:
            mejor = accion
    return mejor, values
