Nikko Cleri
May 2025

The models created here are to be used in Cleri et al. in prep., part of JWST-AR-05558, which will study the major optical line ratio diagnostics of ionizing sources at a large range of redshifts.
As a part of this work, we have produced a large model library from the photoionization modeling code Cloudy, which models the nebular emission for many different permutations of ionizing SED, metallicity, and other parameters. 

The code uses an input builder tool and a slurm file builder tool from my (Nikko's) GitHub (github.com/njcleri/nikkos-tools). 

There are many different permutations of model parameters which we test, described here.

For all models, we iterate over:
- dimensionless ionization parameter (closed boundaries):
    log(U) = -4.0 to log(U) = -1.0 in steps of 0.25
    13 total log(U) steps

- Hydrogen density:
    We run two densities, log(n_H/cm^-3) = 2, 3

***BPASS STELLAR MODELS***
For BPASS stellar models (using v2.2.1, Stanway & Eldridge 2018):

- Initial Mass Functions:
    The initial mass functions from BPASS are two-component power laws. 
    For alpha_1 and alpha_2 representing the low- and high-mass power law slopes, M_1 representing the boundary between the mass regimes, and M_max representing the high-mass cutoff, we use:
        100_300: alpha_1 = -1.30, alpha_2 = -2.00, M_1 = 0.5 M_solar, M_max = 300 M_solar
        135_300: alpha_1 = - 1.30, alpha_2 = -2.35, M_1 = 0.5 M_solar, M_max = 300 M_solar
        170_300: alpha_1 = -1.30, alpha_2 = -2.70, M_1 = 0.5 M_solar, M_max = 300 M_solar
        chab300: alpha_1 = exponential cut-off (Chabrier 2003), alpha_2 = -2.30, M_1 = 1.0 M_solar, M_max = 300 M_solar
    for 4 total IMF slope/cutoff combinations.

- Stellar Ages: 
    The BPASS stellar ages are given in 0.1 dex increments from log(age/years)=6.0 to log(age/years)=11. 
    As we are interested in saving computation time, we prioritize a finer grid at younger ages.

    The age grid we employ is (closed boundaries):
        log(age/years)=6.0 to log(age/years)=8.0 in steps of 0.1, and
        log(age/years)=8.5 to log(age/years)=11 in steps of 0.5
    for 27 total age steps.

- Stellar Metallicities: 
    BPASS gives stellar metallicity mass fractions in absolute units (Z_solar = 0.020):
        0.00001, 0.0001, 0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.008, 0.010, 0.014, 0.020, 0.040
    for total 13 steps in metallicity. In solar units, this is:
        5.0e-04, 5.0e-03, 5.0e-02, 1.0e-01, 1.5e-01, 2.0e-01, 2.5e-01, 3.0e-01, 4.0e-01, 5.0e-01, 7.0e-01, 1.0e+00, 2.0e+00


- Single and Binary Star Models:
    BPASS includes treatment for both isolated single stars and binaries for each IMF.

- Elemental Abundance Scaling:
    The first set of models (labeled solar_abundance_scaling) are have elemental abundances scaled to solar abundance patterns (i.e., element scale factor = 1). 
    The second set of models (labeled non_solar_abundance_scaling) have elemental abundances different from solar abundance patterns.
    All of the abundance scaling is done only on the nebula, i.e., the nebula and stars have different abundance patterns (stellar models with varied abundances were not available at the time of these models being made).
    These include:
        - CNO: varied together from 0.5 to 5 in steps of 0.5
        - alphas (C, O, Ne, S): varied together from 0.5 to 5 in steps of 0.5
        - CN: varied together [0.01, 0.05, 0.1, 0.5, 1.5, 2.0]

The library contains six files for each model:
    - **.in: the 'input', containing the parameters and specifications of the model
    - **.out: the generic Cloudy output (doesn't really matter other than to see the 'Cloudy exited OK')
    - **.ovr: the overview (probably not what you care about)
    - **.con: the continuum (you probably want this one)
    - **.ilin: the intrinsic line emissivities (you probably want this one)
    - **.elin: the emergent line emissivities (you might care about this one but probably not)

The naming convention for the tar files in the library is:
    <BPASS Version>_imf<imf>_burst_<binary/single>_models_complete.tar.gz

and for the individual files:
    sed<SED>_age<log age>zstar<stellar metallicity in solar units>hden<hydrogen density>_z<gas metallicity>_logU<log U>.<file extension>

where <SED> for the BPASS models is:
    <BPASS Version>_imf<imf>_burst_<binary/single>.ascii
    







