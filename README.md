# 🚐 Rueditas Amigas - Diagrama de Despliegue

![PlantUML](https://img.shields.io/badge/Architecture-PlantUML-blue?style=flat-square)
![Status](https://img.shields.io/badge/Status-Validated-green?style=flat-square)

**Rueditas Amigas** es una plataforma de traslados inclusivos diseñada para personas con necesidades específicas. Este repositorio contiene la arquitectura de despliegue propuesta para escalar el sistema y garantizar la continuidad del servicio.

---

Rueditas Amigas es una empresa dedicada a brindar servicios de traslado inclusivos para personas con necesidades específicas. La organización ofrece diferentes tipos de servicios adaptados, tales como traslados turísticos y actividades recreativas, garantizando recorridos de ida y vuelta, dejando a los pasajeros, en el mismo punto de encuentro que en la salida. 
Parte de nuestro equipo realizó previamente el modelo de datos y definió un esquema relacional para persistir la información del sistema (ver modelo en el siguiente link). 
A partir de este modelo, se implementó una primera versión del sistema, la cual actualmente presenta diversas problemáticas operativas debido al crecimiento del negocio y el aumento en la cantidad de usuarios.

### ⚠️ Problemáticas Actuales

* Cuando se registra un alto volumen de personas realizando solicitudes de reserva de manera simultánea, el sistema experimenta una degradación significativa en su rendimiento. Las pantallas demoran en cargar o directamente dejan de responder, generando tiempos de espera elevados y una experiencia negativa para el usuario.
* En este contexto, el equipo de Rueditas Amigas nos comenta que además de requerir una solución que mejore el rendimiento, es necesario que el sistema también sea tolerante a fallos para evitar caídas del sistema y garantizar la continuidad del servicio.

---

### 🖼️ Diagrama de Despliegue
> [!TIP]
> El diagrama se genera automáticamente mediante GitHub Actions tras cada cambio en la carpeta `diagrams/`.

![Diagrama de Despliegue](./output/deployment.png)

---

## 🔗 Enlaces de Interés
* 📄 [Modelo de Datos Relacional](https://docs.google.com/...)

---
<p align="center">
  Desarrollado con ❤️ para garantizar un traslado inclusivo y eficiente.
</p>
