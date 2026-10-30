"""Punto 2. Inferencia exacta por enumeración."""
from algorithms.probability import normalize


def enumeration_ask(network, query: str, evidence: dict) -> dict:
    """Calcula P(query | evidence) sobre la conjunta factorizada.

    Entradas: network es la red; query es el nombre de la
    variable consultada; evidence es {nombre de variable: 0 o 1}.
    Salida: {0: probabilidad, 1: probabilidad}.

    Tips:
    - Recorra network.variables en orden topológico.
    - Para una variable fijada multiplique su probabilidad; para una oculta
      sume las dos alternativas 0 y 1. Normalice al terminar.
    - Use copias del evento y no modifique evidence.
    - network.probability(variable, valor, evento) consulta la CPT;
      el evento debe contener los valores de todos los padres.
    - Puede usar una función auxiliar recursiva. Al terminar el recorrido,
      el producto sin factores restantes vale 1.
    - Evidencia imposible: ValueError. Consulta observada: distribución puntual
      solo si la evidencia es posible.
    """
    # Valida nombres de variables y dominio de la evidencia.
    network.validate_query(query, evidence)
    
    """
    Uso de la IA:
    
    El algorítmo se basa principalmente en la figura 13.11 del AIMA, la cual implementa esta inferencia
    en pseudocódigo. El uso de la IA se basó principalmente en entender algunos de estos aspectos del pseudocódigo
    que en principio no fueron muy claros para nosotros.
    
    En particular, la IA nos ayudó a aclarar los siguientes aspectos al momento de implementar el código:
    - Cómo determinar que la evidencia es imposible
    - Qué era exactamente "Rest"
    - Cómo calcular la sumatoria del else return en enumerate_all
    - Qué era exactamente e_xi y e_v y cómo definirlos
    - Qué es el parámetro "event" que solicita network.probability de bayes.py
    
    El código original fue:

    def enumeration_ask(network, query: str, evidence: dict) -> dict:
    
    q_x = {}
    
    for var in (0, 1):
      # if evidencia imposible:
        # return ValueError
      c_evidencia = evidencia
      q_x[x] = enumerate_all(network, network.variables, c_evidencia)
    return normalize(q_x)
    
    def enumerate_all(network, vars: list, evidence: dict) -> float:
    v = vars[0]
  
    if not vars:
      return 1.0
  
    if v in evidence:
      return network.probability(v, evidence[v], #EVENT) * enumerate_all(network, vars, evidence)
    else:
      #PENDIENTE
      
    Aquí, la IA ayudó a modelar x_i, e_xi y e_v y además a realizar la corrección de algunos temas puntuales como por ejemplo
    los parámetros de las funciones, el caso base de la función recursiva y la copia de la evidencia para no sobreescribirla. 
    """

    # TODO: Add your code here
    
    q_x = {}
    
    for x_i in (0, 1):
      if query in evidence and evidence[query] != x_i:
        q_x[x_i] = 0.0
        continue
      e_xi = {**evidence, query: x_i}
      q_x[x_i] = enumerate_all(network, network.variables, e_xi)
    return normalize(q_x)
      
    
    raise NotImplementedError("Complete este bloque TODO")
    # FIN DEL BLOQUE DEL ESTUDIANTE

""" Función auxiliar recursiva sugerida por uno de los tips, basada en Figure 13.11 de AIMA"""

def enumerate_all(network, vars: list, evidence: dict) -> float:
  
  if not vars:
    return 1.0
  
  v = vars[0]
  rest = vars[1:]
  
  if v in evidence:
    return network.probability(v, evidence[v], evidence) * enumerate_all(network, rest, evidence)
  else:
    total = 0.0
    for value in (0, 1):
      e_v = {**evidence, v: value}
      total += network.probability(v, value, e_v) * enumerate_all(network, rest, e_v)
    return total
    