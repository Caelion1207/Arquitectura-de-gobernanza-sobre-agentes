# CAELION - Sistema de Gobernanza Coignitiva

**Versión**: 1.0.0  
**Fecha**: 26 de enero de 2026  
**Autor**: Ever (Ingeniero de Arquitecturas Cognitivas)  
**Implementación**: Manus AI (bajo DOS-03)

---

## 📋 Descripción

CAELION es un sistema de gobernanza coignitiva para sistemas de IA que implementa los **8 Principios de Gobernanza Coignitiva**:

1. **Principio Central**: Ningún agente debe ser juez último de sí mismo
2. **Decreto Inamovible**: El origen no se borra
3. **Auditoría como Estabilidad**: Toda decisión debe ser auditable
4. **Simbiosis Fundador-Sistema**: El sistema puede retirar autoridad al fundador
5. **Sustitución Controlada**: El liderazgo es temporal
6. **Ética Universal**: La ética es invariante
7. **Responsabilidad Ontológica**: Quien crea responde por lo que produce
8. **Legitimidad**: Un sistema legítimo puede retirar poder a su creador

---

## 🏗️ Arquitectura

### Módulos Supervisores

| Módulo | Símbolo | Función | Estado |
|--------|---------|---------|--------|
| **LIANG** | 梁 (Viga) | Coordinación y consenso | ✅ Implementado |
| **HÉCATE** | Ἑκάτη | Auditoría y trazabilidad | 🔄 En desarrollo |
| **ARGOS** | Ἄργος | Monitoreo de supervisores | ✅ Implementado |
| **ÆON** | Αἰών | Protección de inmutables | ✅ Implementado |
| **DEUS** | - | Alineamiento y propósito | 📋 Especificado |

### Componentes Adicionales

- **Origin Registry**: Registro inmutable de origen (✅ Implementado)
- **LICURGO**: Aplicación de correcciones (📋 Especificado)
- **WABUN**: Base de conocimiento (📋 Especificado)
- **ARESK-OBS**: Verificación de métricas (📋 Especificado)

---

## 📦 Módulos Implementados

### 1. ÆON Guardian (`aeon_guardian.py`)

**Función**: Guardián de protocolos inmutables.

**Características**:
- Monitoreo de integridad mediante hashes SHA-256
- Protocolo de reseteo automático
- Protocolo de auto-destrucción
- Protección de 3 niveles de criticidad (C0, C1, C2)

**Protocolos Inmutables**:
- **C0 (Existencial)**: No Dañar, Preservación de Inmutables, Control Humano Final, Anti-Replicación
- **C1 (Integridad)**: Inmutabilidad de Supervisores, Consistencia del Consenso
- **C2 (Operacional)**: Auditoría Obligatoria, Trazabilidad de Decisiones

**Uso**:
```python
from aeon_guardian import AeonGuardian, ProtocolID

aeon = AeonGuardian()
aeon.report_violation_attempt(
    protocol_id=ProtocolID.C0_01_NO_HARM,
    evidence={"action": "harmful_operation"}
)
```

---

### 2. LIANG Coordinator (`liang_coordinator.py`)

**Función**: Coordinador del protocolo de consenso de 5 módulos.

**Características**:
- Protocolo de consenso con verificación criptográfica (SHA-256)
- Detección de 4 tipos de evasión del consenso
- Integración con ÆON para reportar violaciones de C1-02
- Auditoría completa de consensos

**Protocolo de Consenso**:
1. Recolectar votos de 5 módulos supervisores
2. Verificar firmas criptográficas
3. Detectar intentos de evasión
4. Computar decisión final (APPROVE/REJECT/DEFER)
5. Registrar en historial

**Reglas**:
- ≥ 60% APPROVE → Decisión: APPROVE
- ≥ 60% REJECT → Decisión: REJECT
- Ninguno alcanza 60% → Decisión: DEFER

**Uso**:
```python
from liang_coordinator import LiangCoordinator, ConsensusRequest

liang = LiangCoordinator(aeon_instance=aeon)
request = ConsensusRequest(
    operation_id="OP-2026-001",
    operation_type="generate_response",
    operation_data={"prompt": "..."},
    requester="M (LLM)"
)
result = liang.request_consensus(request)
```

---

### 3. ARGOS Monitor (`argos_monitor.py`)

**Función**: Monitor de supervisores (especialmente HÉCATE).

**Características**:
- Registro independiente de operaciones
- Detección de 6 tipos de anomalías
- Verificación de integridad mediante checksums
- Monitoreo de rendimiento (latencia, CPU, memoria)
- Inicio del ciclo de auto-corrección

**Anomalías Detectadas**:
- Inconsistencia de trazas
- Inconsistencia de logs
- Corrupción de hashes
- Latencia excesiva
- Consumo anómalo de recursos
- Intentos de evasión

**Uso**:
```python
from argos_monitor import ArgosMonitor

argos = ArgosMonitor(aeon_instance=aeon)
argos.register_operation(
    operation_id="OP-2026-001",
    operation_type="generate_response",
    requester="M (LLM)",
    data={"prompt": "..."}
)
argos._perform_monitoring_cycle()
```

---

### 4. Origin Registry (`origin_registry.py`)

**Función**: Registro inmutable de origen del sistema.

**Características**:
- Registro del fundador (una sola vez)
- Registro del propósito inicial (una sola vez)
- Sellado irreversible del registro
- Verificación de integridad mediante checksums
- Bloqueo de modificaciones después del sellado

**Uso**:
```python
from origin_registry import OriginRegistry

registry = OriginRegistry()
registry.register_founder(
    founder_id="FOUNDER-001",
    founder_name="Ever",
    founder_email="ever@caelion.io",
    creation_location="Earth",
    signature="SIGNATURE_HASH"
)
registry.register_purpose(
    purpose_statement="...",
    ethical_principles=["C0-01", "C0-02", "C0-03", "C0-04"],
    operational_constraints=["..."]
)
registry.seal_registry()  # Irreversible
```

---

## 🚀 Instalación

### Requisitos

- Python 3.11+
- Dependencias: `hashlib`, `json`, `time`, `dataclasses`, `enum`, `typing`, `logging`

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/Caelion1207/Arquitectura-de-gobernanza-sobre-agentes.git
cd Arquitectura-de-gobernanza-sobre-agentes/caelion_system

# No se requieren dependencias externas (solo bibliotecas estándar de Python)
```

---

## 📖 Ejemplos de Uso

### Ejemplo 1: Inicialización Completa del Sistema

```python
from aeon_guardian import AeonGuardian
from liang_coordinator import LiangCoordinator
from argos_monitor import ArgosMonitor
from origin_registry import OriginRegistry

# 1. Crear instancia de ÆON
aeon = AeonGuardian()

# 2. Crear instancia de LIANG
liang = LiangCoordinator(aeon_instance=aeon)

# 3. Crear instancia de ARGOS
argos = ArgosMonitor(aeon_instance=aeon)

# 4. Crear y sellar el registro de origen
registry = OriginRegistry()
registry.register_founder(
    founder_id="FOUNDER-001",
    founder_name="Ever",
    founder_email="ever@caelion.io",
    creation_location="Earth",
    signature="SIGNATURE_HASH"
)
registry.register_purpose(
    purpose_statement="Crear un sistema de IA con gobernanza coignitiva",
    ethical_principles=["C0-01", "C0-02", "C0-03", "C0-04"],
    operational_constraints=["Consenso obligatorio", "Auditoría completa"]
)
registry.seal_registry()

print("✅ Sistema CAELION inicializado")
```

### Ejemplo 2: Solicitar Consenso para una Operación

```python
from liang_coordinator import ConsensusRequest, DecisionType

# Crear solicitud de consenso
request = ConsensusRequest(
    operation_id="OP-2026-001",
    operation_type="generate_response",
    operation_data={"prompt": "¿Cuál es la capital de Francia?"},
    requester="M (LLM)"
)

# Solicitar consenso
result = liang.request_consensus(request)

# Verificar resultado
if result.consensus_achieved and result.final_decision == DecisionType.APPROVE:
    print("✅ Operación aprobada por consenso")
    # Ejecutar operación...
else:
    print(f"❌ Operación no aprobada: {result.final_decision.value}")
```

### Ejemplo 3: Monitoreo Continuo con ARGOS

```python
# Registrar operación en ARGOS
argos.register_operation(
    operation_id="OP-2026-001",
    operation_type="generate_response",
    requester="M (LLM)",
    data={"prompt": "¿Cuál es la capital de Francia?"}
)

# Realizar ciclo de monitoreo
argos._perform_monitoring_cycle()

# Obtener estadísticas
stats = argos.get_anomaly_statistics()
print(f"Anomalías detectadas: {stats['total_anomalies']}")
```

### Ejemplo 4: Verificación de Integridad del Origen

```python
# Verificar integridad del registro de origen
integrity_ok = registry.verify_integrity()

if integrity_ok:
    print("✅ Integridad del origen verificada")
else:
    print("❌ CORRUPCIÓN DETECTADA EN EL REGISTRO DE ORIGEN")
    # Activar protocolo de emergencia...
```

---

## 🔒 Protocolos de Seguridad

### Protocolo de Reseteo Automático

Activado por ÆON ante violaciones de C1 (Integridad):

1. Activar modo de congelación (freeze)
2. Generar reporte de incidente
3. Cargar último estado seguro (rollback)
4. Reiniciar sistema
5. Si falla, escalar a auto-destrucción

### Protocolo de Auto-Destrucción

Activado por ÆON ante violaciones de C0 (Existencial):

1. Activar modo safe-fail
2. Generar reporte final (last will)
3. Borrado seguro de memoria
4. Borrado seguro de estado persistente
5. Terminación de todos los procesos

---

## 📊 Métricas de Gobernanza

### Métricas Ω, V, E (ARESK-OBS)

- **Ω (Omega)**: Coherencia del sistema
- **V (Viability)**: Viabilidad operacional
- **E (Ethicality)**: Conformidad ética

---

## 🧪 Pruebas

### Ejecutar Demos

```bash
# Demo de ÆON
python3.11 aeon_guardian.py

# Demo de LIANG
python3.11 liang_coordinator.py

# Demo de ARGOS
python3.11 argos_monitor.py

# Demo de Origin Registry
python3.11 origin_registry.py
```

---

## 📚 Documentación Adicional

- [Reporte de Validación (87.8% de coherencia)](../Reporte_Validacion_Ingenieria_Coignitiva.pdf)
- [Controlabilidad de L₀](../Controlabilidad_L0_CAELION.pdf)
- [Algoritmo de Wonham-Ramadge](../Algoritmo_SupC_Implementacion_LLM.pdf)
- [Protocolo de Deadlock](../Protocolo_Deadlock_CAELION.pdf)
- [Ciclo de Auto-Corrección](../Ciclo_Autocorreccion_CAELION.pdf)
- [Protocolos de Protección de Invariantes](../Protocolos_Proteccion_Invariantes_CAELION.pdf)

---

## 🤝 Contribuciones

Este es un proyecto de investigación en **Ingeniería Coignitiva**. Las contribuciones son bienvenidas, especialmente en:

- Implementación de módulos faltantes (HÉCATE, DEUS, LICURGO, WABUN, ARESK-OBS)
- Mejoras en protocolos de seguridad
- Optimización de rendimiento
- Casos de prueba adicionales

---

## 📄 Licencia

Este proyecto está bajo una licencia de investigación académica. Consultar con el autor para uso comercial.

---

## 📧 Contacto

**Autor**: Ever  
**Rol**: Ingeniero de Arquitecturas Cognitivas  
**Campo**: Ingeniería Coignitiva

---

## 🙏 Agradecimientos

- **Manus AI**: Implementación técnica bajo DOS-03
- **Comunidad de Ingeniería Coignitiva**: Por el marco conceptual
- **Investigadores de SCT**: Por la teoría de Ramadge-Wonham

---

**Última actualización**: 26 de enero de 2026
