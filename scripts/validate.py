import re
import sys
from pathlib import Path

# ----------------------------
# 1. Cargar archivo
# ----------------------------
files = list(Path("diagrams").glob("*.puml"))
if not files:
    print("❌ No .puml file found")
    sys.exit(1)

file_path = files[0]
lines = file_path.read_text().splitlines()

# ----------------------------
# Matcheo por nombres
# ----------------------------

def matchea_nombre (prefixes, keywords, text):
    # Creamos el grupo de keywords: (Administrador|Persona Administradora|...) permitiendo espacios en el medio
    def make_flexible(word):
        return r"\s*".join(list(word))

    flexible_keywords = [make_flexible(k) for k in keywords]
    keyword_group = "|".join(flexible_keywords)

    # El regex busca: (Comienza con admin seguido de lo que sea) O (Cualquier keyword de la lista)
    # Expresión: (admin.*|Administrador|Persona Administradora)
    search_pattern = rf"({prefixes}.*|{keyword_group})"

    print(f"Pattern: {search_pattern}")

    match = re.search(search_pattern, text, re.IGNORECASE)
    return match is not None

# ----------------------------
# 2. Parseo
# ----------------------------
componentes = {}   # nombre -> tipo
relaciones = []   # {desde, to}

def extraer_nombre(linea):
    m = re.search(r'"([^"]+)"', linea)
    return m.group(1) if m else None

for line in lines:
    l = line.lower()

    # detectar nodos por tipo
    if "actor" in l:
        nombre = extraer_nombre(line)
        if nombre:
            componentes[nombre] = "actor"

    elif "database" in l:
        nombre = extraer_nombre(line)
        if nombre:
            componentes[nombre] = "database"

    elif "cloud" in l:
        nombre = extraer_nombre(line)
        if nombre:
            componentes[nombre] = "cloud"

    elif "node" in l:
        nombre = extraer_nombre(line)
        if nombre:
            componentes[nombre] = "node"

    # detectar relaciones
    m = re.search(r'"([^"]+)"\s*(.*?)\s*([<>-]+)\s*"([^"]+)"', line)
    if m:
        componente_izquierdo = m.group(1)
        flecha = m.group(3)
        componente_derecho = m.group(4)

        if ">" in flecha and "<" not in flecha:
            # left -> right
            relaciones.append({"desde": componente_izquierdo, "hasta": componente_derecho})

        elif "<" in flecha and ">" not in flecha:
            # right -> left
            relaciones.append({"desde": componente_derecho, "hasta": componente_izquierdo})

        else:
            # caso "--" (sin dirección)
            pass

# ----------------------------
# 3. Componentes
# ----------------------------

def tipo_componente(nombre):
    return componentes.get(nombre)

def componentes_de_tipo(tipo):
    return [c for c, t in componentes.items() if t == tipo]

# Detectar nodos balanceadores y servidores
# (cloud -> balanceador -> >=2 servidores)
balanceadores = set()
servidores = set()

for c, t in componentes.items():
    if t != "node":
        continue

    internet_entrante = [
        r for r in relaciones
        if r["hasta"] == c and tipo_componente(r["desde"]) == "cloud"
    ]

    nodos_salientes = [
        r for r in relaciones
        if r["desde"] == c and tipo_componente(r["hasta"]) == "node"
    ]

    if len(internet_entrante) >= 1 and len(nodos_salientes) >= 2:
        componentes[c] = "balanceador"
        balanceadores.add(c)

        # Marco los nodos balanceados como servidores
        for r in nodos_salientes:
            nodo = r["hasta"]
            componentes[nodo] = "servidor"
            servidores.add(nodo)

        break

actores = componentes_de_tipo("actor")
databases = componentes_de_tipo("database")
nodos = componentes_de_tipo("node")
clouds = componentes_de_tipo("cloud")

# ----------------------------
# 3. Validaciones
# ----------------------------
errors = 0

def fail(msg):
    global errors
    print(f"❌ {msg}")
    errors += 1

def ok(msg):
    print(f"✅ {msg}")

# ----------------------------
# Al menos 1 actor, todos conectados a través de internet
# ----------------------------

actores_desconectados = any(
    not any(
        tipo_componente(r["hasta"]) == "cloud"
        for r in relaciones
        if r["desde"] == a
    )
    for a in actores
)

if not actores:
    fail("Debe haber al menos un actor")
elif actores_desconectados:
    fail("Todos los actores deben estar conectados a través de internet (ver elementos cloud)")
else:
    for a in actores:
        es_solicitante = matchea_nombre(["user", "usua"], ["Usuario", "User", "Solicitante"], a)
        es_admin = matchea_nombre(["admin"], ["Administrador", "Persona Administradora"], a)

        print(f"✅ Solicitante encontrado: {es_solicitante}")
        print(f"✅ Solicitante encontrado: {es_admin}")

        if es_solicitante:
            print(f"✅ Solicitante encontrado: {a}")
        elif es_admin:
            print(f"✅ Administrador encontrado: {a}")
        else:
            print(f"No matchea: {a}")

    ok("Actor/es OK")

# ----------------------------
# Hay un y solo un balanceador
# ----------------------------

if not balanceadores:
    fail("Debe haber al menos un balanceador (internet --> balanceador --> multiples nodos)")
elif len(balanceadores) > 1:
    fail("No debe haber más de un balanceador")
else:
    ok("Balanceador OK")

balanceador = balanceadores.pop()

# ----------------------------
# Al menos una database, sin actores conectados
# ----------------------------

actores_a_dbs = any(
    any(
        tipo_componente(r["hasta"]) == "database"
        for r in relaciones
        if r["desde"] == a
    )
    for a in actores
)

if not databases:
    fail("Debe haber al menos una base de datos")
elif actores_a_dbs:
    fail("No debe haber actores conectados a una base de datos")
else:
    ok("Base/s de datos OK")

# ----------------------------
# Todos los servidores comparten relaciones
# ----------------------------

def salidas(s):
    return {
        r["hasta"]
        for r in relaciones
        if r["desde"] == s
    }

# Servidor cualquiera de entre el set
ref = salidas(next(iter(servidores)))

comparten_salidas = all(
    salidas(s) == ref
    for s in servidores
)

if not comparten_salidas:
    fail("Los servidores no comparten las mismas relaciones")
else:
    ok("Servidores OK")

# ----------------------------
# 4. Resultado final
# ----------------------------
if errors > 0:
    print(f"📝 Correcciones pendientes: {errors}")
    sys.exit(1)

print("✅ ✨Ejercicio correcto✨")