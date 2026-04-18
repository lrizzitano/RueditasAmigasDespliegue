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

    prefixes_group = "|".join(prefixes)

    flexible_keywords = [make_flexible(k) for k in keywords]
    keyword_group = "|".join(flexible_keywords)

    # El regex busca: (Comienza con admin seguido de lo que sea) O (Cualquier keyword de la lista)
    # Expresión: (admin.*|Administrador|Persona Administradora)
    search_pattern = rf"({prefixes_group}.*|{keyword_group})"

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
# Hay entre 2 y 4 actores
# ----------------------------
actor_extranio = False
cant_solicitantes = 0
cant_admins = 0

for a in actores:
        es_solicitante = matchea_nombre(["user", "usua"], ["Persona Usuaria", "Persona Solicitante", "Solicitante"], a)
        es_admin = matchea_nombre(["admin"], ["Administrador", "Persona Administradora"], a)

        if es_solicitante:
            print(f"✅ Solicitante encontrado: {a}")
            cant_solicitantes += 1
        elif es_admin:
            print(f"✅ Administrador encontrado: {a}")
            cant_admins += 1
        else:
            actor_extranio = True
           

if len(actores) < 2:
    fail("Debe haber al menos dos actores definidos (ver elemento 'actor')")
elif len(actores) > 4:
    fail("Hay demasiados actores, todos están realmente justificados?")
elif cant_solicitantes < 1:
    fail("Debe haber al menos un actor que represente a les solicitantes")
elif cant_admins < 1:
    fail("Debe haber al menos un actor que represente a les administradores")
elif actor_extranio:
    fail("Se encontraron actores que no corresponden a solicitantes ni administradores.")
else:
    ok("Actores OK")

# ----------------------------
# Si hay componente cloud && solo 1 nodo => los actores deben estar conectados
# ----------------------------
actores_desconectados = False

if clouds and len(nodos) == 1:
    actores_desconectados = any(
        not any(
            tipo_componente(r["hasta"]) == "cloud"
            for r in relaciones
            if r["desde"] == a
        )
        for a in actores
    )

if actores_desconectados:
    fail("Todos los actores deben estar conectados a través de internet")
else:
    ok("Conexion de actores OK")

# ----------------------------
# Al menos una database, sin actores conectados
# ----------------------------

actores_a_dbs = any(
    (tipo_componente(r["desde"]) == "actor" and tipo_componente(r["hasta"]) == "database") or
    (tipo_componente(r["desde"]) == "database" and tipo_componente(r["hasta"]) == "actor")
    for r in relaciones
)

if not databases:
    fail("Debe haber al menos una base de datos")
elif actores_a_dbs:
    fail("No debe haber actores conectados directamente a una base de datos")
else:
    ok("Base/s de datos OK")

# ----------------------------
# Hay entre 1 y 3 nodos
# ----------------------------

if not nodos:
    fail("Debe haber al menos un nodo")
elif len(nodos) > 3:
    fail("Hay demasiados nodos, todos están realmente justificados?")
else:
    ok("Nodo/s OK")

# ----------------------------
# 4. Resultado final
# ----------------------------
if errors > 0:
    print(f"📝 Correcciones pendientes: {errors}")
    sys.exit(1)

print("✅ ✨TPI2 aprobado✨")