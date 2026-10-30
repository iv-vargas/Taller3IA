"""Punto 3. Muestreo a priori y su extensión por rechazo."""
import random
from algorithms.probability import normalize


def prior_sample(network, rng: random.Random) -> dict:
    """Genera un mundo completo, muestreando padres antes que hijos.

    Entradas: network es la red y rng el generador aleatorio.
    Salida: un diccionario {nombre de variable: 0 o 1} con todos los nodos.

    Tips:
    - Use exclusivamente rng.random(); X=1 si r < P(X=1 | padres).
    - No fije evidencia aquí: esta función genera muestras a priori.
    - network.variables ya está en orden topológico. Consulte la CPT con
      network.probability(variable, 1, event), usando el evento parcial.
    """
    # Versión inicial propia: Tras revisar con ayuda de la IA se concluyó que la implementación es correcta.
    mundo = {}
    
    for variable in network.variables:
        probabilidad = network.probability(variable, 1, mundo)
        if rng.random() < probabilidad:
            mundo[variable] = 1
        else:
            mundo[variable] = 0
    
    return mundo
    


def sampling_ask(network, query, evidence, samples, rng, reject=False):
    """Estima una marginal o una condicional, usando exactamente samples intentos.

    Entradas: query es un nombre de variable; evidence es {variable: 0 o 1};
    samples es el número de intentos; rng es el generador aleatorio;
    reject indica si se descartan muestras incompatibles con la evidencia.
    Salida: (distribución estimada, número de muestras aceptadas).
    Use (None, 0) si ninguna muestra es compatible con la evidencia.

    Tips:
    - Reutilice prior_sample. Sin rechazo solo se permite evidence vacío.
    - Con rechazo cuente únicamente mundos compatibles con toda la evidencia.
    - Normalice los conteos aceptados, no divida entre intentos totales.
    - Si no acepta muestras, distribution=None; no invente ceros ni uniformes.
    """
    # Validación de las entradas; no modificar.
    network.validate_query(query, evidence)
    if samples < 1:
        raise ValueError("El número de muestras debe ser positivo")
    if evidence and not reject:
        raise ValueError("Muestreo a priori estima marginales; use rechazo con evidencia")
    
    """
    1. Versión inicial propia:
    query_0 = 0
    query_1 = 0
    muestras_aceptadas = 0
    
    for sample in range(samples):
        mundo = prior_sample(network, rng)
        
        if reject:
            for variable in mundo.keys():
                if mundo[variable] != evidence[variable]:
                    break
                else:
                    muestras_aceptadas += 1
                    if mundo[query] == 0:
                        query_0 += 1
                    else:
                        query_1 += 1
    
    if muestras_aceptadas == 0:
        return (None, 0)
    
    distribucion = normalize({0:query_0, 1:query_1})
    return (distribucion, muestras_aceptadas)

    Tras revisar la primera versión del algoritmo con ayuda de la IA se encontraron diversos errores en esta.
    Primero, el chequeo de compatibilidad recorría las variables del mundo en lugar de las de la evidencia,
    haciendo que evidence[variable] lance KeyError para toda variable no observaba. Segundo, los contadores se
    actualizan dentro del ciclo de comprobación de la evidencia, por lo que un mismo mundo se llegan a contar multiples
    veces. Tercero, todo el conteo se encuentra dentro un if reject, lo que hace que cuando reject sea false
    no se contara ningun mundo.
    """
    # Versión 2 corregida:
    query_0 = 0
    query_1 = 0
    muestras_aceptadas = 0
    
    for sample in range(samples):
        mundo = prior_sample(network, rng)
        aceptado = True
        
        for variable in evidence.keys():
            if evidence[variable] != mundo[variable]:
                aceptado = False
                break
        
        if aceptado:
            muestras_aceptadas += 1
            if mundo[query] == 0:
                query_0 += 1
            else:
                query_1 += 1
    
    if muestras_aceptadas == 0:
        return (None, 0)
    
    distribucion = normalize({0:query_0, 1:query_1})
    return (distribucion, muestras_aceptadas)
    
    
