import glob
import pandas as pd

AGN_solar_path = "/Users/njc5787/Research/cloudy_model_library/cloudy_model_library_complete/AGN/solar_abundances/"

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
    for ilin in glob.glob(f"{AGN_solar_path}**/**.ilin"):
        parameters = ilin.replace(AGN_solar_path, '').replace('.ilin', '')
        try:
            catalog[parameters] = clean_cloudy_line_file(ilin, name=parameters).copy()
        except:
            print(ilin)
            pass

    AGN_solar = catalog.T
    AGN_solar['logU'] = None
    AGN_solar['zgas'] = None
    AGN_solar['hden'] = None
    AGN_solar['mbh'] = None

    for id, row in AGN_solar.iterrows():
        logU = float(id.rsplit('logU')[-1])
        zgas = float(id.replace(f'_logU{logU}', '').rsplit('z')[-1])
        hden = int(id.replace(f'_z{zgas}_logU{logU}', '').rsplit('hden')[-1])
        mbh = int(id.replace(f'_hden{hden}_z{zgas}_logU{logU}', '').rsplit('mbh')[-1])

        AGN_solar.loc[id, 'logU'] = logU
        AGN_solar.loc[id, 'zgas'] = zgas
        AGN_solar.loc[id, 'hden'] = hden
        AGN_solar.loc[id, 'mbh'] = mbh

    AGN_solar.to_csv('../data/AGN_solar.csv')