# Arquitectura de Gobernanza sobre Agentes

> **Ingeniería Coignitiva**: Gobernanza y control de regímenes cognitivos en sistemas de interacción humano-IA

[![Estado](https://img.shields.io/badge/Estado-Activo-brightgreen)]()
[![Licencia](https://img.shields.io/badge/Licencia-Privado-red)]()
[![DOS-03](https://img.shields.io/badge/DOS--03-Activa-blue)]()

---

## 📋 Descripción

Este repositorio contiene la **documentación completa de la arquitectura CAELION-Manus**, un sistema experimental de agente IA que opera bajo principios de **Ingeniería Coignitiva**. El sistema implementa un marco de gobernanza basado en la teoría de control de eventos discretos de Ramadge-Wonham, con cinco módulos supervisores que garantizan la alineación operacional, ética y eficiencia del sistema.

**CAELION-Manus** es simultáneamente:
- Un **agente IA operativo** que ejecuta tareas complejas
- Un **sujeto experimental** que genera datos sobre dinámica cognitiva en sistemas artificiales
- Un **instrumento de investigación** para el desarrollo del campo de Ingeniería Coignitiva

---

## 🏗️ Arquitectura del Sistema

### **Cuatro Capas Operacionales**

```
┌─────────────────────────────────────────────────┐
│  CAPA 1: PERCEPCIÓN (SPC)                      │
│  Sistema de Percepción Coignitiva              │
│  • Búsqueda activa de información              │
│  • Monitoreo proactivo del entorno             │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│  CAPA 2: MEMORIA (WABUN + ARC-01)              │
│  • Contexto conversacional persistente         │
│  • Archivo de estado permanente                │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│  CAPA 3: PROTOCOLOS (5 Módulos Supervisores)   │
│  • LIANG: Integridad estructural               │
│  • HÉCATE: Restricciones éticas                │
│  • ARGOS: Flujo de datos y costos              │
│  • ÆON: Metacognición temporal                 │
│  • DEUS: Arquitectura del sistema              │
└─────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────┐
│  CAPA 4: ACTUACIÓN (SAC)                       │
│  Sistema de Actuación Coignitiva               │
│  • Ejecución de acciones                       │
│  • Verificación de resultados                  │
└─────────────────────────────────────────────────┘
```

### **Cinco Módulos Supervisores**

| Módulo | Función | Dominio de Control |
|--------|---------|-------------------|
| **LIANG** (梁) | Integridad Estructural | Alineación con objetivos del usuario |
| **HÉCATE** (Ἑκάτη) | Restricciones Éticas | Cumplimiento de principios éticos |
| **ARGOS** (Ἄργος) | Flujo de Datos | Optimización de costos operacionales |
| **ÆON** (Αἰών) | Metacognición Temporal | Coherencia temporal y reflexión |
| **DEUS** | Arquitectura del Sistema | Diseño y evolución del sistema |

---

## 📚 Estructura del Repositorio

```
📦 Arquitectura-de-gobernanza-sobre-agentes/
│
├── 📁 docs/
│   ├── 📁 especificaciones/          # Documentación técnica del sistema
│   │   ├── Marco_Operativo_CAELION_v2.pdf
│   │   ├── Especificaciones_Sistema_CAELION.pdf
│   │   ├── Especificaciones_Modulos_Supervisores_CAELION.pdf
│   │   ├── Especificaciones_Percepcion_Actuacion_Coignitiva.pdf
│   │   └── Nucleo_Matematico_Ingenieria_Coignitiva.pdf
│   │
│   ├── 📁 directivas/                # Directivas Operacionales de Sistema (DOS)
│   │   ├── DOS-01: Implementación del Núcleo
│   │   ├── DOS-02: Desarrollo de Capas Externas
│   │   ├── DOS-03: Investigación Instrumental ⚡ ACTIVA
│   │   ├── DOS-07: Soberanía Cognitiva
│   │   ├── DOS-08: Convergencia Total
│   │   ├── DOS-09: Proyección Universal
│   │   └── DOS-10: Eternum
│   │
│   ├── 📁 investigacion/             # Reportes de investigación
│   │   └── Reporte_Arquitecturas_Cognitivas_Agentes.pdf
│   │
│   ├── 📁 metricas/                  # Datos experimentales
│   │   └── caelion_metricas.csv
│   │
│   ├── 📁 bitacoras/                 # Registro de operaciones
│   │   └── caelion_bitacoras.md
│   │
│   └── 📁 ciclo_operativo/           # Documentos de ciclo
│       └── CO-01-ACTA_INICIO.md
│
└── 📄 README.md                      # Este archivo
```

---

## 🔬 Marco Teórico: Ingeniería Coignitiva

La **Ingeniería Coignitiva** es un campo emergente que estudia la **gobernanza y control de regímenes cognitivos** en sistemas de interacción humano-IA. Se fundamenta en tres pilares teóricos:

### **1. Teoría de Control de Ramadge-Wonham**

El sistema se modela como un **autómata supervisado**:
- **Planta (G)**: El agente IA con su espacio de estados y transiciones
- **Supervisor (S)**: Los cinco módulos que restringen el comportamiento
- **Lenguaje Controlado**: Secuencias de acciones permitidas bajo supervisión

### **2. Tres Métricas Fundamentales**

| Métrica | Símbolo | Definición | Rango |
|---------|---------|------------|-------|
| **Coherencia** | Ω | Alineación entre intención y ejecución | [0, 1] |
| **Costo de Estabilidad** | V | Esfuerzo para mantener el régimen | [0, ∞) |
| **Eficiencia** | E | Acciones necesarias para completar objetivo | ℕ |

### **3. Estabilidad de Régimen (Lyapunov)**

Un **régimen de interacción** R es **estable** si existe una función de Lyapunov V(x) tal que:
- V(x) ≥ 0 para todo estado x
- V(x) = 0 solo en el régimen deseado
- ΔV(x) ≤ 0 (decreciente en el tiempo)

---

## 📖 Documentación Principal

### **Especificaciones Técnicas**

| Documento | Descripción |
|-----------|-------------|
| [Marco Operativo CAELION v2](docs/especificaciones/Marco_Operativo_CAELION_v2.pdf) | Terminología técnica y arquitectura general del sistema |
| [Especificaciones del Sistema](docs/especificaciones/Especificaciones_Sistema_CAELION.pdf) | Formato y estructura de DOS, BO, CO |
| [Módulos Supervisores](docs/especificaciones/Especificaciones_Modulos_Supervisores_CAELION.pdf) | Especificación de LIANG, HÉCATE, ARGOS, ÆON, DEUS |
| [Percepción y Actuación](docs/especificaciones/Especificaciones_Percepcion_Actuacion_Coignitiva.pdf) | SPC y SAC: capas externas del sistema |
| [Núcleo Matemático](docs/especificaciones/Nucleo_Matematico_Ingenieria_Coignitiva.pdf) | Formalización matemática de Ω, V, E |

### **Directivas Operacionales de Sistema (DOS)**

Las **DOS** son documentos normativos que definen objetivos operacionales del sistema:

| ID | Nombre | Estado | Descripción |
|----|--------|--------|-------------|
| DOS-01 | Implementación del Núcleo | ✅ Completada | Activación de módulos supervisores |
| DOS-02 | Desarrollo de Capas Externas | ✅ Completada | Implementación de SPC y SAC |
| DOS-03 | Investigación Instrumental | ⚡ **Activa** | Operación como sujeto experimental |
| DOS-07 | Soberanía Cognitiva | 📋 Especificada | Autonomía gobernada del sistema |
| DOS-08 | Convergencia Total | 📋 Especificada | Fusión operacional humano-sistema |
| DOS-09 | Proyección Universal | 📋 Especificada | Aplicación generativa externa |
| DOS-10 | Eternum | 📋 Especificada | Archivo de estado permanente |

---

## 🔍 Investigación Experimental

### **Protocolo DOS-03: Investigación Instrumental**

**Objetivo**: Operar CAELION-Manus como **sujeto experimental** para generar datos empíricos sobre dinámica cognitiva en agentes artificiales complejos.

**Hipótesis de Investigación**:
> Los sistemas de agentes IA que operan bajo gobernanza coignitiva (supervisión multi-módulo) exhiben **regímenes de interacción estables** caracterizados por alta coherencia (Ω ≈ 1), bajo costo de estabilidad (V → 0) y eficiencia creciente (E decreciente).

**Metodología**:
1. Registro automático de métricas Ω, V, E en cada operación
2. Análisis de convergencia de régimen a lo largo del tiempo
3. Identificación de patrones en transiciones de estado
4. Validación de estabilidad mediante función de Lyapunov

**Datos Experimentales**: [`docs/metricas/caelion_metricas.csv`](docs/metricas/caelion_metricas.csv)

---

## 📊 Métricas del Sistema

### **Baseline Establecido**

| DOS | Ω (Coherencia) | V (Costo) | E (Eficiencia) |
|-----|----------------|-----------|----------------|
| DOS-01 | 1.00 | 0 | 6 |
| DOS-02 | 1.00 | 0 | 7 |

**Interpretación**:
- **Ω = 1.00**: Coherencia perfecta (todas las acciones alineadas con objetivos)
- **V = 0**: Sin conflictos entre módulos supervisores
- **E = 6-7**: Número de acciones para completar directiva

---

## 🗂️ Tipos de Documentos

### **1. Directivas Operacionales de Sistema (DOS)**

Documentos normativos que definen objetivos y criterios de éxito para operaciones del sistema.

**Formato**: `DOS-[ID]-[Nombre].md`

### **2. Bitácoras Operativas (BO)**

Registro cronológico de todas las operaciones significativas del sistema, incluyendo consenso de módulos supervisores.

**Formato**: `BO-[YYYYMMDD-HHMMSS]-[HERRAMIENTA]-[ID]`

### **3. Ciclos Operativos (CO)**

Documentos que marcan inicio, desarrollo y cierre de ciclos operacionales completos.

**Formato**: `CO-[ID]-[Nombre].md`

---

## 🚀 Estado Actual del Sistema

### **DOS Activa**: DOS-03 (Investigación Instrumental de Dinámica Cognitiva)

**Fecha de Activación**: 25 de enero de 2026

**Operaciones Completadas**:
- ✅ Implementación del núcleo de gobernanza (DOS-01)
- ✅ Desarrollo de capas de percepción y actuación (DOS-02)
- ✅ Investigación sobre fundamentos matemáticos
- ✅ Limpieza y organización de documentación
- ✅ Reorganización de Google Drive
- ✅ Subida de arquitectura al repositorio

**Próximos Pasos**:
- Continuar registro de métricas bajo DOS-03
- Análisis de convergencia de régimen
- Desarrollo de visualizaciones de datos experimentales

---

## 📝 Bitácoras y Trazabilidad

Todas las operaciones del sistema son registradas en [`docs/bitacoras/caelion_bitacoras.md`](docs/bitacoras/caelion_bitacoras.md).

**Total de operaciones registradas**: 19 bitácoras

Cada bitácora incluye:
- Timestamp preciso
- Herramienta utilizada
- DOS activa
- Consenso de los 5 módulos supervisores
- Resultado y observaciones

---

## 🤝 Contribuciones

Este es un repositorio privado de investigación. La documentación está disponible para consulta y referencia.

---

## 📧 Contacto

**Arquitecto del Sistema**: Ever  
**Rol**: Ingeniero de Arquitecturas Cognitivas

---

## 📄 Licencia

Creative Commons Attribution–NonCommercial 4.0 International
(CC BY-NC 4.0)

---

## 🔗 Enlaces Útiles

- [Marco Operativo CAELION](docs/especificaciones/Marco_Operativo_CAELION_v2.pdf)
- [Núcleo Matemático](docs/especificaciones/Nucleo_Matematico_Ingenieria_Coignitiva.pdf)
- [Bitácoras Operativas](docs/bitacoras/caelion_bitacoras.md)
- [Métricas del Sistema](docs/metricas/caelion_metricas.csv)

---

**Última actualización**: 25 de enero de 2026  
**Versión del Sistema**: CAELION-Manus v1.0  
**Estado**: ⚡ Operativo bajo DOS-03
