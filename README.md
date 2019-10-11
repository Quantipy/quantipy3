# Quantipy

### Python for people data
Quantipy is an open-source data processing, analysis and reporting software project that builds on the excellent pandas and numpy libraries. Aimed at people data, Quantipy offers support for native handling of special data types like multiple choice variables, statistical analysis using case or observation weights, DataFrame metadata and pretty data exports.

### Quantipy for Python 3
This repository is a port of [Quantipy](https://www.github.com/quantipy/quantipy) from Python 2.x to Python 3.

When adding features to classes such as DataSet, the test suite for DataSet can be run with the command, until the test suite is cleaned up.

`python3 -m unittest tests.test_dataset`

The DataSet suite of features are ready for production use, [the batch operations are not](SupportedFeaturesPython3.md).

### Key features
  - Reads plain .csv, converts from Dimensions, SPSS, Decipher, or Ascribe
  - Open metadata format to describe and manage datasets
  - Powerful, metadata-driven cleaning, editing, recoding and transformation of datasets
  - Computation and assessment of data weights
  - Easy-to-use analysis interface
  - Automated data aggregation using ``Batch`` defintions
  - Structured analysis and reporting via Chain and Cluster containers
  - Exports to SPSS, Dimensions ddf/mdd, MS Excel and Powerpoint with flexible layouts and various options

#### Contributors
- Alexander Buchhammer, Alasdair Eaglestone, James Griffiths, Kerstin Müller : https://yougov.co.uk
- Datasmoothie’s Birgir Hrafn Sigurðsson and Geir Freysson: http://www.datasmoothie.com

## Docs
[View the documentation at readthedocs.org](http://quantipy.readthedocs.io/)

### Required libraries before installation
We recommend installing [Anaconda for Python 3](http://continuum.io/downloads)
which will provide most of the required libraries and an easy means of keeping
them up-to-date over time.
  - Python 3
  - Numpy
  - Pandas

### Developing

#### Windows

Dependencies numpy and scipy are handled by conda.
Create a virtual environment:
```python
conda create -n envqp python=3
```
Install in editable mode:
```python
pip install -r requirements_dev.txt
```

#### Linux
Dependencies numpy and scipy are handled in the installation.

Create a virtual environment:
```python
conda create -n envqp python=3
```
Install in editable mode:
```python
pip install -r requirements_dev.txt
```

## 5-minutes to Quantipy

**Get started**

Start a new folder called 'Quantipy-5' and add a subfolder called 'data'.

You can find an example dataset in quantipy/tests:

- Example Data (A).csv
- Example Data (A).json

Put these files into your ``'data'`` folder.

Start with some import statements:

```python
import pandas as pd
import quantipy as qp

from quantipy.core.tools.dp.prep import frange

# This is a handy bit of pandas code to let you display your dataframes
# without having them split to fit a vertical column.
pd.set_option('display.expand_frame_repr', False)
```

**Load, inspect and edit your data**

Load the input files in a ``qp.DataSet`` instance and inspect the metadata
with methods like ``.variables()``, ``.meta()`` or ``.crosstab()``:
```python
# Define the paths of your input files
path_json = './data/Example Data (A).json'
path_csv = './data/Example Data (A).csv'

dataset = qp.DataSet('Example Data (A)')
dataset.read_quantipy(path_json, path_csv)

dataset.crosstab('q2', text=True)
```

```
Question                                                           q2. Which, if any, of these other sports have you ever participated in?
Values                                                                                                                                   @
Question                                           Values
q2. Which, if any, of these other sports have y... All                                                         2999.0
                                                   Sky diving                                                  1127.0
                                                   Base jumping                                                1366.0
                                                   Mountain biking                                             1721.0
                                                   Kite boarding                                                649.0
                                                   Snowboarding                                                 458.0
                                                   Parachuting                                                  428.0
                                                   Other                                                        492.0
                                                   None of these                                                 53.0
```

Variables can be created, recoded or edited with DataSet methods, e.g. ``derive()``:
```python
mapper = [(1,  'Any sports', {'q2': frange('1-6, 97')}),
          (98, 'None of these', {'q2': 98})]

dataset.derive('q2_rc', 'single', dataset.text('q2'), mapper)
dataset.meta('q2_rc')
```

```
single                                              codes          texts missing
q2_rc: Which, if any, of these other sports hav...
1                                                       1     Any sports    None
2                                                      98  None of these    None
```

The  ``DataSet`` case data component can be inspected with the []-indexer, as known from a ``pd.DataFrame``:
```python

dataset[['q2', 'q2_rc']].head(5)
```

```
        q2  q2_rc
0  1;2;3;5;    1.0
1      3;6;    1.0
2       NaN    NaN
3       NaN    NaN
4       NaN    NaN
```
