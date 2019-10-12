# Quantipy

### Python for people data
Quantipy is an open-source data processing, analysis and reporting software project that builds on the excellent pandas and numpy libraries. Aimed at people data, Quantipy offers support for native handling of special data types like multiple choice variables, statistical analysis using case or observation weights, DataFrame metadata and pretty data exports.

### Quantipy for Python 3
This repository is a port of [Quantipy](https://www.github.com/quantipy/quantipy) from Python 2.x to Python 3.

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

## Installation
Quantipy is currently not published on pip (there's an [issue](https://github.com/Quantipy/quantipy3/issues/1) for that, if you want to help out.)

To start using Quantipy we

1. Create a virtual environment
1. Download or clone the library
1. Install the required packages

#### 1. Create a virtual envirionment


Create a virtual environment:

conda
```python
conda create -n envqp python=3
```

with venv
```python
python -m venv [your_env_name]
 ```

#### 2. Download or clone library

```
git clone https://github.com/Quantipy/quantipy3.git
```

Add the quantipy3 folder that is created to your path, so you can import quantipy from wherever you are working.

#### 3. Install required libraries

Activate your virtual environment and install all the required packages.

```
source [yourenv]/bin/activate
pip install -r quantipy3/requirements.txt
```

You're all set, now you can start crunching your survey data with ease.

## 5-minutes to Quantipy

**Get started**

If you are working with SPSS, import your sav file.

```
import quantipy as qp
dataset = qp.DataSet.("My dataset, wave 1")
dataset.read_spss('my_file.sav')
```

You can start straight away by exploring what variables are in your file.

```
dataset.variables()
```
```
['gender',
 'agecat',
 'price_satisfaction',
 'numitems_satisfaction',
 'org_satisfaction',
 'service_satisfaction',
 'quality_satisfaction',
 'overall_satisfaction',
 'weight']
```

If you want more details on a variable, explore it's meta data.

```
dataset.meta('agecat')
```


<table border="1" class="dataframe">  <thead>    <tr style="text-align: right;">      <th>single</th>      <th>codes</th>      <th>texts</th>      <th>missing</th>    </tr>    <tr>      <th>agecat: Age category</th>      <th></th>      <th></th>      <th></th>    </tr>  </thead>  <tbody>    <tr>      <th>1</th>      <td>1</td>      <td>18-24</td>      <td>None</td>    </tr>    <tr>      <th>2</th>      <td>2</td>      <td>25-34</td>      <td>None</td>    </tr>    <tr>      <th>3</th>      <td>3</td>      <td>35-49</td>      <td>None</td>    </tr>    <tr>      <th>4</th>      <td>4</td>      <td>50-64</td>      <td>None</td>    </tr>    <tr>      <th>5</th>      <td>5</td>      <td>64+</td>      <td>None</td>    </tr>  </tbody></table>

Quantipy knows out-of-the-box what SPSS's meta data means and uses it correctly. All codes and labels are the same as in the sav file.

**Calculate some results, counts or percentages**

```
dataset.crosstab('price_satisfaction', 'gender')
```

<table border="1" class="dataframe">  <thead>    <tr>      <th></th>      <th>Question</th>      <th colspan="6" halign="left">agecat. Age category</th>    </tr>    <tr>      <th></th>      <th>Values</th>      <th>All</th>      <th>18-24</th>      <th>25-34</th>      <th>35-49</th>      <th>50-64</th>      <th>64+</th>    </tr>    <tr>      <th>Question</th>      <th>Values</th>      <th></th>      <th></th>      <th></th>      <th></th>      <th></th>      <th></th>    </tr>  </thead>  <tbody>    <tr>      <th rowspan="6" valign="top">price_satisfaction. Price satisfaction</th>      <th>All</th>      <td>582.0</td>      <td>46.0</td>      <td>127.0</td>      <td>230.0</td>      <td>147.0</td>      <td>32.0</td>    </tr>    <tr>      <th>Strongly Negative</th>      <td>72.0</td>      <td>8.0</td>      <td>20.0</td>      <td>22.0</td>      <td>17.0</td>      <td>5.0</td>    </tr>    <tr>      <th>Somewhat Negative</th>      <td>135.0</td>      <td>10.0</td>      <td>30.0</td>      <td>52.0</td>      <td>38.0</td>      <td>5.0</td>    </tr>    <tr>      <th>Neutral</th>      <td>140.0</td>      <td>9.0</td>      <td>32.0</td>      <td>59.0</td>      <td>36.0</td>      <td>4.0</td>    </tr>    <tr>      <th>Somewhat Positive</th>      <td>145.0</td>      <td>12.0</td>      <td>25.0</td>      <td>63.0</td>      <td>33.0</td>      <td>12.0</td>    </tr>    <tr>      <th>Strongly Positive</th>      <td>90.0</td>      <td>7.0</td>      <td>20.0</td>      <td>34.0</td>      <td>23.0</td>      <td>6.0</td>    </tr>  </tbody></table>

You can also filter

```
dataset.crosstab('price_satisfaction', 'agecat', f={'gender':1})
```

and use a weight column

```
dataset.crosstab('price_satisfaction', 'agecat', f={'gender':1}, w="weight")

```

Variables can be created, recoded or edited with DataSet methods, e.g. ``derive()``:
```python
mapper = [(1,  '18-35 year old', {'agecat': [1,2]}),
          (2, '36 and older', {'agecat': [3,4,5]})]

dataset.derive('two_age_groups', 'single', dataset.text("Older or younger than 35"), mapper)
dataset.meta('two_age_groups')
```

```
single                                              codes     texts              missing
two_age_groups: "Older or youngar than 35"
1                                                       1     18-35 years old    None
2                                                       2     36 and older       None
```

The  ``DataSet`` case data component can be inspected with the []-indexer, as known from a ``pd.DataFrame``:
```python

dataset[['gender', 'age']].head(5)
```

```
        gender  age
0       1.0    1.0
1       2.0    1.0
2       2.0    2.0
3       1.0    NaN
4       NaN    1.0
```

# Contributing

The test suite for Quantipy can be run with the command

`python3 -m unittest`

But when developing a specific aspect of Quantipy, it might be quicker to run (e.g. for the DataSet)

`python3 -m unittest tests.test_dataset`

Tests for unsupported features are skipped, [see here for what tests are supported](SupportedFeaturesPython3.md).

We welcome volunteers and supporters. Please include a test case with any pull request, especially those that run calculations.
