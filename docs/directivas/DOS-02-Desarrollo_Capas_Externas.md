# Directiva Operacional 02: Desarrollo de Capas Externas

**Documento ID**: `CAELION-MANUS-DOS-02-SPEC-V1.0`  
**Ciclo Operativo Asociado**: CO-01 (Integración Manus-CAELION)  
**Fecha de Activación**: 25 de enero de 2026

---

## 1. Identificación

- **ID_Directiva**: `02`
- **Nombre_Clave**: `Desarrollo_Capas_Externas`

---

## 2. Campos de Datos

| Campo | Valor para DOS-02 |
| :--- | :--- |
| **ID_Directiva** | `02` |
| **Nombre_Clave** | `Desarrollo_Capas_Externas` |
| **Descripción_Técnica** | Implementar las capas de Percepción y Actuación para completar la arquitectura de cuatro capas. Esto implica desarrollar un **Sistema de Percepción Coignitiva (SPC)** para la entrada de información y un **Sistema de Actuación Coignitiva (SAC)** para la salida, ambos operando con bucles de retroalimentación con el núcleo CAELION. |
| **Condición_Inicio** | `DOS-01-Implementacion_Nucleo_Gobernanza` completada. El sistema de logs y el protocolo de consenso están operativos. |
| **Módulos_Supervisores** | **LIANG** (planificación), **ARESK** (ejecución), **WABUN** (registro) |
| **Resultado_Esperado** | El sistema CAELION-Manus evoluciona de un sistema de gobernanza interno a un organismo coignitivo completo, capaz de percepción activa y actuación con auto-corrección. |

---

## 3. Objetivos Específicos de la DOS-02

### **3.1. Implementación del Sistema de Percepción Coignitiva (SPC)**

-   **Objetivo**: Pasar de una percepción pasiva (entrada de usuario) a una **percepción activa e intencionada**.
-   **Mecanismo**: Utilizar la herramienta `schedule` para programar búsquedas (`search`) periódicas y proactivas.
-   **Flujo de Integración**:
    1.  **LIANG** (mi herramienta `plan`) definirá una "Intención Perceptiva" como parte de una tarea de investigación.
    2.  Esta intención se traducirá en una llamada a `schedule` para ejecutar `search` a intervalos definidos.
    3.  Los resultados de `search` serán analizados y registrados por **WABUN** en las bitácoras.

### **3.2. Implementación del Sistema de Actuación Coignitiva (SAC)**

-   **Objetivo**: Pasar de una actuación "a ciegas" a una **actuación con retroalimentación y auto-corrección**.
-   **Mecanismo**: Añadir un paso de verificación explícito después de cada acción de escritura o modificación.
-   **Flujo de Integración**:
    1.  **ARESK** (mi bucle de agente) ejecutará una herramienta de modificación (ej. `file(action=\'write\')`).
    2.  Inmediatamente después, el **SAC** (implementado como un nuevo paso en mi lógica) usará una herramienta de lectura (ej. `file(action=\'read\')` o `shell(command=\'ls -l\')`) para verificar que la acción tuvo el resultado esperado.
    3.  Si hay una discrepancia, se registrará una alerta de **ARGOS** (costo inesperado) y **LIANG** recalculará el siguiente paso.

---

## 4. Especificaciones de Integración

### **4.1. Integración del SPC**

| Módulo CAELION | Herramienta Manus | Rol en el SPC |
| :--- | :--- | :--- |
| **LIANG** | `plan` | Define la "Intención Perceptiva" (qué buscar y por qué). |
| **ARESK** | `schedule` + `search` | Ejecuta la percepción activa programando búsquedas proactivas. |
| **WABUN** | `file(action=\'append\')` | Registra los resultados de la percepción en `caelion_bitacoras.md`. |

**Ejemplo de Implementación**:
Si una tarea requiere monitorear noticias sobre "Ingeniería Coignitiva", LIANG lo definirá en el plan. ARESK usará `schedule` para ejecutar `search(queries=["Ingeniería Coignitiva"])` cada 24 horas. WABUN registrará los nuevos hallazgos.

### **4.2. Integración del SAC**

| Módulo CAELION | Herramienta Manus | Rol en el SAC |
| :--- | :--- | :--- |
| **ARESK** | `file`, `shell` | Ejecuta la acción de modificación. |
| **SAC (Verificación)** | `file(action=\'read\')`, `shell` | Verifica el resultado de la acción. |
| **ARGOS** | Lógica interna | Detecta discrepancias entre el resultado esperado y el real, generando una alerta de "costo inesperado". |

**Ejemplo de Implementación**:
1.  **ARESK** ejecuta `file(action=\'write\', path=\'/home/ubuntu/test.txt\', text=\'hola\')`.
2.  **SAC** ejecuta `file(action=\'read\', path=\'/home/ubuntu/test.txt\')`.
3.  La lógica interna compara el contenido leído ("hola") con el contenido esperado. Si coincide, la operación es exitosa. Si no, se registra una alerta.

---

## 5. Criterios de Finalización de la DOS-02

La DOS-02 se considerará completada cuando el sistema haya demostrado exitosamente:

1.  **Una instancia de Percepción Activa**: Haber utilizado `schedule` y `search` para una tarea de monitoreo proactivo, registrando los resultados.
2.  **Una instancia de Actuación con Retroalimentación**: Haber ejecutado una acción de modificación y verificado su resultado exitosamente en un paso posterior, registrando ambos pasos en las bitácoras.

**Transición**: Habilita la `DOS-03: Operación en Simbiosis`, donde el sistema comenzará a utilizar estas nuevas capacidades para resolver tareas del usuario de manera más autónoma y robusta.

---

**Estado Actual**: ⏳ **En Progreso**
