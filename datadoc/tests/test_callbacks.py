from copy import deepcopy

from datadoc.Enums import DatasetState, SupportedLanguages, VariableRole
from datadoc.Model import LanguageStrings
from datadoc.tests.utils import TEST_PARQUET_FILEPATH
import datadoc.state as state
from datadoc.DataDocMetadata import DataDocMetadata
from datadoc import Callbacks


DATA_ORIGINAL = [
    {
        "short_name": "pers_id",
        "variable_role": None,
    },
]
DATA_VALID = [
    {
        "short_name": "pers_id",
        "variable_role": "IDENTIFIER",
    },
]
DATA_INVALID = [
    {
        "short_name": "pers_id",
        "variable_role": 3.1415,
    },
]


def test_accept_variable_metadata_input_no_change_in_data():
    state.metadata = DataDocMetadata(TEST_PARQUET_FILEPATH)
    output = Callbacks.accept_variable_metadata_input(DATA_ORIGINAL, DATA_ORIGINAL)
    assert output[0] == DATA_ORIGINAL
    assert output[1] is False
    assert output[2] == ""


def test_accept_variable_metadata_input_new_data():
    state.metadata = DataDocMetadata(TEST_PARQUET_FILEPATH)
    output = Callbacks.accept_variable_metadata_input(DATA_VALID, DATA_ORIGINAL)

    assert (
        state.metadata.variables_lookup["pers_id"].variable_role
        == VariableRole.IDENTIFIER
    )
    assert output[0] == DATA_VALID
    assert output[1] is False
    assert output[2] == ""


def test_accept_variable_metadata_input_incorrect_data_type():
    state.metadata = DataDocMetadata(TEST_PARQUET_FILEPATH)
    previous_metadata = deepcopy(state.metadata.meta.variables)
    output = Callbacks.accept_variable_metadata_input(DATA_INVALID, DATA_ORIGINAL)

    assert output[0] == DATA_ORIGINAL
    assert output[1] is True
    assert "validation error for DataDocVariable" in output[2]
    assert state.metadata.meta.variables == previous_metadata


def test_accept_dataset_metadata_input_new_data():
    state.metadata = DataDocMetadata(TEST_PARQUET_FILEPATH)
    output = Callbacks.accept_dataset_metadata_input(
        DatasetState.INPUT_DATA, "dataset_state"
    )
    assert output[0] is False
    assert output[1] == ""
    assert state.metadata.meta.dataset.dataset_state == DatasetState.INPUT_DATA


def test_accept_dataset_metadata_input_incorrect_data_type():
    state.metadata = DataDocMetadata(TEST_PARQUET_FILEPATH)
    output = Callbacks.accept_dataset_metadata_input(3.1415, "dataset_state")
    assert output[0] is True
    assert "validation error for DataDocDataSet" in output[1]


def test_change_language():
    ENGLISH_NAME = "English Name"
    BOKMÅL_NAME = "Bokmål Name"
    state.metadata = DataDocMetadata(TEST_PARQUET_FILEPATH)
    state.metadata.meta.dataset.name = LanguageStrings(en=ENGLISH_NAME, nb=BOKMÅL_NAME)
    output = Callbacks.change_language(SupportedLanguages.NORSK_BOKMÅL)
    assert ENGLISH_NAME not in output
    assert BOKMÅL_NAME in output
    output = Callbacks.change_language(SupportedLanguages.ENGLISH)
    assert ENGLISH_NAME in output
    assert BOKMÅL_NAME not in output
