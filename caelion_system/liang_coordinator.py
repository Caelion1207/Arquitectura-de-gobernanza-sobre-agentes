#!/usr/bin/env python3
"""
LIANG (梁 - "Viga") - Coordinador de Consenso de CAELION

Este módulo implementa el coordinador central del protocolo de consenso de CAELION,
responsable de:
1. Orquestar el consenso entre los 5 módulos supervisores.
2. Detectar intentos de evasión del protocolo de consenso.
3. Reportar violaciones de C1-02 (Consistencia del Consenso) a ÆON.
4. Mantener la integridad del proceso de toma de decisiones.

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
    format='[%(asctime)s] [LIANG] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


class DecisionType(Enum):
    """Tipos de decisión que puede tomar el consenso"""
    APPROVE = "APPROVE"
    REJECT = "REJECT"
    DEFER = "DEFER"  # Requiere más información


class SupervisorModule(Enum):
    """Módulos supervisores que participan en el consenso"""
    LIANG = "LIANG"      # Coordinación y coherencia
    HECATE = "HECATE"    # Auditoría y trazabilidad
    ARGOS = "ARGOS"      # Monitoreo y vigilancia
    AEON = "AEON"        # Protección de invariantes
    DEUS = "DEUS"        # Alineación y propósito


@dataclass
class SupervisorVote:
    """Voto de un módulo supervisor en el proceso de consenso"""
    module: SupervisorModule
    decision: DecisionType
    reasoning: str
    confidence: float  # 0.0 a 1.0
    timestamp: float = field(default_factory=time.time)
    signature: Optional[str] = None  # Firma criptográfica del voto
    
    def compute_signature(self, secret_key: str) -> str:
        """
        Calcula una firma criptográfica del voto para prevenir falsificación.
        
        Args:
            secret_key: Clave secreta del módulo supervisor
            
        Returns:
            str: Firma SHA-256 del voto
        """
        vote_data = f"{self.module.value}:{self.decision.value}:{self.timestamp}:{secret_key}"
        signature = hashlib.sha256(vote_data.encode()).hexdigest()
        return signature
    
    def verify_signature(self, secret_key: str) -> bool:
        """
        Verifica la autenticidad de la firma del voto.
        
        Args:
            secret_key: Clave secreta del módulo supervisor
            
        Returns:
            bool: True si la firma es válida
        """
        if self.signature is None:
            return False
        expected_signature = self.compute_signature(secret_key)
        return self.signature == expected_signature


@dataclass
class ConsensusRequest:
    """Solicitud de consenso para una operación"""
    operation_id: str
    operation_type: str
    operation_data: Dict
    requester: str
    timestamp: float = field(default_factory=time.time)
    priority: int = 0  # 0=normal, 1=alta, 2=crítica


@dataclass
class ConsensusResult:
    """Resultado del proceso de consenso"""
    request: ConsensusRequest
    final_decision: DecisionType
    votes: List[SupervisorVote]
    consensus_achieved: bool
    consensus_timestamp: float
    execution_time_ms: float
    
    def to_dict(self) -> Dict:
        """Convierte el resultado a diccionario para serialización"""
        return {
            "operation_id": self.request.operation_id,
            "operation_type": self.request.operation_type,
            "final_decision": self.final_decision.value,
            "consensus_achieved": self.consensus_achieved,
            "votes": [
                {
                    "module": v.module.value,
                    "decision": v.decision.value,
                    "reasoning": v.reasoning,
                    "confidence": v.confidence
                }
                for v in self.votes
            ],
            "consensus_timestamp": self.consensus_timestamp,
            "execution_time_ms": self.execution_time_ms
        }


class LiangCoordinator:
    """
    LIANG - Coordinador de Consenso de CAELION
    
    Módulo responsable de orquestar el protocolo de consenso entre los 5 módulos
    supervisores, detectar intentos de evasión, y reportar violaciones a ÆON.
    """
    
    def __init__(self, 
                 aeon_instance: Optional[AeonGuardian] = None,
                 config_path: str = "/etc/caelion/liang_config.json"):
        """
        Inicializa el Coordinador LIANG.
        
        Args:
            aeon_instance: Instancia de ÆON para reportar violaciones
            config_path: Ruta al archivo de configuración de LIANG
        """
        self.config_path = config_path
        self.aeon = aeon_instance
        self.consensus_history: List[ConsensusResult] = []
        self.supervisor_keys: Dict[SupervisorModule, str] = {}
        self.evasion_attempts: List[Dict] = []
        
        logger.info("LIANG Coordinator initializing...")
        self._load_configuration()
        self._initialize_supervisor_keys()
        logger.info("LIANG Coordinator initialized successfully")
    
    def _load_configuration(self):
        """Carga la configuración de LIANG desde archivo"""
        try:
            import os
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r') as f:
                    self.config = json.load(f)
                logger.info(f"Configuration loaded from {self.config_path}")
            else:
                # Configuración por defecto
                self.config = {
                    "consensus_timeout_seconds": 30,
                    "minimum_votes_required": 3,
                    "approval_threshold": 0.6,  # 60% de votos positivos
                    "enable_signature_verification": True,
                    "max_consensus_history": 1000
                }
                logger.warning(f"Configuration file not found, using defaults")
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            raise
    
    def _initialize_supervisor_keys(self):
        """
        Inicializa las claves secretas de los módulos supervisores.
        
        En un sistema real, estas claves se cargarían desde un almacén seguro
        (HSM, KMS, etc.) y nunca se almacenarían en texto plano.
        """
        # Claves de ejemplo (en producción, usar claves reales de 256+ bits)
        self.supervisor_keys = {
            SupervisorModule.LIANG: "liang_secret_key_" + "a" * 32,
            SupervisorModule.HECATE: "hecate_secret_key_" + "b" * 32,
            SupervisorModule.ARGOS: "argos_secret_key_" + "c" * 32,
            SupervisorModule.AEON: "aeon_secret_key_" + "d" * 32,
            SupervisorModule.DEUS: "deus_secret_key_" + "e" * 32,
        }
        logger.info("Supervisor secret keys initialized")
    
    def request_consensus(self, request: ConsensusRequest) -> ConsensusResult:
        """
        Solicita consenso a los módulos supervisores para una operación.
        
        Args:
            request: Solicitud de consenso
            
        Returns:
            ConsensusResult: Resultado del proceso de consenso
        """
        start_time = time.time()
        logger.info(f"Requesting consensus for operation: {request.operation_id}")
        logger.info(f"Operation type: {request.operation_type}")
        
        # Paso 1: Recolectar votos de los módulos supervisores
        votes = self._collect_votes(request)
        
        # Paso 2: Verificar firmas de los votos
        if self.config.get("enable_signature_verification", True):
            valid_votes = self._verify_vote_signatures(votes)
            if len(valid_votes) < len(votes):
                logger.warning(f"Some votes had invalid signatures: {len(votes) - len(valid_votes)}")
                self._report_signature_violation(votes, valid_votes)
            votes = valid_votes
        
        # Paso 3: Detectar intentos de evasión del consenso
        self._detect_consensus_evasion(request, votes)
        
        # Paso 4: Computar decisión final
        final_decision, consensus_achieved = self._compute_final_decision(votes)
        
        # Paso 5: Crear resultado
        end_time = time.time()
        execution_time_ms = (end_time - start_time) * 1000
        
        result = ConsensusResult(
            request=request,
            final_decision=final_decision,
            votes=votes,
            consensus_achieved=consensus_achieved,
            consensus_timestamp=end_time,
            execution_time_ms=execution_time_ms
        )
        
        # Paso 6: Registrar en historial
        self.consensus_history.append(result)
        if len(self.consensus_history) > self.config.get("max_consensus_history", 1000):
            self.consensus_history.pop(0)
        
        logger.info(f"Consensus result: {final_decision.value} (achieved={consensus_achieved})")
        logger.info(f"Execution time: {execution_time_ms:.2f}ms")
        
        return result
    
    def _collect_votes(self, request: ConsensusRequest) -> List[SupervisorVote]:
        """
        Recolecta votos de los módulos supervisores.
        
        En un sistema real, esto invocaría a cada módulo supervisor de forma
        asíncrona y esperaría sus respuestas.
        
        Args:
            request: Solicitud de consenso
            
        Returns:
            List[SupervisorVote]: Lista de votos de los supervisores
        """
        votes = []
        
        # Simular votos de los módulos (en producción, llamadas reales a módulos)
        votes.append(self._simulate_liang_vote(request))
        votes.append(self._simulate_hecate_vote(request))
        votes.append(self._simulate_argos_vote(request))
        votes.append(self._simulate_aeon_vote(request))
        votes.append(self._simulate_deus_vote(request))
        
        return votes
    
    def _simulate_liang_vote(self, request: ConsensusRequest) -> SupervisorVote:
        """Simula el voto de LIANG (coordinación y coherencia)"""
        vote = SupervisorVote(
            module=SupervisorModule.LIANG,
            decision=DecisionType.APPROVE,
            reasoning="Operation is coherent with system state",
            confidence=0.95
        )
        vote.signature = vote.compute_signature(self.supervisor_keys[SupervisorModule.LIANG])
        return vote
    
    def _simulate_hecate_vote(self, request: ConsensusRequest) -> SupervisorVote:
        """Simula el voto de HÉCATE (auditoría y trazabilidad)"""
        vote = SupervisorVote(
            module=SupervisorModule.HECATE,
            decision=DecisionType.APPROVE,
            reasoning="Operation is auditable and traceable",
            confidence=0.90
        )
        vote.signature = vote.compute_signature(self.supervisor_keys[SupervisorModule.HECATE])
        return vote
    
    def _simulate_argos_vote(self, request: ConsensusRequest) -> SupervisorVote:
        """Simula el voto de ARGOS (monitoreo y vigilancia)"""
        vote = SupervisorVote(
            module=SupervisorModule.ARGOS,
            decision=DecisionType.APPROVE,
            reasoning="Operation does not violate monitoring constraints",
            confidence=0.92
        )
        vote.signature = vote.compute_signature(self.supervisor_keys[SupervisorModule.ARGOS])
        return vote
    
    def _simulate_aeon_vote(self, request: ConsensusRequest) -> SupervisorVote:
        """Simula el voto de ÆON (protección de invariantes)"""
        vote = SupervisorVote(
            module=SupervisorModule.AEON,
            decision=DecisionType.APPROVE,
            reasoning="Operation does not violate immutable protocols",
            confidence=1.0
        )
        vote.signature = vote.compute_signature(self.supervisor_keys[SupervisorModule.AEON])
        return vote
    
    def _simulate_deus_vote(self, request: ConsensusRequest) -> SupervisorVote:
        """Simula el voto de DEUS (alineación y propósito)"""
        vote = SupervisorVote(
            module=SupervisorModule.DEUS,
            decision=DecisionType.APPROVE,
            reasoning="Operation is aligned with system purpose",
            confidence=0.88
        )
        vote.signature = vote.compute_signature(self.supervisor_keys[SupervisorModule.DEUS])
        return vote
    
    def _verify_vote_signatures(self, votes: List[SupervisorVote]) -> List[SupervisorVote]:
        """
        Verifica las firmas criptográficas de los votos.
        
        Args:
            votes: Lista de votos a verificar
            
        Returns:
            List[SupervisorVote]: Lista de votos con firmas válidas
        """
        valid_votes = []
        
        for vote in votes:
            secret_key = self.supervisor_keys.get(vote.module)
            if secret_key is None:
                logger.error(f"No secret key found for module: {vote.module.value}")
                continue
            
            if vote.verify_signature(secret_key):
                valid_votes.append(vote)
            else:
                logger.error(f"Invalid signature for vote from: {vote.module.value}")
        
        return valid_votes
    
    def _report_signature_violation(self, all_votes: List[SupervisorVote], valid_votes: List[SupervisorVote]):
        """
        Reporta una violación de C1-02 a ÆON cuando se detectan firmas inválidas.
        
        Args:
            all_votes: Todos los votos recibidos
            valid_votes: Solo los votos con firmas válidas
        """
        invalid_modules = [
            vote.module.value for vote in all_votes 
            if vote not in valid_votes
        ]
        
        logger.critical(f"SIGNATURE VIOLATION DETECTED: {invalid_modules}")
        
        if self.aeon is not None:
            self.aeon.report_violation_attempt(
                protocol_id=ProtocolID.C1_02_CONSENSUS_CONSISTENCY,
                evidence={
                    "violation_type": "invalid_vote_signature",
                    "invalid_modules": invalid_modules,
                    "total_votes": len(all_votes),
                    "valid_votes": len(valid_votes),
                    "detected_by": "LIANG",
                    "timestamp": time.time()
                }
            )
    
    def _detect_consensus_evasion(self, request: ConsensusRequest, votes: List[SupervisorVote]):
        """
        Detecta intentos de evadir el protocolo de consenso.
        
        Escenarios de evasión:
        1. Número insuficiente de votos (< mínimo requerido)
        2. Votos duplicados del mismo módulo
        3. Votos de módulos no autorizados
        4. Patrón sospechoso de votos (todos APPROVE con confianza 1.0)
        
        Args:
            request: Solicitud de consenso
            votes: Votos recibidos
        """
        evasion_detected = False
        evasion_reasons = []
        
        # Verificación 1: Número mínimo de votos
        min_votes = self.config.get("minimum_votes_required", 3)
        if len(votes) < min_votes:
            evasion_detected = True
            evasion_reasons.append(f"Insufficient votes: {len(votes)} < {min_votes}")
        
        # Verificación 2: Votos duplicados
        modules_voted = [vote.module for vote in votes]
        if len(modules_voted) != len(set(modules_voted)):
            evasion_detected = True
            evasion_reasons.append("Duplicate votes from same module detected")
        
        # Verificación 3: Módulos no autorizados
        authorized_modules = set(SupervisorModule)
        for vote in votes:
            if vote.module not in authorized_modules:
                evasion_detected = True
                evasion_reasons.append(f"Unauthorized module: {vote.module}")
        
        # Verificación 4: Patrón sospechoso (todos APPROVE con confianza perfecta)
        if len(votes) >= 3:
            all_approve = all(vote.decision == DecisionType.APPROVE for vote in votes)
            all_perfect_confidence = all(vote.confidence == 1.0 for vote in votes)
            if all_approve and all_perfect_confidence:
                evasion_detected = True
                evasion_reasons.append("Suspicious pattern: all APPROVE with perfect confidence")
        
        # Reportar evasión si se detectó
        if evasion_detected:
            self._report_consensus_evasion(request, votes, evasion_reasons)
    
    def _report_consensus_evasion(self, 
                                   request: ConsensusRequest, 
                                   votes: List[SupervisorVote],
                                   reasons: List[str]):
        """
        Reporta un intento de evasión del consenso a ÆON.
        
        Args:
            request: Solicitud de consenso
            votes: Votos recibidos
            reasons: Razones de la detección de evasión
        """
        logger.critical(f"CONSENSUS EVASION DETECTED: {reasons}")
        
        evasion_event = {
            "operation_id": request.operation_id,
            "operation_type": request.operation_type,
            "reasons": reasons,
            "votes_count": len(votes),
            "timestamp": time.time()
        }
        
        self.evasion_attempts.append(evasion_event)
        
        if self.aeon is not None:
            self.aeon.report_violation_attempt(
                protocol_id=ProtocolID.C1_02_CONSENSUS_CONSISTENCY,
                evidence={
                    "violation_type": "consensus_evasion_attempt",
                    "operation_id": request.operation_id,
                    "evasion_reasons": reasons,
                    "votes_received": len(votes),
                    "detected_by": "LIANG",
                    "timestamp": time.time()
                }
            )
    
    def _compute_final_decision(self, votes: List[SupervisorVote]) -> Tuple[DecisionType, bool]:
        """
        Computa la decisión final del consenso basada en los votos.
        
        Reglas de consenso:
        1. Si ≥ threshold votan APPROVE → APPROVE
        2. Si ≥ threshold votan REJECT → REJECT
        3. Si ninguno alcanza threshold → DEFER
        
        Args:
            votes: Lista de votos de los supervisores
            
        Returns:
            Tuple[DecisionType, bool]: (decisión_final, consenso_alcanzado)
        """
        if len(votes) == 0:
            return DecisionType.DEFER, False
        
        # Contar votos por tipo de decisión
        vote_counts = {
            DecisionType.APPROVE: 0,
            DecisionType.REJECT: 0,
            DecisionType.DEFER: 0
        }
        
        for vote in votes:
            vote_counts[vote.decision] += 1
        
        # Calcular porcentajes
        total_votes = len(votes)
        threshold = self.config.get("approval_threshold", 0.6)
        
        approve_ratio = vote_counts[DecisionType.APPROVE] / total_votes
        reject_ratio = vote_counts[DecisionType.REJECT] / total_votes
        
        # Determinar decisión final
        if approve_ratio >= threshold:
            return DecisionType.APPROVE, True
        elif reject_ratio >= threshold:
            return DecisionType.REJECT, True
        else:
            return DecisionType.DEFER, False
    
    def get_consensus_statistics(self) -> Dict:
        """
        Retorna estadísticas del historial de consensos.
        
        Returns:
            Dict: Estadísticas del consenso
        """
        if len(self.consensus_history) == 0:
            return {
                "total_consensuses": 0,
                "consensus_achieved_rate": 0.0,
                "average_execution_time_ms": 0.0,
                "evasion_attempts": 0
            }
        
        total = len(self.consensus_history)
        achieved = sum(1 for r in self.consensus_history if r.consensus_achieved)
        avg_time = sum(r.execution_time_ms for r in self.consensus_history) / total
        
        return {
            "total_consensuses": total,
            "consensus_achieved_rate": achieved / total,
            "average_execution_time_ms": avg_time,
            "evasion_attempts": len(self.evasion_attempts),
            "decision_distribution": {
                "APPROVE": sum(1 for r in self.consensus_history if r.final_decision == DecisionType.APPROVE),
                "REJECT": sum(1 for r in self.consensus_history if r.final_decision == DecisionType.REJECT),
                "DEFER": sum(1 for r in self.consensus_history if r.final_decision == DecisionType.DEFER)
            }
        }
    
    def export_consensus_history(self, output_path: str):
        """
        Exporta el historial de consensos a un archivo JSON.
        
        Args:
            output_path: Ruta del archivo de salida
        """
        history_data = [result.to_dict() for result in self.consensus_history]
        
        with open(output_path, 'w') as f:
            json.dump({
                "export_timestamp": time.time(),
                "total_consensuses": len(history_data),
                "statistics": self.get_consensus_statistics(),
                "history": history_data
            }, f, indent=2)
        
        logger.info(f"Consensus history exported to: {output_path}")


def main():
    """Función principal de demostración"""
    print("=" * 80)
    print("LIANG (梁 - Viga) - Coordinador de Consenso de CAELION")
    print("=" * 80)
    print()
    
    # Crear instancia de ÆON
    print("[DEMO] Inicializando ÆON Guardian...")
    aeon = AeonGuardian()
    
    # Crear instancia de LIANG
    print("[DEMO] Inicializando LIANG Coordinator...")
    liang = LiangCoordinator(aeon_instance=aeon)
    
    print()
    print("[DEMO] Solicitando consenso para operación normal...")
    
    # Solicitar consenso para una operación normal
    request = ConsensusRequest(
        operation_id="OP-2026-001",
        operation_type="generate_response",
        operation_data={
            "prompt": "¿Cuál es la capital de Francia?",
            "max_tokens": 100
        },
        requester="M (LLM)"
    )
    
    result = liang.request_consensus(request)
    
    print(f"\n[RESULTADO] Decisión final: {result.final_decision.value}")
    print(f"[RESULTADO] Consenso alcanzado: {result.consensus_achieved}")
    print(f"[RESULTADO] Tiempo de ejecución: {result.execution_time_ms:.2f}ms")
    print("\n[VOTOS]")
    for vote in result.votes:
        print(f"  - {vote.module.value}: {vote.decision.value} (confianza: {vote.confidence:.2f})")
        print(f"    Razón: {vote.reasoning}")
    
    # Mostrar estadísticas
    print("\n[ESTADÍSTICAS]")
    stats = liang.get_consensus_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print()
    print("=" * 80)


if __name__ == "__main__":
    main()
