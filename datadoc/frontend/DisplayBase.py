from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Type, List, Callable
from pydantic import BaseModel
from dash import dcc
from dash.development.base_component import Component

from datadoc.Enums import SupportedLanguages
from datadoc import state


INPUT_KWARGS = {
    "debounce": True,
    "style": {"width": "100%"},
    "className": "ssb-input",
}
NUMBER_KWARGS = dict(**INPUT_KWARGS, **{"type": "number"})
DROPDOWN_KWARGS = {
    "style": {"width": "100%"},
    "className": "ssb-dropdown",
}


def kwargs_factory():
    """For initialising the field extra_kwargs. We aren't allowed to
    directly assign a mutable type like a dict to a dataclass field"""
    return INPUT_KWARGS


def get_standard_metadata(metadata: BaseModel, identifier: str) -> Any:
    return metadata.dict()[identifier]


def get_multi_language_metadata(
    metadata: BaseModel, identifier: str
) -> Optional[SupportedLanguages]:
    value = getattr(metadata, identifier)
    if value is None:
        return value
    return getattr(value, state.CURRENT_METADATA_LANGUAGE)


@dataclass
class DisplayMetadata:
    identifier: str
    display_name: str
    description: str
    obligatory: bool = False
    editable: bool = True
    multiple_language_support: bool = False


@dataclass
class DisplayVariablesMetadata(DisplayMetadata):
    options: Optional[Dict[str, List[Dict[str, str]]]] = None
    presentation: Optional[str] = "input"


@dataclass
class DisplayDatasetMetadata(DisplayMetadata):
    extra_kwargs: Dict[str, Any] = field(default_factory=kwargs_factory)
    component: Type[Component] = dcc.Input
    options: Optional[Dict[str, List[Dict[str, str]]]] = None
    value_getter: Callable[[BaseModel, str], Any] = get_standard_metadata
