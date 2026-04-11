# 🚐 Rueditas Amigas - Diagrama de Despliegue

**Rueditas Amigas** es una empresa dedicada a brindar servicios de traslado inclusivos para personas con necesidades específicas. La organización ofrece diferentes tipos de servicios adaptados, tales como traslados turísticos y actividades recreativas, garantizando recorridos de ida y vuelta, dejando a los pasajeros, en el mismo punto de encuentro que en la salida. 
Parte de nuestro equipo realizó previamente el modelo de datos y definió un esquema relacional para persistir la información del sistema (ver modelo en el siguiente link). 
A partir de este modelo, se implementó una primera versión del sistema, la cual actualmente presenta diversas problemáticas operativas debido al crecimiento del negocio y el aumento en la cantidad de usuarios.

---

### ⚠️ Problemáticas Actuales

* Cuando se registra un alto volumen de personas realizando solicitudes de reserva de manera simultánea, el sistema experimenta una degradación significativa en su rendimiento. Las pantallas demoran en cargar o directamente dejan de responder, generando tiempos de espera elevados y una experiencia negativa para el usuario.
* En este contexto, el equipo de Rueditas Amigas nos comenta que además de requerir una solución que mejore el rendimiento, es necesario que el sistema también sea tolerante a fallos para evitar caídas del sistema y garantizar la continuidad del servicio.

Proponé y diagramá una arquitectura que resuelva estas problemáticas usando PlantUML.

---

### 🖼️ Diagrama de Despliegue
> [!IMPORTANT]
> En caso de que las validaciones sean correctas, el diagrama se generará automáticamente mediante GitHub Actions en la carpeta `diagrams/`.

---

## 🔗 Enlace al enunciado del modelo relacional
* 📄 [Modelo de Datos Relacional]([https://docs.google.com/...](https://docs.google.com/document/d/1vDZ-ybIgk7lBvqI5vZ0lp2qpSolJnpKDtUftYn65XU8/edit?usp=sharing)
* 📄 [Documentación de Diagramas de Despliegue en PLantUML](https://plantuml.com/es/deployment-diagram).
* 📄 [Link Enunciado]([https://plantuml.com/es/deployment-diagram](https://docs.google.com/document/d/1ZwuV6ZYL8CbhLsqYLzW98h5nP8PAU0XXAEapIen8ls0/edit?usp=sharing)).

