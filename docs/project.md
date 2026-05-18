# Project documentation

## Thesis title

Interpolacija vremenskih podataka pomoću strojnog učenja.

English title:
Time-series data interpolation using machine learning.

## Goal

The goal of this thesis is to compare classical interpolation methods and machine learning methods for reconstructing missing values in time-series data.

## Dataset

The main dataset is the Jena Climate dataset.

It contains high-resolution meteorological measurements recorded every 10 minutes.

The main target variable is temperature.

## Main idea

The original time series contains frequent measurements.

To simulate lower temporal resolution, only every nth value is kept, while intermediate values are removed and treated as missing.

Then different methods are used to reconstruct the removed values.

## Methods

Classical methods:

- forward fill
- linear interpolation
- time interpolation
- cubic interpolation
- spline interpolation

Machine learning methods:

- RandomForestRegressor
- MLPRegressor

## Evaluation metrics

- MAE
- RMSE
- R2 score

## Expected output

The project should produce:

- reconstructed time series
- result tables
- comparison plots
- discussion of which method performs best
