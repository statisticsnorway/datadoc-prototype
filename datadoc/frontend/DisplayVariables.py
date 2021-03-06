from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional

from datadoc.Enums import Datatype, VariableRole


class VariableIdentifiers(str, Enum):
    """As defined here: https://statistics-norway.atlassian.net/wiki/spaces/MPD/pages/3042869256/Variabelforekomst"""

    SHORT_NAME = "short_name"
    NAME = "name"
    DATA_TYPE = "datatype"
    VARIABLE_ROLE = "variable_role"
    DEFINITION_URI = "definition_uri"
    DIRECT_PERSON_IDENTIFYING = "direct_person_identifying"
    DATA_SOURCE = "data_source"
    POPULATION_DESCRIPTION = "population_description"
    COMMENT = "comment"
    TEMPORALITY_TYPE = "temporality_type"
    MEASUREMENT_UNIT = "measurement_unit"
    FORMAT = "format"
    CLASSIFICATION_URI = "classification_uri"
    SENTINEL_VALUE_URI = "sentinel_value_uri"
    INVALID_VALUE_DESCRIPTION = "invalid_value_description"
    IDENTIFIER = "id"
    CONTAINS_DATA_FROM = "contains_data_from"
    CONTAINS_DATA_UNTIL = "contains_data_until"


@dataclass
class DisplayMetadata:
    identifier: str
    display_name: str
    description: str
    options: Optional[Dict[str, List[Dict[str, str]]]] = None
    obligatory: bool = False
    presentation: Optional[str] = "input"
    editable: bool = True


DISPLAY_VARIABLES = {
    VariableIdentifiers.SHORT_NAME: DisplayMetadata(
        # https://statistics-norway.atlassian.net/wiki/spaces/MPD/pages/3042869256/Variabelforekomst#shortName
        identifier=VariableIdentifiers.SHORT_NAME.value,
        display_name="Kortnavn",
        description="Fysisk navn på variabelen i datasettet. Bør tilsvare anbefalt kortnavn.",
        obligatory=True,
        editable=False,
    ),
    VariableIdentifiers.NAME: DisplayMetadata(
        # https://statistics-norway.atlassian.net/wiki/spaces/MPD/pages/3042869256/Variabelforekomst#name
        identifier=VariableIdentifiers.NAME.value,
        display_name="Navn",
        description="Variabelnavn kan arves fra VarDef, men kan også dokumenteres/endres her.",
        obligatory=True,
    ),
    VariableIdentifiers.DATA_TYPE: DisplayMetadata(
        # https://statistics-norway.atlassian.net/wiki/spaces/MPD/pages/3042869256/Variabelforekomst#datatype
        identifier=VariableIdentifiers.DATA_TYPE.value,
        display_name="Datatype",
        description="Datatype",
        obligatory=True,
        presentation="dropdown",
        options={"options": [{"label": i.name, "value": i.name} for i in Datatype]},
    ),
    VariableIdentifiers.VARIABLE_ROLE: DisplayMetadata(
        # https://statistics-norway.atlassian.net/wiki/spaces/MPD/pages/3042869256/Variabelforekomst#variabelRole
        identifier=VariableIdentifiers.VARIABLE_ROLE.value,
        display_name="Variabelens rolle",
        description="Variabelens rolle i datasett",
        obligatory=True,
        presentation="dropdown",
        options={"options": [{"label": i.name, "value": i.name} for i in VariableRole]},
    ),
    VariableIdentifiers.DEFINITION_URI: DisplayMetadata(
        # https://statistics-norway.atlassian.net/wiki/spaces/MPD/pages/3042869256/Variabelforekomst#definitionUri
        identifier=VariableIdentifiers.DEFINITION_URI.value,
        display_name="Definition URI",
        description="En lenke (URI) til variabelens definisjon i SSB (Vardok/VarDef)",
        obligatory=True,
    ),
    VariableIdentifiers.DIRECT_PERSON_IDENTIFYING: DisplayMetadata(
        # https://statistics-norway.atlassian.net/wiki/spaces/MPD/pages/3042869256/Variabelforekomst#directPersonIdentifying
        identifier=VariableIdentifiers.DIRECT_PERSON_IDENTIFYING.value,
        display_name="DPI",
        description="Direkte personidentifiserende informasjon (DPI)",
        obligatory=True,
        presentation="dropdown",
        options={
            "options": [
                {"label": "Ja", "value": "True"},
                {"label": "Nei", "value": "False"},
            ]
        },
    ),
    VariableIdentifiers.DATA_SOURCE: DisplayMetadata(
        # https://statistics-norway.atlassian.net/wiki/spaces/MPD/pages/3042869256/Variabelforekomst#dataSource
        identifier=VariableIdentifiers.DATA_SOURCE.value,
        display_name="Datakilde",
        description="Datakilde. Settes på datasettnivå, men kan overstyres på variabelforekomstnivå.",
    ),
    VariableIdentifiers.POPULATION_DESCRIPTION: DisplayMetadata(
        # https://statistics-norway.atlassian.net/wiki/spaces/MPD/pages/3042869256/Variabelforekomst#populationDescription
        identifier=VariableIdentifiers.POPULATION_DESCRIPTION.value,
        display_name="Populasjonen",
        description="Populasjonen variabelen beskriver kan spesifiseres nærmere her. Settes på datasettnivå, men kan overstyres på variabelforekomstnivå.",
    ),
    VariableIdentifiers.COMMENT: DisplayMetadata(
        # https://statistics-norway.atlassian.net/wiki/spaces/MPD/pages/3042869256/Variabelforekomst#comment
        identifier=VariableIdentifiers.COMMENT.value,
        display_name="Kommentar",
        description="Ytterligere presiseringer av variabeldefinisjon",
    ),
}

OBLIGATORY_VARIABLES_METADATA = [
    m.identifier for m in DISPLAY_VARIABLES.values() if m.obligatory
]
