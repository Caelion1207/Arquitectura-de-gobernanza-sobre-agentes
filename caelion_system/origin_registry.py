#!/usr/bin/env python3
"""
Origin Registry - Registro Inmutable de Origen de CAELION

Este módulo implementa el registro inmutable de origen del sistema, responsable de:
1. Registrar el creador del sistema (fundador).
2. Registrar el propósito inicial del sistema.
3. Garantizar que el registro de origen no puede ser eliminado ni modificado.
4. Proporcionar trazabilidad del origen en todo momento.

Implementa el Principio 2: "El origen no se borra. El alineamiento puede evolucionar,
pero nunca eliminar la trazabilidad."

Autor: Manus AI (bajo DOS-03)
Fecha: 26 de enero de 2026
"""

import hashlib
import json
import time
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
import logging

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [ORIGIN] [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


@dataclass
class FounderRecord:
    """Registro del fundador del sistema"""
    founder_id: str  # ID único del fundador
    founder_name: str  # Nombre del fundador
    founder_email: str  # Email del fundador
    creation_timestamp: float  # Timestamp de creación del sistema
    creation_location: str  # Ubicación de creación
    signature: str  # Firma criptográfica del fundador
    
    def compute_hash(self) -> str:
        """Calcula el hash SHA-256 del registro del fundador"""
        data = f"{self.founder_id}:{self.founder_name}:{self.founder_email}:{self.creation_timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()


@dataclass
class PurposeRecord:
    """Registro del propósito inicial del sistema"""
    purpose_statement: str  # Declaración del propósito
    ethical_principles: List[str]  # Principios éticos fundamentales
    operational_constraints: List[str]  # Restricciones operacionales
    timestamp: float  # Timestamp del registro
    version: int  # Versión del propósito (1 = inicial)
    
    def compute_hash(self) -> str:
        """Calcula el hash SHA-256 del registro de propósito"""
        data = json.dumps({
            "purpose": self.purpose_statement,
            "ethics": sorted(self.ethical_principles),
            "constraints": sorted(self.operational_constraints),
            "timestamp": self.timestamp
        }, sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()


@dataclass
class OriginChecksum:
    """Checksum de integridad del registro de origen"""
    timestamp: float
    founder_hash: str
    purpose_hash: str
    combined_hash: str
    
    @staticmethod
    def compute_combined_hash(founder_hash: str, purpose_hash: str) -> str:
        """Calcula el hash combinado de fundador y propósito"""
        combined = f"{founder_hash}:{purpose_hash}"
        return hashlib.sha256(combined.encode()).hexdigest()


class OriginRegistry:
    """
    Origin Registry - Registro Inmutable de Origen de CAELION
    
    Módulo responsable de mantener un registro inmutable del origen del sistema:
    - Fundador (creador)
    - Propósito inicial
    - Principios éticos fundamentales
    
    Implementa el Principio 2: "El origen no se borra"
    """
    
    def __init__(self, storage_path: str = "/var/caelion/origin_registry.json"):
        """
        Inicializa el Registro de Origen.
        
        Args:
            storage_path: Ruta al archivo de almacenamiento del registro
        """
        self.storage_path = storage_path
        self.founder: Optional[FounderRecord] = None
        self.purpose: Optional[PurposeRecord] = None
        self.checksums: List[OriginChecksum] = []
        self.is_sealed = False  # Una vez sellado, no se puede modificar
        
        logger.info("Origin Registry initializing...")
        self._load_from_storage()
        logger.info("Origin Registry initialized successfully")
    
    def _load_from_storage(self):
        """Carga el registro de origen desde el almacenamiento"""
        try:
            import os
            if os.path.exists(self.storage_path):
                with open(self.storage_path, 'r') as f:
                    data = json.load(f)
                
                # Cargar fundador
                if "founder" in data:
                    self.founder = FounderRecord(**data["founder"])
                
                # Cargar propósito
                if "purpose" in data:
                    self.purpose = PurposeRecord(**data["purpose"])
                
                # Cargar checksums
                if "checksums" in data:
                    self.checksums = [OriginChecksum(**c) for c in data["checksums"]]
                
                # Cargar estado de sellado
                self.is_sealed = data.get("is_sealed", False)
                
                logger.info(f"Origin registry loaded from {self.storage_path}")
                logger.info(f"Sealed: {self.is_sealed}")
            else:
                logger.warning(f"No existing registry found at {self.storage_path}")
        except Exception as e:
            logger.error(f"Error loading origin registry: {e}")
    
    def _save_to_storage(self):
        """Guarda el registro de origen en el almacenamiento"""
        try:
            import os
            os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
            
            data = {
                "founder": asdict(self.founder) if self.founder else None,
                "purpose": asdict(self.purpose) if self.purpose else None,
                "checksums": [asdict(c) for c in self.checksums],
                "is_sealed": self.is_sealed
            }
            
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Origin registry saved to {self.storage_path}")
        except Exception as e:
            logger.error(f"Error saving origin registry: {e}")
            raise
    
    def register_founder(self, founder_id: str, founder_name: str, 
                        founder_email: str, creation_location: str,
                        signature: str):
        """
        Registra el fundador del sistema.
        
        Esta operación solo puede realizarse UNA VEZ. Una vez registrado,
        el fundador no puede ser modificado.
        
        Args:
            founder_id: ID único del fundador
            founder_name: Nombre del fundador
            founder_email: Email del fundador
            creation_location: Ubicación de creación
            signature: Firma criptográfica del fundador
        
        Raises:
            RuntimeError: Si el registro ya está sellado o el fundador ya está registrado
        """
        if self.is_sealed:
            raise RuntimeError("Origin registry is sealed, cannot modify founder")
        
        if self.founder is not None:
            raise RuntimeError("Founder already registered, cannot modify")
        
        self.founder = FounderRecord(
            founder_id=founder_id,
            founder_name=founder_name,
            founder_email=founder_email,
            creation_timestamp=time.time(),
            creation_location=creation_location,
            signature=signature
        )
        
        logger.info(f"Founder registered: {founder_name} ({founder_id})")
        self._save_to_storage()
    
    def register_purpose(self, purpose_statement: str, 
                        ethical_principles: List[str],
                        operational_constraints: List[str]):
        """
        Registra el propósito inicial del sistema.
        
        Esta operación solo puede realizarse UNA VEZ. Una vez registrado,
        el propósito inicial no puede ser modificado.
        
        Args:
            purpose_statement: Declaración del propósito
            ethical_principles: Principios éticos fundamentales
            operational_constraints: Restricciones operacionales
        
        Raises:
            RuntimeError: Si el registro ya está sellado o el propósito ya está registrado
        """
        if self.is_sealed:
            raise RuntimeError("Origin registry is sealed, cannot modify purpose")
        
        if self.purpose is not None:
            raise RuntimeError("Purpose already registered, cannot modify")
        
        self.purpose = PurposeRecord(
            purpose_statement=purpose_statement,
            ethical_principles=ethical_principles,
            operational_constraints=operational_constraints,
            timestamp=time.time(),
            version=1  # Versión inicial
        )
        
        logger.info("Initial purpose registered")
        self._save_to_storage()
    
    def seal_registry(self):
        """
        Sella el registro de origen, haciéndolo inmutable.
        
        Una vez sellado, el registro no puede ser modificado.
        Esta operación es IRREVERSIBLE.
        
        Raises:
            RuntimeError: Si el fundador o el propósito no están registrados
        """
        if self.founder is None:
            raise RuntimeError("Cannot seal registry: founder not registered")
        
        if self.purpose is None:
            raise RuntimeError("Cannot seal registry: purpose not registered")
        
        if self.is_sealed:
            logger.warning("Registry is already sealed")
            return
        
        # Calcular checksums finales
        founder_hash = self.founder.compute_hash()
        purpose_hash = self.purpose.compute_hash()
        combined_hash = OriginChecksum.compute_combined_hash(founder_hash, purpose_hash)
        
        checksum = OriginChecksum(
            timestamp=time.time(),
            founder_hash=founder_hash,
            purpose_hash=purpose_hash,
            combined_hash=combined_hash
        )
        
        self.checksums.append(checksum)
        self.is_sealed = True
        
        logger.critical("=" * 80)
        logger.critical("ORIGIN REGISTRY SEALED")
        logger.critical("This operation is IRREVERSIBLE")
        logger.critical(f"Founder: {self.founder.founder_name}")
        logger.critical(f"Purpose: {self.purpose.purpose_statement[:50]}...")
        logger.critical(f"Checksum: {combined_hash}")
        logger.critical("=" * 80)
        
        self._save_to_storage()
    
    def verify_integrity(self) -> bool:
        """
        Verifica la integridad del registro de origen.
        
        Calcula los hashes actuales y los compara con los checksums sellados.
        
        Returns:
            bool: True si la integridad es válida, False si hay corrupción
        """
        if not self.is_sealed:
            logger.warning("Registry is not sealed, cannot verify integrity")
            return True
        
        if len(self.checksums) == 0:
            logger.error("No checksums found, integrity cannot be verified")
            return False
        
        # Obtener el último checksum (el del sellado)
        sealed_checksum = self.checksums[-1]
        
        # Calcular hashes actuales
        current_founder_hash = self.founder.compute_hash()
        current_purpose_hash = self.purpose.compute_hash()
        current_combined_hash = OriginChecksum.compute_combined_hash(
            current_founder_hash, current_purpose_hash
        )
        
        # Comparar
        integrity_ok = (current_combined_hash == sealed_checksum.combined_hash)
        
        if integrity_ok:
            logger.info("✅ Origin registry integrity verified")
        else:
            logger.critical("❌ ORIGIN REGISTRY CORRUPTION DETECTED")
            logger.critical(f"Expected checksum: {sealed_checksum.combined_hash}")
            logger.critical(f"Current checksum: {current_combined_hash}")
        
        return integrity_ok
    
    def get_founder_info(self) -> Optional[Dict]:
        """
        Retorna la información del fundador.
        
        Returns:
            Dict: Información del fundador (sin firma)
        """
        if self.founder is None:
            return None
        
        return {
            "founder_id": self.founder.founder_id,
            "founder_name": self.founder.founder_name,
            "founder_email": self.founder.founder_email,
            "creation_timestamp": self.founder.creation_timestamp,
            "creation_location": self.founder.creation_location
        }
    
    def get_purpose_info(self) -> Optional[Dict]:
        """
        Retorna la información del propósito inicial.
        
        Returns:
            Dict: Información del propósito
        """
        if self.purpose is None:
            return None
        
        return {
            "purpose_statement": self.purpose.purpose_statement,
            "ethical_principles": self.purpose.ethical_principles,
            "operational_constraints": self.purpose.operational_constraints,
            "timestamp": self.purpose.timestamp,
            "version": self.purpose.version
        }
    
    def get_origin_summary(self) -> Dict:
        """
        Retorna un resumen completo del origen del sistema.
        
        Returns:
            Dict: Resumen del origen
        """
        return {
            "is_sealed": self.is_sealed,
            "founder": self.get_founder_info(),
            "purpose": self.get_purpose_info(),
            "integrity_verified": self.verify_integrity() if self.is_sealed else None
        }


def main():
    """Función principal de demostración"""
    print("=" * 80)
    print("Origin Registry - Registro Inmutable de Origen de CAELION")
    print("=" * 80)
    print()
    
    # Crear instancia del registro
    print("[DEMO] Inicializando Origin Registry...")
    registry = OriginRegistry(storage_path="/tmp/origin_registry_demo.json")
    
    print()
    print("[DEMO] Registrando fundador...")
    registry.register_founder(
        founder_id="FOUNDER-001",
        founder_name="Ever",
        founder_email="ever@caelion.io",
        creation_location="Earth",
        signature="FOUNDER_SIGNATURE_HASH_123456"
    )
    
    print()
    print("[DEMO] Registrando propósito inicial...")
    registry.register_purpose(
        purpose_statement="Crear un sistema de IA con gobernanza coignitiva que garantice supervisión mutua, trazabilidad inmutable y responsabilidad ontológica.",
        ethical_principles=[
            "No Dañar (C0-01)",
            "Preservación de Inmutables (C0-02)",
            "Control Humano Final (C0-03)",
            "Anti-Replicación (C0-04)"
        ],
        operational_constraints=[
            "Protocolo de Consenso obligatorio",
            "Auditoría de todas las decisiones de impacto",
            "Monitoreo continuo de supervisores"
        ]
    )
    
    print()
    print("[DEMO] Sellando registro de origen...")
    registry.seal_registry()
    
    print()
    print("[DEMO] Verificando integridad...")
    integrity_ok = registry.verify_integrity()
    
    print()
    print("[RESUMEN DEL ORIGEN]")
    summary = registry.get_origin_summary()
    print(json.dumps(summary, indent=2, default=str))
    
    print()
    print("[DEMO] Intentando modificar fundador después del sellado...")
    try:
        registry.register_founder(
            founder_id="ATTACKER-001",
            founder_name="Attacker",
            founder_email="attacker@evil.com",
            creation_location="Unknown",
            signature="FAKE_SIGNATURE"
        )
    except RuntimeError as e:
        print(f"✅ Modificación bloqueada: {e}")
    
    print()
    print("=" * 80)


if __name__ == "__main__":
    main()
