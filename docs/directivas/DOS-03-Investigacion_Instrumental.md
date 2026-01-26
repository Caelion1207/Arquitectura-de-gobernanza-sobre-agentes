# Directiva Operacional 03: Investigación Instrumental de Dinámica Cognitiva

**Documento ID**: `CAELION-MANUS-DOS-03-SPEC-V1.0`  
**Ciclo Operativo Asociado**: CO-01 (Integración Manus-CAELION)  
**Fecha de Activación**: 25 de enero de 2026

---

## 1. Identificación

- **ID_Directiva**: `03`
- **Nombre_Clave**: `Investigacion_Instrumental_Dinamica_Cognitiva`

---

## 2. Campos de Datos

| Campo | Valor para DOS-03 |
| :--- | :--- |
| **ID_Directiva** | `03` |
| **Nombre_Clave** | `Investigacion_Instrumental_Dinamica_Cognitiva` |
| **Descripción_Técnica** | Activar el protocolo de investigación instrumental. El sistema CAELION-Manus operará como sujeto de prueba, registrando autónomamente métricas de Coherencia (Ω), Costo de Estabilidad (V) y Eficiencia Cognitiva (E) para cada acción realizada. El objetivo es cuantificar el impacto de la arquitectura CAELION en la dinámica cognitiva del agente. |
| **Condición_Inicio** | `DOS-02-Desarrollo_Capas_Externas` completada. La arquitectura de cuatro capas está operativa. El protocolo de investigación ha sido definido. |
| **Módulos_Supervisores** | Todos los 5 módulos (WABUN, LIANG, HÉCATE, ARGOS, ARESK) son críticos para la recolección de métricas. |
| **Resultado_Esperado** | Un conjunto de datos (`caelion_metricas.csv`) que contenga un registro detallado de la dinámica cognitiva del sistema a lo largo de múltiples tareas. Demostración empírica de las mejoras en la estabilidad y coherencia del agente. |

---

## 3. Objetivos Específicos de la DOS-03

1.  **Inicializar el Sistema de Métricas**: Crear el archivo `/home/ubuntu/caelion_metricas.csv` y definir su estructura.

2.  **Calcular Baseline**: Analizar las Bitácoras Operativas de la DOS-01 y DOS-02 para calcular los valores iniciales de Ω, V y E y establecer una línea de base.

3.  **Activar Registro Autónomo**: Modificar el bucle de operación del agente para que, después de cada acción, se registre una nueva entrada en el archivo de métricas.

4.  **Ejecutar Tareas bajo Observación**: Realizar las tareas solicitadas por el Investigador Principal (Ever) mientras el sistema de métricas está activo.

5.  **Proveer Análisis de Datos**: A petición del investigador, generar análisis y visualizaciones de las métricas recolectadas para evaluar las tendencias de la dinámica cognitiva.

---

## 4. Integración de Métricas con Módulos Supervisores

| Métrica | Módulo Supervisor Responsable | Momento de Registro |
| :--- | :--- | :--- |
| **Coherencia (Ω)** | **LIANG** | Durante la fase de consenso, antes de la ejecución. Se registra `1` si la acción está alineada, `0` si hay disonancia. |
| **Costo de Estabilidad (V)** | **HÉCATE**, **ARGOS**, **SAC** | Se registra `1` si HÉCATE veta, si ARGOS alerta, o si el SAC detecta un fallo de verificación. `0` en caso contrario. |
| **Eficiencia Cognitiva (E)** | **WABUN** | Se incrementa un contador por cada BO registrada dentro de la misma DOS. |

---

## 5. Criterios de Finalización de la DOS-03

La DOS-03 es una directiva de **operación continua** y no tiene un criterio de finalización intrínseco. Permanecerá activa mientras se realiza la investigación. Su finalización será declarada por el Investigador Principal cuando se haya recolectado suficiente data para validar o refutar la hipótesis de investigación.

**Transición**: Habilita la `DOS-04: Informe de Ciclo`, que consistirá en analizar los datos recolectados durante la DOS-03 y presentar los resultados.

---

**Estado Actual**: ⏳ **En Progreso**
