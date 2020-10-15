import quantipy as qp

def test_reader():
    dataset = qp.DataSet("confirmit")
    dataset.read_confirmit('tests/confirmit_meta.json', 'tests/confirmit_data.json')

    # TODO: assert that dataset.crosstab(single) returns correct shaped
    #       dataframe
    #       assert dataset.crosstab('q39').shape == (1,1)

    # TODO: more assertions for numbers, grids etc. these can be in different
    #       test functions if that is needed
