# Prepare metabolomics data from Su et al. 2020 for FAIR Data Cube

## Setup of project environment

This R project was created with R version 4.1.2 and Bioconductor version 3.14. It uses `renv` for package management. Run `renv::restore()` to restore the package environment. Two additional dependencies need to be installed from GitHub:

```
library(devtools)

devtools::install_github('shizidushu/hfun', dependencies=TRUE)
devtools::install_github("komorowskilab/metafetcher")
```

## Preparing metabolomics data and metadata

The R notebook `convert_data_metadata_chebi.Rmd` makes use of biodbChebi and bridgeDB, and maps metabolite names to ChEBI identifiers. Input data is read from `../data/Su_2020_original`, intermediate annotation files are stored at `../data/Su_2020_intermediate/metabolomics`, output files are stored at `../data/Su_2020_FAIR/metabolomics`. Detailed information on the generated files is available in the [wiki](https://github.com/Xomics/TWOCdemonstrator/wiki).


