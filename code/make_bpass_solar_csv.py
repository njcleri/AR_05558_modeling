import glob
import pandas as pd

BPASS_solar_path = "/Users/njc5787/Research/cloudy_model_library/cloudy_model_library_complete/BPASS/solar_abundances/"

def clean_cloudy_line_file(filename, name='emissivity'):
    '''
    My method for making cloudy line emissivity files more user friendly. 
    To pull emissivities for a given line from each grid step, 
    read in the df and use df.loc['HE_2_1640.00A'] format. 
    '''
    df = pd.read_csv(filename, sep='\t+', header=0, names=[name], comment='#', engine='python')
    df = df[df.index.str.contains('iteration') == False]
    df.index = df.index.str.replace('  ', '_')
    df.index = df.index.str.replace(' ', '_')
    df.index = df.index.str[:-1]
    
    return df

if __name__ == "__main__":

    catalog = pd.DataFrame()
    for ilin in glob.glob(f"{BPASS_solar_path}/**/**/**.ilin"):
        parameters = ilin.replace(BPASS_solar_path, '').replace('.ilin', '')
        try:
            catalog[parameters] = clean_cloudy_line_file(ilin, name=parameters).copy()
        except:
            print(ilin)
            pass

    BPASS_solar = catalog.T
    BPASS_solar['logU'] = None
    BPASS_solar['zgas'] = None
    BPASS_solar['hden'] = None
    BPASS_solar['zstar'] = None
    BPASS_solar['age'] = None
    BPASS_solar['sed'] = None
    BPASS_solar['binary_or_single'] = None
    BPASS_solar['history'] = None
    BPASS_solar['imf'] = None

    for id, row in BPASS_solar.iterrows():
        logU = float(id.rsplit('logU')[-1])
        zgas = float(id.replace(f'_logU{logU}', '').rsplit('z')[-1])
        hden = int(id.replace(f'_z{zgas}_logU{logU}', '').rsplit('hden')[-1])
        zstar = float(id.replace(f'_hden{hden}_z{zgas}_logU{logU}', '').rsplit('zstar')[-1])
        age = float(id.replace(f'_zstar{zstar}_hden{hden}_z{zgas}_logU{logU}', '').rsplit('age')[-1])
        sed = str(id.replace(f'_age{age}_zstar{zstar}_hden{hden}_z{zgas}_logU{logU}', '').rsplit('sed')[-1])
        binary = str(id.replace(f'.ascii_age{age}_zstar{zstar}_hden{hden}_z{zgas}_logU{logU}', '').rsplit('_')[-1])
        history = str(id.replace(f'_{binary}.ascii_age{age}_zstar{zstar}_hden{hden}_z{zgas}_logU{logU}', '').rsplit('_')[-1])
        imf = str(id.replace(f'_{history}_{binary}.ascii_age{age}_zstar{zstar}_hden{hden}_z{zgas}_logU{logU}', '').rsplit('imf')[-1])

        BPASS_solar.loc[id, 'logU'] = logU
        BPASS_solar.loc[id, 'zgas'] = zgas
        BPASS_solar.loc[id, 'hden'] = hden
        BPASS_solar.loc[id, 'zstar'] = zstar
        BPASS_solar.loc[id, 'age'] = age
        BPASS_solar.loc[id, 'sed'] = sed
        BPASS_solar.loc[id, 'binary_or_single'] = binary
        BPASS_solar.loc[id, 'history'] = history
        BPASS_solar.loc[id, 'imf'] = imf

    BPASS_solar.to_csv('../data/BPASS_solar.csv')