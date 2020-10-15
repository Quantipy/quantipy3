# Quantipy3

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

  ### Features not yet supported in Python 3 version
  - Structured analysis and reporting via Chain and Cluster containers
  - Exports to SPSS, Dimensions ddf/mdd, MS Excel and Powerpoint with flexible layouts and various options
  - Python 3.8 is not yet fully supported, but 3.5, 3.6, and 3.7 are.

#### Contributors
- Alexander Buchhammer, Alasdair Eaglestone, James Griffiths, Kerstin Müller : https://yougov.co.uk
- Datasmoothie’s Birgir Hrafn Sigurðsson and [Geir Freysson](http://www.twitter.com/@geirfreysson): http://www.datasmoothie.com

## Installation

`pip install quantipy3`

or

`python3 -m pip install quantipy3`

Note that the package is called __quantipy3__ on pip.

#### Create a virtual envirionment

If you want to create a virtual environment when using Quantipy:

conda
```python
conda create -n envqp python=3
```

with venv
```python
python -m venv [your_env_name]
 ```

## 5-minutes to Quantipy

**Get started**

If you are working with SPSS, import your sav file.

```
import quantipy as qp
dataset = qp.DataSet("My dataset, wave 1")
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

#### Weighting
If your data hasn't been weighted yet, you can use Quantipy's RIM weighting algorithm.

Assuming we have the same variables as before, `gender` and `agecat` we can weight the dataset with these two variables:

```
from quantipy.core.weights.rim import Rim

age_targets = {'agecat':{1:5.0, 2:30.0, 3:26.0, 4:19.0, 5:20.0}}
gender_targets = {'gender':{0:49, 1:51}}
scheme = Rim('gender_and_age')
scheme.set_targets(targets=[age_targets, gender_targets])
dataset.weight(scheme,unique_key='respondentId',
               weight_name="my_weight",
               inplace=True)
```
Quantipy will show you a weighting report:
```
Weight variable       weights_gender_and_age
Weight group                  _default_name_
Weight filter                           None
Total: unweighted                 582.000000
Total: weighted                   582.000000
Weighting efficiency               60.009826
Iterations required                14.000000
Mean weight factor                  1.000000
Minimum weight factor               0.465818
Maximum weight factor               6.187700
Weight factor ratio                13.283522
```

And you can test whether the weighting has worked by running crosstabs:

```
dataset.crosstab('agecat', pct=True, w='my_new_weight')
```

<table border="1" class="dataframe">  <thead>    <tr>      <th></th>      <th>Question</th>      <th>agecat. Age category</th>    </tr>        <tr>      <th>Question</th>      <th>Values</th>      <th></th>    </tr>  </thead>  <tbody>    <tr>      <th rowspan="6" valign="top">agecat. Age category</th>      <th>All</th>      <td>100.0</td>    </tr>    <tr>      <th>18-24</th>      <td>5.0</td>    </tr>    <tr>      <th>25-34</th>      <td>30.0</td>    </tr>    <tr>      <th>35-49</th>      <td>26.0</td>    </tr>    <tr>      <th>50-64</th>      <td>19.0</td>    </tr>    <tr>      <th>64+</th>      <td>20.0</td>    </tr>  </tbody></table>

```
dataset.crosstab('gender', pct=True, w='my_new_weight')
```

<table border="1" class="dataframe">  <thead>    <tr>      <th></th>      <th>Question</th>      <th>gender. Gender</th>        <tr>      <th>Question</th>      <th>Values</th>      <th></th>    </tr>  </thead>  <tbody>    <tr>      <th rowspan="3" valign="top">gender. Gender</th>      <th>All</th>      <td>100.0</td>    </tr>    <tr>      <th>Male</th>      <td>49.0</td>    </tr>    <tr>      <th>Female</th>      <td>51.0</td>    </tr>  </tbody></table>

# Contributing

The test suite for Quantipy can be run with the command

`python3 -m pytest tests`

But when developing a specific aspect of Quantipy, it might be quicker to run (e.g. for the DataSet)

`python3 -m unittest tests.test_dataset`

Tests for unsupported features are skipped, [see here for what tests are supported](SupportedFeaturesPython3.md).

We welcome volunteers and supporters. Please include a test case with any pull request, especially those that run calculations.
