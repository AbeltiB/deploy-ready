from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List

from app.models.schemas.architecture import ArchitectureDesign
from app.models.schemas.blockly import EnhancedBlocklyDefinition
from app.models.schemas.component_catalog import get_available_components
from app.models.schemas.core import PropertyValue
from app.models.schemas.layout import EnhancedLayoutDefinition
from app.utils.output_JSON_formatter import format_pipeline_output, validate_output


@dataclass
class StageResult:
    stage: str
    status: str
    details: Dict[str, Any]


class APIPipeline:
    """Synchronous, self-contained pipeline with explicit generation/validation stages."""

    stage_order = [
        "intent_analysis",
        "context_building",
        "architecture_generation",
        "architecture_validation",
        "layout_generation",
        "layout_validation",
        "blockly_generation",
        "blockly_validation",
        "json_conversion",
    ]

    def run(self, prompt: str) -> Dict[str, Any]:
        context: Dict[str, Any] = {
            "prompt": prompt.strip(),
            "started_at": datetime.now(timezone.utc).isoformat(),
            "components_catalog": get_available_components(),
            "stages": [],
        }

        self._record(context, "intent_analysis", self._intent_analysis(context))
        self._record(context, "context_building", self._context_building(context))
        self._record(context, "architecture_generation", self._architecture_generation(context))
        self._record(context, "architecture_validation", self._architecture_validation(context))
        self._record(context, "layout_generation", self._layout_generation(context))
        self._record(context, "layout_validation", self._layout_validation(context))
        self._record(context, "blockly_generation", self._blockly_generation(context))
        self._record(context, "blockly_validation", self._blockly_validation(context))
        self._record(context, "json_conversion", self._json_conversion(context))

        return {
            "status": "success",
            "prompt": context["prompt"],
            "pipeline": {
                "stage": "completed",
                "steps": self.stage_order,
                "started_at": context["started_at"],
                "finished_at": datetime.now(timezone.utc).isoformat(),
            },
            "intent": context["intent"],
            "context": context["enriched_context"],
            "architecture": context["architecture"],
            "layout": context["layout"],
            "blockly": context["blockly"],
            "result": context["formatted_result"],
            "validation": context["json_validation"],
            "stage_results": [r.__dict__ for r in context["stages"]],
        }

    def _record(self, context: Dict[str, Any], stage: str, details: Dict[str, Any]) -> None:
        context["stages"].append(StageResult(stage=stage, status="completed", details=details))

    def _intent_analysis(self, context: Dict[str, Any]) -> Dict[str, Any]:
        text = context["prompt"].lower()
        if any(k in text for k in ["todo", "task", "checklist"]):
            domain = "productivity"
        elif any(k in text for k in ["shop", "cart", "payment", "order"]):
            domain = "ecommerce"
        elif any(k in text for k in ["chat", "message", "social"]):
            domain = "communication"
        else:
            domain = "general"

        complexity = "simple"
        if len(text) > 220 or "dashboard" in text or "multi" in text:
            complexity = "complex"
        elif len(text) > 120:
            complexity = "moderate"

        entities = [w for w in ["auth", "api", "list", "search", "upload"] if w in text]
        context["intent"] = {
            "domain": domain,
            "complexity": complexity,
            "summary": context["prompt"][:180],
            "entities": entities,
        }
        return context["intent"]

    def _context_building(self, context: Dict[str, Any]) -> Dict[str, Any]:
        intent = context["intent"]
        enriched = {
            "target_screen": "main_screen",
            "theme": {
                "background": "#FFFFFF",
                "primary": "#007AFF",
                "text": "#111111",
            },
            "component_candidates": ["Text", "InputText", "Button"],
            "catalog_size": len(context["components_catalog"]),
            "intent_domain": intent["domain"],
        }
        context["enriched_context"] = enriched
        return enriched

    def _architecture_generation(self, context: Dict[str, Any]) -> Dict[str, Any]:
        architecture = {
            "app_type": "single-page",
            "screens": [
                {
                    "id": "main_screen",
                    "name": "Main Screen",
                    "purpose": context["intent"]["summary"],
                    "components": ["Text", "InputText", "Button"],
                    "navigation": [],
                }
            ],
            "navigation": {"type": "none", "routes": []},
            "state_management": [
                {
                    "name": "userInput",
                    "type": "local-state",
                    "scope": "screen",
                    "initial_value": "",
                }
            ],
            "data_flow": {
                "user_interactions": ["submit_prompt", "view_result"],
                "api_calls": [],
                "local_storage": [],
            },
        }
        context["architecture"] = architecture
        return architecture

    def _architecture_validation(self, context: Dict[str, Any]) -> Dict[str, Any]:
        validated = ArchitectureDesign.model_validate(context["architecture"])
        context["architecture"] = validated.model_dump()
        return {"valid": True, "screens": len(validated.screens)}

    def _layout_generation(self, context: Dict[str, Any]) -> Dict[str, Any]:
        layout = {
            "screen_id": "main_screen",
            "components": [
                {
                    "component_id": "title_text",
                    "component_type": "Text",
                    "properties": {
                        "value": {"type": "literal", "value": "Generated App"},
                        "style": {"type": "literal", "value": {"left": 20, "top": 70, "width": 220, "height": 44}},
                    },
                },
                {
                    "component_id": "prompt_input",
                    "component_type": "InputText",
                    "properties": {
                        "placeholder": {"type": "literal", "value": "Type here"},
                        "style": {"type": "literal", "value": {"left": 20, "top": 140, "width": 320, "height": 44}},
                    },
                },
                {
                    "component_id": "submit_button",
                    "component_type": "Button",
                    "properties": {
                        "text": {"type": "literal", "value": "Submit"},
                        "style": {"type": "literal", "value": {"left": 20, "top": 210, "width": 140, "height": 44}},
                    },
                },
            ],
            "layout_metadata": {"generator": "api_pipeline"},
        }
        context["layout"] = layout
        return layout

    def _layout_validation(self, context: Dict[str, Any]) -> Dict[str, Any]:
        validated = EnhancedLayoutDefinition.model_validate(context["layout"])
        context["layout"] = validated.model_dump()
        return {"valid": True, "component_count": len(validated.components)}

    def _blockly_generation(self, context: Dict[str, Any]) -> Dict[str, Any]:
        blockly = {
            "blocks": {
                "languageVersion": 0,
                "blocks": [
                    {
                        "type": "event_when_started",
                        "id": "block_start",
                        "x": 20,
                        "y": 20,
                        "fields": {},
                        "inputs": {},
                    }
                ],
            },
            "variables": [{"id": "var_prompt", "name": "prompt", "type": "String"}],
            "custom_blocks": [],
        }
        context["blockly"] = blockly
        return blockly

    def _blockly_validation(self, context: Dict[str, Any]) -> Dict[str, Any]:
        validated = EnhancedBlocklyDefinition.model_validate(context["blockly"])
        context["blockly"] = validated.model_dump()
        return {"valid": True, "blocks": len(validated.blocks.blocks)}

    def _json_conversion(self, context: Dict[str, Any]) -> Dict[str, Any]:
        raw = {
            "architecture": context["architecture"],
            "layout": context["layout"],
            "blockly": context["blockly"],
        }
        formatted = format_pipeline_output(raw)
        valid, errors = validate_output(formatted)
        context["formatted_result"] = formatted
        context["json_validation"] = {"valid": valid, "errors": errors}
        return {"valid": valid, "errors": errors}


pipeline = APIPipeline()


def run_pipeline(prompt: str) -> Dict[str, Any]:
    return pipeline.run(prompt)
