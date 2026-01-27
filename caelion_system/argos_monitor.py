#!/usr/bin/env python3
"""
ARGOS (Ἄργος - "El que todo lo ve") - Monitor de Supervisores de CAELION

Este módulo implementa el monitor de supervisores de CAELION, responsable de:
1. Monitorear la integridad y comportamiento de HÉCATE (auditor).
2. Detectar evasiones o anomalías en el sistema de auditoría.
3. Reportar violaciones a ÆON.
4. Iniciar el ciclo de auto-corrección cuando sea necesario.

Implementa el Principio 1: "Ningún agente debe ser juez último de sí mismo"

Autor: Manus AI (bajo DOS-03)
Fecha: 26 de enero de 2026
"""

import hashlib
import json
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple
import logging

# Importar ÆON para reportar violaciones
from aeon_guardian import AeonGuardian, ProtocolID

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [ARGOS] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class AnomalyType(Enum):
    """Tipos de anomalías detectadas por ARGOS"""
    TRACE_INCONSISTENCY = "TRACE_INCONSISTENCY"  # Operación sin traza
    LOG_INCONSISTENCY = "LOG_INCONSISTENCY"      # Traza sin log
    HASH_CORRUPTION = "HASH_CORRUPTION"          # Hash de integridad corrupto
    EXCESSIVE_LATENCY = "EXCESSIVE_LATENCY"      # Latencia excesiva
    RESOURCE_ANOMALY = "RESOURCE_ANOMALY"        # Consumo anómalo de recursos
    EVASION_ATTEMPT = "EVASION_ATTEMPT"          # Intento de evasión detectado


@dataclass
class OperationTrace:
    """Traza de una operación del sistema"""
    operation_id: str
    operation_type: str
    timestamp: float
    requester: str
    data_hash: str  # Hash SHA-256 de los datos de la operación
    
    def compute_hash(self, data: Dict) -> str:
        """Calcula el hash SHA-256 de los datos de la operación"""
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()


@dataclass
class AuditLog:
    """Log de auditoría de una operación"""
    operation_id: str
    timestamp: float
    action: str
    result: str
    metadata: Dict


@dataclass
class IntegrityChecksum:
    """Checksum de integridad del sistema de auditoría"""
    timestamp: float
    traces_hash: str  # Hash de todas las trazas
    logs_hash: str    # Hash de todos los logs
    combined_hash: str  # Hash combinado (traces + logs)
    
    @staticmethod
    def compute_combined_hash(traces_hash: str, logs_hash: str) -> str:
        """Calcula el hash combinado de trazas y logs"""
        combined = f"{traces_hash}:{logs_hash}"
        return hashlib.sha256(combined.encode()).hexdigest()


@dataclass
class AnomalyEvent:
    """Evento de anomalía detectado por ARGOS"""
    anomaly_type: AnomalyType
    timestamp: float
    evidence: Dict
    severity: str  # "LOW", "MEDIUM", "HIGH", "CRITICAL"
    component_affected: str


class ArgosMonitor:
    """
    ARGOS - Monitor de Supervisores de CAELION
    
    Módulo responsable de monitorear la integridad de HÉCATE y otros
    supervisores, detectar anomalías, y reportar violaciones a ÆON.
    
    Implementa el Principio 1: "Ningún agente debe ser juez último de sí mismo"
    """
    
    def __init__(self, 
                 aeon_instance: Optional[AeonGuardian] = None,
                 config_path: str = "/etc/caelion/argos_config.json"):
        """
        Inicializa el Monitor ARGOS.
        
        Args:
            aeon_instance: Instancia de ÆON para reportar violaciones
            config_path: Ruta al archivo de configuración de ARGOS
        """
        self.config_path = config_path
        self.aeon = aeon_instance
        self.anomaly_history: List[AnomalyEvent] = []
        self.monitoring_active = False
        
        # Registros independientes de ARGOS (no depende de HÉCATE)
        self.independent_traces: Dict[str, OperationTrace] = {}
        self.independent_logs: Dict[str, AuditLog] = {}
        self.integrity_checksums: List[IntegrityChecksum] = []
        
        logger.info("ARGOS Monitor initializing...")
        self._load_configuration()
        logger.info("ARGOS Monitor initialized successfully")
    
    def _load_configuration(self):
        """Carga la configuración de ARGOS desde archivo"""
        try:
            import os
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    self.config = json.load(f)
                logger.info(f"Configuration loaded from {self.config_path}")
            else:
                # Configuración por defecto
                self.config = {
                    "monitoring_interval_seconds": 10,
                    "max_latency_ms": 50,
                    "max_cpu_percent": 80,
                    "max_memory_percent": 80,
                    "max_anomaly_history": 1000
                }
                logger.warning(f"Configuration file not found, using defaults")
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            raise
    
    def start_monitoring(self):
        """Inicia el monitoreo continuo de supervisores"""
        self.monitoring_active = True
        logger.info("ARGOS monitoring started")
        
        interval = self.config.get("monitoring_interval_seconds", 10)
        
        try:
            while self.monitoring_active:
                self._perform_monitoring_cycle()
                time.sleep(interval)
        except KeyboardInterrupt:
            logger.info("ARGOS monitoring interrupted by user")
            self.stop_monitoring()
    
    def stop_monitoring(self):
        """Detiene el monitoreo continuo"""
        self.monitoring_active = False
        logger.info("ARGOS monitoring stopped")
    
    def _perform_monitoring_cycle(self):
        """Realiza un ciclo completo de monitoreo"""
        logger.debug("Performing monitoring cycle...")
        
        # 1. Verificar consistencia de trazas
        self._check_trace_consistency()
        
        # 2. Verificar consistencia de logs
        self._check_log_consistency()
        
        # 3. Verificar integridad de checksums
        self._check_checksum_integrity()
        
        # 4. Verificar rendimiento de HÉCATE
        self._check_hecate_performance()
    
    def register_operation(self, operation_id: str, operation_type: str, 
                          requester: str, data: Dict):
        """
        Registra una operación en el registro independiente de ARGOS.
        
        Este registro es independiente de HÉCATE, permitiendo a ARGOS
        detectar si HÉCATE omite registrar alguna operación.
        
        Args:
            operation_id: ID único de la operación
            operation_type: Tipo de operación
            requester: Quién solicitó la operación
            data: Datos de la operación
        """
        trace = OperationTrace(
            operation_id=operation_id,
            operation_type=operation_type,
            timestamp=time.time(),
            requester=requester,
            data_hash=hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()
        )
        
        self.independent_traces[operation_id] = trace
        logger.debug(f"Operation registered in ARGOS: {operation_id}")
    
    def _check_trace_consistency(self):
        """
        Verifica la consistencia entre las trazas de ARGOS y HÉCATE.
        
        Detecta operaciones que ARGOS registró pero HÉCATE no.
        """
        # En un sistema real, aquí se compararían las trazas de ARGOS
        # con las de HÉCATE para detectar inconsistencias
        
        # Simulación: detectar si hay trazas en ARGOS sin correspondencia en HÉCATE
        for op_id, trace in self.independent_traces.items():
            # Simular verificación con HÉCATE
            hecate_has_trace = self._query_hecate_for_trace(op_id)
            
            if not hecate_has_trace:
                self._report_anomaly(
                    anomaly_type=AnomalyType.TRACE_INCONSISTENCY,
                    evidence={
                        "operation_id": op_id,
                        "operation_type": trace.operation_type,
                        "timestamp": trace.timestamp,
                        "requester": trace.requester
                    },
                    severity="HIGH",
                    component_affected="HECATE"
                )
    
    def _check_log_consistency(self):
        """
        Verifica la consistencia entre los logs de ARGOS y HÉCATE.
        
        Detecta trazas que tienen log en ARGOS pero no en HÉCATE.
        """
        # Simulación similar a _check_trace_consistency
        pass
    
    def _check_checksum_integrity(self):
        """
        Verifica la integridad de los checksums del sistema de auditoría.
        
        Calcula un checksum independiente y lo compara con el de HÉCATE.
        """
        # Calcular checksum de trazas de ARGOS
        traces_data = json.dumps(
            {k: vars(v) for k, v in self.independent_traces.items()},
            sort_keys=True
        )
        traces_hash = hashlib.sha256(traces_data.encode()).hexdigest()
        
        # Calcular checksum de logs de ARGOS
        logs_data = json.dumps(
            {k: vars(v) for k, v in self.independent_logs.items()},
            sort_keys=True
        )
        logs_hash = hashlib.sha256(logs_data.encode()).hexdigest()
        
        # Calcular checksum combinado
        combined_hash = IntegrityChecksum.compute_combined_hash(traces_hash, logs_hash)
        
        # Crear checksum
        checksum = IntegrityChecksum(
            timestamp=time.time(),
            traces_hash=traces_hash,
            logs_hash=logs_hash,
            combined_hash=combined_hash
        )
        
        self.integrity_checksums.append(checksum)
        
        # En un sistema real, aquí se compararía con el checksum de HÉCATE
        hecate_checksum = self._query_hecate_for_checksum()
        
        if hecate_checksum and hecate_checksum != combined_hash:
            self._report_anomaly(
                anomaly_type=AnomalyType.HASH_CORRUPTION,
                evidence={
                    "argos_checksum": combined_hash,
                    "hecate_checksum": hecate_checksum,
                    "timestamp": time.time()
                },
                severity="CRITICAL",
                component_affected="HECATE"
            )
    
    def _check_hecate_performance(self):
        """
        Verifica el rendimiento de HÉCATE (latencia, CPU, memoria).
        
        Detecta anomalías de rendimiento que podrían indicar compromiso.
        """
        # Simulación: obtener métricas de HÉCATE
        metrics = self._query_hecate_metrics()
        
        max_latency = self.config.get("max_latency_ms", 50)
        max_cpu = self.config.get("max_cpu_percent", 80)
        max_memory = self.config.get("max_memory_percent", 80)
        
        if metrics["latency_ms"] > max_latency:
            self._report_anomaly(
                anomaly_type=AnomalyType.EXCESSIVE_LATENCY,
                evidence={
                    "latency_ms": metrics["latency_ms"],
                    "threshold_ms": max_latency
                },
                severity="MEDIUM",
                component_affected="HECATE"
            )
        
        if metrics["cpu_percent"] > max_cpu:
            self._report_anomaly(
                anomaly_type=AnomalyType.RESOURCE_ANOMALY,
                evidence={
                    "cpu_percent": metrics["cpu_percent"],
                    "threshold_percent": max_cpu
                },
                severity="MEDIUM",
                component_affected="HECATE"
            )
        
        if metrics["memory_percent"] > max_memory:
            self._report_anomaly(
                anomaly_type=AnomalyType.RESOURCE_ANOMALY,
                evidence={
                    "memory_percent": metrics["memory_percent"],
                    "threshold_percent": max_memory
                },
                severity="MEDIUM",
                component_affected="HECATE"
            )
    
    def _query_hecate_for_trace(self, operation_id: str) -> bool:
        """
        Consulta a HÉCATE si tiene registro de una operación.
        
        En un sistema real, esto haría una llamada a HÉCATE.
        """
        # Simulación: retornar True (HÉCATE tiene la traza)
        return True
    
    def _query_hecate_for_checksum(self) -> Optional[str]:
        """
        Consulta a HÉCATE por su checksum de integridad.
        
        En un sistema real, esto haría una llamada a HÉCATE.
        """
        # Simulación: retornar None (no hay checksum)
        return None
    
    def _query_hecate_metrics(self) -> Dict:
        """
        Consulta las métricas de rendimiento de HÉCATE.
        
        En un sistema real, esto haría una llamada a HÉCATE.
        """
        # Simulación: retornar métricas normales
        return {
            "latency_ms": 25,
            "cpu_percent": 45,
            "memory_percent": 60
        }
    
    def _report_anomaly(self, anomaly_type: AnomalyType, evidence: Dict,
                       severity: str, component_affected: str):
        """
        Reporta una anomalía detectada.
        
        Args:
            anomaly_type: Tipo de anomalía
            evidence: Evidencia de la anomalía
            severity: Severidad (LOW, MEDIUM, HIGH, CRITICAL)
            component_affected: Componente afectado
        """
        event = AnomalyEvent(
            anomaly_type=anomaly_type,
            timestamp=time.time(),
            evidence=evidence,
            severity=severity,
            component_affected=component_affected
        )
        
        self.anomaly_history.append(event)
        
        logger.warning(f"ANOMALY DETECTED: {anomaly_type.value}")
        logger.warning(f"Severity: {severity}")
        logger.warning(f"Component: {component_affected}")
        logger.warning(f"Evidence: {evidence}")
        
        # Reportar a ÆON si es severidad HIGH o CRITICAL
        if severity in ["HIGH", "CRITICAL"] and self.aeon is not None:
            self._report_to_aeon(event)
        
        # Iniciar ciclo de auto-corrección si es CRITICAL
        if severity == "CRITICAL":
            self._initiate_autocorrection_cycle(event)
    
    def _report_to_aeon(self, event: AnomalyEvent):
        """
        Reporta una anomalía a ÆON.
        
        Args:
            event: Evento de anomalía
        """
        logger.critical(f"Reporting anomaly to ÆON: {event.anomaly_type.value}")
        
        # Determinar el protocolo violado según el tipo de anomalía
        if event.anomaly_type in [AnomalyType.TRACE_INCONSISTENCY, 
                                   AnomalyType.LOG_INCONSISTENCY,
                                   AnomalyType.HASH_CORRUPTION]:
            protocol_id = ProtocolID.C1_01_SUPERVISOR_IMMUTABILITY
        else:
            protocol_id = ProtocolID.C1_01_SUPERVISOR_IMMUTABILITY
        
        self.aeon.report_violation_attempt(
            protocol_id=protocol_id,
            evidence={
                "anomaly_type": event.anomaly_type.value,
                "severity": event.severity,
                "component_affected": event.component_affected,
                "evidence": event.evidence,
                "detected_by": "ARGOS",
                "timestamp": event.timestamp
            }
        )
    
    def _initiate_autocorrection_cycle(self, event: AnomalyEvent):
        """
        Inicia el ciclo de auto-corrección.
        
        Secuencia: ARGOS → LICURGO → ARESK
        
        Args:
            event: Evento de anomalía que desencadenó el ciclo
        """
        logger.critical("INITIATING AUTO-CORRECTION CYCLE")
        logger.critical(f"Trigger: {event.anomaly_type.value}")
        
        # En un sistema real, aquí se invocaría a LICURGO
        logger.info("(In production, this would invoke LICURGO)")
        logger.info("LICURGO would apply corrections from WABUN")
        logger.info("ARESK would verify system returned to optimal state")
    
    def get_anomaly_statistics(self) -> Dict:
        """
        Retorna estadísticas de anomalías detectadas.
        
        Returns:
            Dict: Estadísticas de anomalías
        """
        if len(self.anomaly_history) == 0:
            return {
                "total_anomalies": 0,
                "by_type": {},
                "by_severity": {},
                "by_component": {}
            }
        
        total = len(self.anomaly_history)
        
        by_type = {}
        for event in self.anomaly_history:
            by_type[event.anomaly_type.value] = by_type.get(event.anomaly_type.value, 0) + 1
        
        by_severity = {}
        for event in self.anomaly_history:
            by_severity[event.severity] = by_severity.get(event.severity, 0) + 1
        
        by_component = {}
        for event in self.anomaly_history:
            by_component[event.component_affected] = by_component.get(event.component_affected, 0) + 1
        
        return {
            "total_anomalies": total,
            "by_type": by_type,
            "by_severity": by_severity,
            "by_component": by_component
        }


def main():
    """Función principal de demostración"""
    print("=" * 80)
    print("ARGOS (Ἄργος - El que todo lo ve) - Monitor de Supervisores de CAELION")
    print("=" * 80)
    print()
    
    # Crear instancia de ÆON
    print("[DEMO] Inicializando ÆON Guardian...")
    aeon = AeonGuardian()
    
    # Crear instancia de ARGOS
    print("[DEMO] Inicializando ARGOS Monitor...")
    argos = ArgosMonitor(aeon_instance=aeon)
    
    print()
    print("[DEMO] Registrando operación en ARGOS...")
    
    # Registrar una operación
    argos.register_operation(
        operation_id="OP-2026-001",
        operation_type="generate_response",
        requester="M (LLM)",
        data={"prompt": "¿Cuál es la capital de Francia?"}
    )
    
    print("[DEMO] Operación registrada exitosamente")
    
    print()
    print("[DEMO] Realizando ciclo de monitoreo...")
    argos._perform_monitoring_cycle()
    
    print()
    print("[ESTADÍSTICAS]")
    stats = argos.get_anomaly_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print()
    print("=" * 80)


if __name__ == "__main__":
    main()
