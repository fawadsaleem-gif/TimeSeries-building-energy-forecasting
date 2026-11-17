# Building Energy Forecasting

**Time-series AI for building energy decision support**

This project investigates statistical and machine-learning approaches
for forecasting hourly electricity readings in a non-residential
building. It uses the **Building Data Genome Project 2 (BDG2)** dataset
and focuses on the `Panther_office_Karla` meter.

The goal is to support building energy consultants by forecasting
expected short-term electricity readings, understanding demand patterns,
and highlighting periods where actual readings differ from predictions.

> **Scope:** This is a forecasting and decision-support study. It does
> not automatically control building systems or determine the cause of
> unusual readings.

## Project at a glance

  Item                            Description
  ------------------------------- ----------------------------------------
  Dataset                         Building Data Genome Project 2 (BDG2)
  Selected meter                  `Panther_office_Karla`
  Building use                    Office
  Floor area                      2,508.4 m²
  Data frequency                  Hourly
  Analysis period                 20 May 2016 -- 31 December 2017
  Forecast target                 Next-hour recorded electricity reading
  Best model in this experiment   Advanced Random Forest
  Test MAE                        2.200
  Test RMSE                       4.123

The meter's units were not independently verified. Values are therefore
described as **recorded electricity readings**, not kW or kWh.

## Research workflow

1.  **Dataset exploration** --- inspect the electricity data and
    building metadata.
2.  **Data quality assessment** --- investigate missing values and long
    initial zero-reading periods.
3.  **Analysis-period selection** --- use a sustained non-zero recording
    period as a provisional screening criterion.
4.  **Preparation** --- create original and interpolated target series
    and split the data chronologically.
5.  **Statistical forecasting** --- evaluate baseline and time-series
    models.
6.  **Machine-learning forecasting** --- train baseline and
    feature-engineered Random Forest models.
7.  **Evaluation and interpretation** --- compare errors, inspect
    feature importance, and analyse forecast errors.

## Dataset and evaluation

Dataset kaggle link : [[BDG2 Dataset Repository]](https://www.kaggle.com/datasets/claytonmiller/buildingdatagenomeproject2)
The selected meter contains 17,544 hourly timestamps in the original
full-year dataset. The selected analysis period contains 14,166 hourly
observations, from 20 May 2016 18:00 to 31 December 2017 23:00.

A chronological split was used:

  Split        Observations Period
  ---------- -------------- --------------------------------------------------
  Training           11,332 20 May 2016 18:00 -- 4 September 2017 21:00
  Testing             2,834 4 September 2017 22:00 -- 31 December 2017 23:00

The original series contained 11 missing readings in the selected
period. An interpolated series was prepared for modelling. Evaluation
excluded timestamps that were originally missing.

The analysis-period start is a **provisional data-screening decision**,
not proof of the building's official opening date, occupancy, or meter
activation.

## Models evaluated

### Statistical forecasting

-   Naive
-   Seasonal Naive
-   Moving Average
-   Simple Exponential Smoothing (SES)
-   Holt's Linear Trend
-   Holt-Winters Exponential Smoothing
-   ARIMA
-   SARIMA

### Machine learning

-   Baseline Random Forest using lag features
-   Advanced Random Forest using lag, calendar, and rolling-statistic
    features

The advanced Random Forest uses 10 predictors:

-   `lag_1`, `lag_2`, `lag_3`
-   `lag_24`, `lag_48`
-   `hour`
-   `day_of_week`
-   `is_weekend`
-   `rolling_mean_3`
-   `rolling_mean_24`

## Main full-test results

The following models were evaluated over the full 2,834-observation test
period using the project's rolling one-step-ahead evaluation approach.

  Model                                MAE        RMSE
  ---------------------------- ----------- -----------
  **Advanced Random Forest**     **2.200**   **4.123**
  Holt-Winters                       2.461       4.377
  Naive                              2.553       5.523
  ARIMA(1,0,1)                       2.657       5.224
  Baseline Random Forest             2.797       4.976

The advanced Random Forest achieved the lowest MAE and RMSE among the
listed full-test results in this experiment. Adding engineered features
improved the baseline Random Forest MAE by approximately 21.3%.

SARIMA was evaluated over the first seven days of the test period only.
Its results should **not** be directly compared with full-test metrics.

## Key findings

-   The advanced Random Forest performed best among the listed full-test
    model results for this building and evaluation period.
-   Feature engineering improved the baseline Random Forest results.
-   `lag_1` (the previous hour's reading) was the dominant feature in
    the model's importance analyses.
-   Forecast errors were higher around some morning hours (particularly
    06:00--08:00) and around 21:00.
-   Sudden changes in recorded electricity readings remain difficult to
    predict.

These findings describe one meter and one historical evaluation period.
They should not be assumed to generalise to other buildings.

## Forecasting interpretation

The test evaluation uses **rolling one-step-ahead forecasting**:

1.  Predict the next hour.
2.  Once that hour's observed reading becomes available, use it to
    construct features for the next forecast.
3.  Continue through the test period.

The Random Forest was trained once; it was not retrained at every test
hour. This is a historical backtesting workflow, not a forecast made
once for an entire future day or year.

Recursive multi-step forecasting (where earlier predictions become
inputs for later predictions) is a separate next step and requires its
own evaluation.

## Repository structure

``` text
Building-Energy-Forecasting/
├── README.md
├── requirements.txt
├── notebooks/
│   ├── 01_BDG2_Exploration.ipynb
│   └── 02_Machine_Learning_Forecasting.ipynb
├── models/
│   └── random_forest_advanced.pkl       # publish separately if appropriate
├── results/
│   ├── model_comparison.csv
│   ├── feature_importance/
│   └── forecasts/
└── poster/
    └── building_energy_forecasting.png
```

The structure above is a suggested public repository layout. Include
only files that exist in your local project and that are appropriate to
redistribute.

## Setup

Create and activate a Python environment (the project was developed in a
Conda environment):

``` bash
conda create -n building-energy-forecasting python=3.12
conda activate building-energy-forecasting
```

Install the dependencies:

``` bash
pip install -r requirements.txt
```

Start Jupyter:

``` bash
jupyter lab
```

Open the notebooks in numerical order.

## Data access and responsible sharing

The BDG2 source dataset is not included in this repository. Obtain it
from its original distribution source and follow its terms of use.

Do not commit raw, cleaned, or processed dataset files unless you have
confirmed that redistribution is permitted. The notebooks may need local
path adjustments to match your downloaded dataset layout.

## Limitations

-   Only one building meter was selected.
-   The meter's physical unit was not verified.
-   The operational analysis start date is provisional.
-   Eleven originally missing readings were interpolated for modelling;
    evaluation excluded those original missing timestamps.
-   The main Random Forest results use rolling one-step-ahead evaluation
    with newly observed prior readings available at each step.
-   SARIMA was evaluated on a shorter seven-day window.
-   No weather, occupancy, HVAC operating schedule, or other external
    variables were included in the current univariate forecasting
    experiment.
-   Point forecasts are provided; prediction intervals and calibrated
    uncertainty estimates have not yet been developed.

## Future work

-   Evaluate recursive 24-hour and 7-day forecasting.
-   Compare models using consistent forecast horizons and evaluation
    procedures.
-   Investigate weather and operational variables as additional
    predictors.
-   Test the workflow on multiple buildings.
-   Develop forecast uncertainty estimates.
-   Explore a consultant-facing interface for reviewing forecasts and
    deviations.

## Acknowledgements

This project uses data from the Building Data Genome Project 2 (BDG2).
The work is an educational and research-oriented forecasting study.
