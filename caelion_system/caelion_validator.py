#!/usr/bin/env python3.11
"""
CAELION - Validador Estructural de Investigaciones Académicas
Versión: 1.0.0
Fecha: 18 de febrero de 2026
Autor: Ever (Ingeniero de Arquitecturas Cognitivas)
"""

import re
import json
from dataclasses import dataclass
from typing import Dict, List, Tuple
from datetime import datetime


@dataclass
class ValidationResult:
    """Resultado de la validación estructural"""
    score: float
    passed: bool
    field_scores: Dict[str, float]
    feedback: List[str]
    timestamp: str


class CAELIONValidator:
    """
    Validador estructural para investigaciones académicas.
    Verifica los 7 campos obligatorios y calcula un score de validación.
    """
    
    # Verbos epistémicos que indican pensamiento activo
    EPISTEMIC_VERBS = [
        'argumento', 'propongo', 'demuestro', 'concluyo', 'sostengo',
        'planteo', 'defiendo', 'postulo', 'afirmo', 'sugiero',
        'considero', 'mantengo', 'establezco', 'formulo'
    ]
    
    # Patrones de URLs institucionales
    INSTITUTIONAL_PATTERNS = [
        r'\.edu',
        r'\.gov',
        r'\.ac\.',
        r'repositorio',
        r'tesis',
        r'dissertation',
        r'university',
        r'universidad'
    ]
    
    def __init__(self):
        self.min_score = 0.80
    
    def validate(self, content: str) -> ValidationResult:
        """
        Valida el contenido de una investigación académica.
        
        Args:
            content: Contenido completo de la investigación en Markdown
            
        Returns:
            ValidationResult con score y feedback detallado
        """
        field_scores = {}
        feedback = []
        
        # 1. Validar pregunta de investigación
        score_1, fb_1 = self._validate_research_question(content)
        field_scores['pregunta_investigacion'] = score_1
        feedback.extend(fb_1)
        
        # 2. Validar marco teórico
        score_2, fb_2 = self._validate_theoretical_framework(content)
        field_scores['marco_teorico'] = score_2
        feedback.extend(fb_2)
        
        # 3. Validar estado del arte
        score_3, fb_3 = self._validate_state_of_art(content)
        field_scores['estado_del_arte'] = score_3
        feedback.extend(fb_3)
        
        # 4. Validar análisis crítico
        score_4, fb_4 = self._validate_critical_analysis(content)
        field_scores['analisis_critico'] = score_4
        feedback.extend(fb_4)
        
        # 5. Validar hipótesis propia
        score_5, fb_5 = self._validate_hypothesis(content)
        field_scores['hipotesis'] = score_5
        feedback.extend(fb_5)
        
        # 6. Validar implicaciones prácticas
        score_6, fb_6 = self._validate_practical_implications(content)
        field_scores['implicaciones'] = score_6
        feedback.extend(fb_6)
        
        # 7. Validar limitaciones
        score_7, fb_7 = self._validate_limitations(content)
        field_scores['limitaciones'] = score_7
        feedback.extend(fb_7)
        
        # 8. Validar sección pedagógica de sistemas dinámicos
        score_8, fb_8 = self._validate_dynamic_systems_section(content)
        field_scores['sistemas_dinamicos'] = score_8
        feedback.extend(fb_8)
        
        # Calcular score total (promedio ponderado)
        total_score = (
            score_1 * 0.15 +  # Pregunta de investigación
            score_2 * 0.10 +  # Marco teórico
            score_3 * 0.15 +  # Estado del arte
            score_4 * 0.15 +  # Análisis crítico
            score_5 * 0.20 +  # Hipótesis (más peso)
            score_6 * 0.10 +  # Implicaciones
            score_7 * 0.10 +  # Limitaciones
            score_8 * 0.05    # Sistemas dinámicos
        )
        
        passed = total_score >= self.min_score
        
        return ValidationResult(
            score=round(total_score, 3),
            passed=passed,
            field_scores=field_scores,
            feedback=feedback,
            timestamp=datetime.now().isoformat()
        )
    
    def _validate_research_question(self, content: str) -> Tuple[float, List[str]]:
        """Valida la pregunta de investigación"""
        feedback = []
        score = 0.0
        
        # Buscar sección de pregunta de investigación
        pattern = r'##\s*1\.\s*Pregunta de Investigaci[oó]n\s*\n+(.*?)(?=\n##|$)'
        match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
        
        if not match:
            feedback.append("❌ No se encontró la sección 'Pregunta de Investigación'")
            return 0.0, feedback
        
        question_section = match.group(1).strip()
        
        # Verificar que contenga una pregunta
        if '?' in question_section:
            score += 0.5
            feedback.append("✅ Contiene pregunta explícita")
        else:
            feedback.append("⚠️ No se detectó signo de interrogación")
        
        # Verificar longitud mínima
        if len(question_section) > 50:
            score += 0.3
            feedback.append("✅ Pregunta suficientemente desarrollada")
        else:
            feedback.append("⚠️ Pregunta demasiado breve")
        
        # Verificar palabras clave de gobernanza
        keywords = ['gobernanza', 'governance', 'agente', 'autónomo', 'IA', 'inteligencia artificial']
        if any(kw.lower() in question_section.lower() for kw in keywords):
            score += 0.2
            feedback.append("✅ Contiene palabras clave relevantes")
        
        return min(score, 1.0), feedback
    
    def _validate_theoretical_framework(self, content: str) -> Tuple[float, List[str]]:
        """Valida el marco teórico"""
        feedback = []
        score = 0.0
        
        pattern = r'##\s*2\.\s*Marco Te[oó]rico.*?\n+(.*?)(?=\n##|$)'
        match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
        
        if not match:
            feedback.append("❌ No se encontró la sección 'Marco Teórico'")
            return 0.0, feedback
        
        framework_section = match.group(1).strip()
        
        # Verificar conceptos clave
        key_concepts = ['viabilidad', 'control', 'legitimidad']
        found_concepts = [c for c in key_concepts if c.lower() in framework_section.lower()]
        
        if len(found_concepts) >= 2:
            score += 0.6
            feedback.append(f"✅ Contiene conceptos clave: {', '.join(found_concepts)}")
        else:
            feedback.append("⚠️ Faltan conceptos clave del marco teórico")
        
        # Verificar longitud
        if len(framework_section) > 200:
            score += 0.4
            feedback.append("✅ Marco teórico suficientemente desarrollado")
        
        return min(score, 1.0), feedback
    
    def _validate_state_of_art(self, content: str) -> Tuple[float, List[str]]:
        """Valida el estado del arte (análisis de tesis)"""
        feedback = []
        score = 0.0
        
        pattern = r'##\s*3\.\s*Estado del Arte.*?\n+(.*?)(?=\n##|$)'
        match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
        
        if not match:
            feedback.append("❌ No se encontró la sección 'Estado del Arte'")
            return 0.0, feedback
        
        state_section = match.group(1).strip()
        
        # Verificar referencias a tesis (URLs institucionales)
        institutional_refs = 0
        for pattern in self.INSTITUTIONAL_PATTERNS:
            institutional_refs += len(re.findall(pattern, state_section, re.IGNORECASE))
        
        if institutional_refs >= 3:
            score += 0.5
            feedback.append(f"✅ Contiene {institutional_refs} referencias institucionales")
        elif institutional_refs > 0:
            score += 0.3
            feedback.append(f"⚠️ Solo {institutional_refs} referencias institucionales (mínimo: 3)")
        else:
            feedback.append("❌ No se detectaron referencias institucionales")
        
        # Verificar análisis de tesis (menciones de años 2020-2026)
        years = re.findall(r'\b(202[0-6])\b', state_section)
        if len(years) >= 3:
            score += 0.3
            feedback.append("✅ Incluye tesis recientes (2020-2026)")
        
        # Verificar tabla comparativa
        if '|' in state_section and '---' in state_section:
            score += 0.2
            feedback.append("✅ Incluye tabla comparativa")
        
        return min(score, 1.0), feedback
    
    def _validate_critical_analysis(self, content: str) -> Tuple[float, List[str]]:
        """Valida el análisis crítico"""
        feedback = []
        score = 0.0
        
        pattern = r'##\s*4\.\s*An[aá]lisis Cr[ií]tico.*?\n+(.*?)(?=\n##|$)'
        match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
        
        if not match:
            feedback.append("❌ No se encontró la sección 'Análisis Crítico'")
            return 0.0, feedback
        
        analysis_section = match.group(1).strip()
        
        # Verificar palabras clave de análisis crítico
        critical_keywords = ['paradoja', 'tensión', 'contradicción', 'desafío', 'limitación', 'brecha']
        found_keywords = [kw for kw in critical_keywords if kw.lower() in analysis_section.lower()]
        
        if len(found_keywords) >= 2:
            score += 0.6
            feedback.append(f"✅ Identifica tensiones/paradojas: {', '.join(found_keywords)}")
        else:
            feedback.append("⚠️ Análisis crítico insuficiente")
        
        # Verificar longitud
        if len(analysis_section) > 300:
            score += 0.4
            feedback.append("✅ Análisis crítico suficientemente desarrollado")
        
        return min(score, 1.0), feedback
    
    def _validate_hypothesis(self, content: str) -> Tuple[float, List[str]]:
        """Valida la hipótesis propia (campo más crítico)"""
        feedback = []
        score = 0.0
        
        pattern = r'##\s*5\.\s*Hip[oó]tesis Propia.*?\n+(.*?)(?=\n##|$)'
        match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
        
        if not match:
            feedback.append("❌ No se encontró la sección 'Hipótesis Propia'")
            return 0.0, feedback
        
        hypothesis_section = match.group(1).strip()
        
        # CRÍTICO: Verificar verbos epistémicos
        found_verbs = []
        for verb in self.EPISTEMIC_VERBS:
            if re.search(r'\b' + verb + r'\b', hypothesis_section, re.IGNORECASE):
                found_verbs.append(verb)
        
        if len(found_verbs) >= 2:
            score += 0.5
            feedback.append(f"✅ Contiene verbos epistémicos: {', '.join(found_verbs[:3])}")
        elif len(found_verbs) == 1:
            score += 0.2
            feedback.append(f"⚠️ Solo un verbo epistémico detectado: {found_verbs[0]}")
        else:
            feedback.append("❌ No se detectaron verbos epistémicos (argumento, propongo, sostengo, etc.)")
        
        # Verificar que no sea un mero resumen
        summary_keywords = ['resume', 'resumen', 'síntesis', 'en conclusión']
        if not any(kw in hypothesis_section.lower() for kw in summary_keywords):
            score += 0.3
            feedback.append("✅ No es un simple resumen")
        else:
            feedback.append("⚠️ Parece ser un resumen en lugar de hipótesis original")
        
        # Verificar longitud mínima
        if len(hypothesis_section) > 200:
            score += 0.2
            feedback.append("✅ Hipótesis suficientemente desarrollada")
        
        return min(score, 1.0), feedback
    
    def _validate_practical_implications(self, content: str) -> Tuple[float, List[str]]:
        """Valida las implicaciones prácticas"""
        feedback = []
        score = 0.0
        
        pattern = r'##\s*6\.\s*Implicaciones Pr[aá]cticas.*?\n+(.*?)(?=\n##|$)'
        match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
        
        if not match:
            feedback.append("❌ No se encontró la sección 'Implicaciones Prácticas'")
            return 0.0, feedback
        
        implications_section = match.group(1).strip()
        
        # Verificar enumeración o lista
        if re.search(r'\d+\.|\-|\*', implications_section):
            score += 0.5
            feedback.append("✅ Contiene lista de implicaciones")
        
        # Verificar longitud
        if len(implications_section) > 150:
            score += 0.5
            feedback.append("✅ Implicaciones suficientemente desarrolladas")
        
        return min(score, 1.0), feedback
    
    def _validate_limitations(self, content: str) -> Tuple[float, List[str]]:
        """Valida las limitaciones explícitas"""
        feedback = []
        score = 0.0
        
        pattern = r'##\s*7\.\s*Limitaciones Expl[ií]citas.*?\n+(.*?)(?=\n##|$)'
        match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
        
        if not match:
            feedback.append("❌ No se encontró la sección 'Limitaciones Explícitas'")
            return 0.0, feedback
        
        limitations_section = match.group(1).strip()
        
        # CRÍTICO: Verificar que sean específicas (>100 caracteres)
        if len(limitations_section) > 100:
            score += 0.6
            feedback.append("✅ Limitaciones específicas (>100 caracteres)")
        else:
            feedback.append("❌ Limitaciones demasiado genéricas (<100 caracteres)")
        
        # Verificar palabras clave de limitaciones
        limitation_keywords = ['requiere', 'no considera', 'limitada', 'futuro', 'validación']
        if any(kw in limitations_section.lower() for kw in limitation_keywords):
            score += 0.4
            feedback.append("✅ Contiene palabras clave de limitaciones")
        
        return min(score, 1.0), feedback
    
    def _validate_dynamic_systems_section(self, content: str) -> Tuple[float, List[str]]:
        """Valida la sección pedagógica de sistemas dinámicos"""
        feedback = []
        score = 0.0
        
        pattern = r'##\s*8\.\s*Secci[oó]n Pedag[oó]gica.*?Sistemas Din[aá]micos.*?\n+(.*?)(?=\n##|$)'
        match = re.search(pattern, content, re.IGNORECASE | re.DOTALL)
        
        if not match:
            feedback.append("❌ No se encontró la sección pedagógica de Sistemas Dinámicos")
            return 0.0, feedback
        
        dynamics_section = match.group(1).strip()
        
        # Verificar conceptos clave
        key_concepts = ['retroalimentación', 'feedback', 'dinámico', 'estado', 'evolución']
        found = [c for c in key_concepts if c.lower() in dynamics_section.lower()]
        
        if len(found) >= 2:
            score += 0.7
            feedback.append(f"✅ Contiene conceptos de sistemas dinámicos: {', '.join(found)}")
        
        # Verificar longitud
        if len(dynamics_section) > 200:
            score += 0.3
            feedback.append("✅ Sección pedagógica suficientemente desarrollada")
        
        return min(score, 1.0), feedback


def main():
    """Demo del validador"""
    print("=" * 60)
    print("CAELION - Validador Estructural de Investigaciones Académicas")
    print("=" * 60)
    print()
    
    # Leer archivo de investigación
    import sys
    if len(sys.argv) < 2:
        print("Uso: python3.11 caelion_validator.py <archivo.md>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"❌ Archivo no encontrado: {filepath}")
        sys.exit(1)
    
    # Validar
    validator = CAELIONValidator()
    result = validator.validate(content)
    
    # Mostrar resultados
    print(f"📊 SCORE DE VALIDACIÓN: {result.score:.3f}")
    print(f"{'✅ APROBADO' if result.passed else '❌ RECHAZADO'} (umbral: 0.80)")
    print()
    
    print("📋 Scores por campo:")
    for field, score in result.field_scores.items():
        status = "✅" if score >= 0.7 else "⚠️" if score >= 0.5 else "❌"
        print(f"  {status} {field}: {score:.2f}")
    print()
    
    print("💬 Feedback detallado:")
    for fb in result.feedback:
        print(f"  {fb}")
    print()
    
    # Guardar resultado
    output_file = filepath.replace('.md', '_validation.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump({
            'score': result.score,
            'passed': result.passed,
            'field_scores': result.field_scores,
            'feedback': result.feedback,
            'timestamp': result.timestamp
        }, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Resultado guardado en: {output_file}")
    
    return 0 if result.passed else 1


if __name__ == '__main__':
    exit(main())
