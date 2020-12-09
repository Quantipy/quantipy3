import quantipy as qp
import pandas as pd
import json, pytest


@pytest.fixture
def confirmit_dataset():
    dataset = qp.DataSet("confirmit")
    dataset.read_confirmit_from_files('tests/confirmit_meta.json',
                           'tests/confirmit_data.json'
                            )
    return dataset


@pytest.fixture
def quantipy_dataset():
    dataset = qp.DataSet("quantipy test data")
    dataset.read_quantipy('tests/Example Data (A).json',
                                     'tests/Example Data (A).csv')
    return dataset


def test_reader(quantipy_dataset):
    assert quantipy_dataset.variables() == ['record_number', 'unique_id', 'age', 'birth_day', 'birth_month', 'birth_year', 'gender', 'locality', 'ethnicity', 'religion', 'q1', 'q2', 'q2b', 'q3', 'q4', 'q5.q5_grid', 'q6.q6_grid', 'q7.q7_grid', 'q8', 'q8a', 'q9', 'q9a', 'Wave', 'weight_a', 'weight_b', 'start_time', 'end_time', 'duration', 'q14_1.q14_1_grid', 'q14_2.q14_2_grid', 'q14_3.q14_3_grid', 'RecordNo']
    assert quantipy_dataset.by_type().shape == (56, 9)
    assert type(quantipy_dataset._data) == pd.DataFrame
    print("NOTE: This is what the dataset.meta() function should return")
    print(quantipy_dataset.meta('gender'))
    print("\n\nNOTE: this is what a crosstab should look like")
    print(quantipy_dataset.crosstab('q4', 'gender'))
    print("\n\nNOTE: this is what the _data object should look like")
    print(quantipy_dataset._data.iloc[:,4:13].head())

    columns = set(quantipy_dataset._meta['columns'].keys())
    meta_columns = set(quantipy_dataset._meta['columns'].keys())
    # check that every column in the data (columns) is also in the meta
    assert columns.issubset(meta_columns)
    # import pdb; pdb.set_trace()


def test_single_type(confirmit_dataset):
    # single type - no loop reference
    print(confirmit_dataset.meta('q39'))
    assert confirmit_dataset.crosstab('q39').shape == (3,1)
    print(confirmit_dataset.meta('q21'))
    assert confirmit_dataset.crosstab('q21').shape == (5,1)
    print(confirmit_dataset.crosstab('q39', 'q21'))
    assert confirmit_dataset.crosstab('q39', 'q21').shape == (3,5)
    assert confirmit_dataset.meta()['columns']['q39'] == json.loads("""
    {"name": "q39",
    "parent": {},
    "type": "single",
    "values": [
        {"text": {"en": "yes"},
        "value": 1},
        {"text": {"en": "no"},
        "value": 2}],
    "text": {"en": "Use script to set values"}}""")
    # single type - with loop reference
    assert confirmit_dataset.meta()['columns']['q55']['values'][1] == json.loads("""
    {"text": {"en": "loopAns1"},
    "value":
    {"name": "l2",
    "parent": {},
    "type": "single",
    "values": [
        {"text": {"en": "loopAns1"},
        "value": 1},
        {"text": {"en": "loopAns2"},
        "value": 2},
        {"text": {"en": "loopAns3"}, "value": 3}],
        "text": {"en": "Loop  l2 title"},
        "texts": [{"languageId": 9,
        "text": "Loop  l2 title"}],
        "variables": [{"name": "q56",
        "parent": {},
        "type": "string",
        "properties": {},
        "text": {"en": ""}}]}}""")
    
    # TODO: assert that dataset.crosstab(single) returns correct shaped
    #       dataframe
    #       assert dataset.crosstab('q39').shape == (1,1)

    # TODO: more assertions for numbers, grids etc. these can be in different
    #       test functions if that is needed

def test_delimited_set_type(confirmit_dataset):
    print(confirmit_dataset.meta('q1'))
    assert confirmit_dataset.meta()['columns']['q1'] == json.loads("""
    {"name": "q1",
    "parent": {},
    "type": "delimited set",
    "properties": {},
    "values": [
        {"text": {"en": "ans1"}, "value": 1},
        {"text": {"en": "ans2"}, "value": 2},
        {"text": {"en": "ans3"}, "value": 3}],
        "text": {"en": "multi - default options"}}""")
    assert confirmit_dataset.crosstab('q1').shape == (4,1)
    print(confirmit_dataset.crosstab('q1', 'q22'))
    assert confirmit_dataset.crosstab('q1', 'q22').shape == (4,5)

def test_number_type(confirmit_dataset):
    print(confirmit_dataset.meta('q73'))
    print(confirmit_dataset.crosstab('q73'))
    assert confirmit_dataset.meta()['columns']['q73'] == json.loads("""
    {"name": "q73",
    "parent": {},
    "type": "float",
    "text": {"en": "open - numeric"}}
    """)
    assert confirmit_dataset.crosstab('q73').shape == (71, 1)
    assert confirmit_dataset.crosstab('q73', 'q39').shape == (71, 3)

def test_array_type(confirmit_dataset):
    print(confirmit_dataset.meta()['columns']['q5_1'])
    assert confirmit_dataset.crosstab('q5_1', 'q39').shape == (52, 3)
    assert confirmit_dataset.meta()['masks']['q5'] == json.loads("""
    {"name": "q5",
    "parent": {},
    "type": "array",
    "properties": {},
    "items": [
        {"properties": {},
        "source": "columns@q5_1",
        "text": {"en": "ans1"}},
        {"properties": {},
        "source": "columns@q5_2",
        "text": {"en": "ans2"}},
        {"properties": {},
        "source": "columns@q5_3",
        "text": {"en": "ans3"}}],
        "subtype": "float",
        "text": {"en": "numeric list"}}""")

    assert confirmit_dataset.meta()['columns']['q5_1'] == json.loads("""
    {"name": "q5_1",
    "parent": {
        "masks@q5":
        {"type": "array"}},
        "text": {"en": "ans1"},
        "type": "float"}""")


def test_rating_type(confirmit_dataset):
    print(confirmit_dataset.meta()['columns']['q14_1'])
    assert confirmit_dataset.crosstab('q14_1', 'q39').shape == (4, 3)
    print(confirmit_dataset.meta()['masks']['q14'])
    assert confirmit_dataset.meta()['masks']['q14'] == json.loads("""
    {
        "name": "q14",
        "parent": {},
        "type": "array",
        "properties": {},
        "items": [{
            "properties": {},
            "source": "columns@q14_1",
            "text": {"en": "ans1"}
        },
        {
            "properties": {},
            "source": "columns@q14_2",
            "text": {"en": "ans2"}
        },
        {
            "properties": {},
            "source": "columns@q14_3",
            "text": {"en": "ans3"}
        }],
        "subtype": "single",
        "values": "lib@values@q14",
        "text": {"en": "grid - numeric precodes"}
    }""")

    assert confirmit_dataset.meta()['columns']['q14_1'] == json.loads("""
    {
        "name": "q14_1",
        "parent": {
            "masks@q14": {"type": "array"}
        },
        "text": {"en": "ans1"},
        "type": "single",
        "values": "lib@values@q14"
    }""")


def test_ranking_type(confirmit_dataset):
    print(confirmit_dataset.meta()['columns']['q2_1'])
    assert confirmit_dataset.crosstab('q2_1', 'q39').shape == (11, 3)
    print(confirmit_dataset.meta()['masks']['q2'])
    assert confirmit_dataset.meta()['masks']['q2'] == json.loads("""
    {
        "name": "q2",
        "parent": {},
        "type": "array",
        "properties": {},
        "items": [{
            "properties": {},
            "source": "columns@q2_1",
            "text": {"en": "ans1"}
        },
        {
            "properties": {},
            "source": "columns@q2_2",
            "text": {"en": "ans2"}
        },
        {
            "properties": {},
            "source": "columns@q2_3",
            "text": {"en": "ans3"}
        },
        {
            "properties": {},
            "source": "columns@q2_4",
            "text": {"en": "ans4"}
        },
        {
            "properties": {},
            "source": "columns@q2_5",
            "text": {"en": "ans5"}
        },
        {
            "properties": {},
            "source": "columns@q2_6",
            "text": {"en": "ans6"}
        },
        {
            "properties": {},
            "source": "columns@q2_7",
            "text": {"en": "ans7"}
        },
        {
            "properties": {},
            "source": "columns@q2_8",
            "text": {"en": "ans8"}
        },
        {
            "properties": {},
            "source": "columns@q2_9",
            "text": {"en": "ans9"}
        },
        {
            "properties": {},
            "source": "columns@q2_10",
            "text": {"en": "ans10"}
        }],
        "subtype": "int",
        "text": {"en": "ranking- ordered (10 answers)"}
    }""")

    assert confirmit_dataset.meta()['columns']['q2_1'] == json.loads("""
    {
        "name": "q2_1",
        "parent": {
            "masks@q2": {"type": "array"}
        },
        "text": {"en": "ans1"},
        "type": "int"
    }""")


def test_multigrid_type(confirmit_dataset):
    print(confirmit_dataset.meta()['masks']['g56'])
    print(confirmit_dataset.crosstab('g56_1'))
    assert confirmit_dataset.crosstab('g56_1', 'q39').shape == (3, 3)
    print(confirmit_dataset.meta()['masks']['g56'])
    assert confirmit_dataset.meta()['masks']['g56'] == json.loads("""
    {
        "name": "g56",
        "parent": {},
        "type": "array",
        "properties": {},
        "items": [{
            "properties": {},
            "source": "columns@g56_1",
            "text": {"en": "a"}
        },
        {
            "properties": {},
            "source": "columns@g56_2",
            "text": {"en": "b"}
        },
        {
            "properties": {},
            "source": "columns@g56_3",
            "text": {"en": "c"}
        }],
        "subtype": "delimited set",
        "values": "lib@values@g56",
        "text": {"en": ""}
        }
    """)

def test_read_from_api():
    dataset_from_api = qp.DataSet("confirmit")
    dataset_from_api.read_confirmit_api( projectid="p913481003361",
                                public_url="https://ws.euro.confirmit.com/",
                                idp_url="https://idp.euro.confirmit.com/",
                                client_id="71a15e5d-b52d-4534-b54b-fa6e2a9da8a7",
                                client_secret="2a943d4d-58ab-42b8-a276-53d07ad34064"
                                )
    print(dataset_from_api.meta('q39'))
    assert dataset_from_api.crosstab('q39').shape == (3,1)
    print(dataset_from_api.meta('q21'))
    assert dataset_from_api.crosstab('q21').shape == (6,1)
    print(dataset_from_api.crosstab('q39', 'q21'))
    assert dataset_from_api.crosstab('q39', 'q21').shape == (3,6)
    assert dataset_from_api.meta()['columns']['q39'] == json.loads("""
    {"name": "q39",
    "parent": {},
    "type": "single",
    "values": [
        {"text": {"en": "yes"},
        "value": 1},
        {"text": {"en": "no"},
        "value": 2}],
    "text": {"en": "Use script to set values"}}""")
