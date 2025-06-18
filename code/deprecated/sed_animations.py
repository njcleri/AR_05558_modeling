import glob
from warnings import simplefilter
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import astropy.units as u
from astropy import constants as const
from matplotlib.gridspec import GridSpec
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter

simplefilter(action="ignore", category=pd.errors.PerformanceWarning)
simplefilter(action="ignore", category=pd.errors.ParserWarning)

def clean_cloudy_con_file(filename):
    '''
    My method for making cloudy continuum files which are run on a single grid
    more user friendly. 
    '''
    df = pd.read_csv(filename, delimiter='\t+', comment='##')
    df = df.rename(columns={'#Cont  nu':'wave'})
    # df['step'] = np.zeros(len(df['wave']))
    # df['step'] = pd.qcut(df.index, int(len(df['wave'])/df['wave'].nunique()))
    # df['step'] = df['step'].cat.rename_categories(np.arange(0,len(df['step'].unique())))
    
    return df

def get_wavelength_from_ev(energy_eV):
    '''
    Takes photon energy in eV and returns corresponding wavelength in Angstroms
    '''
    return (const.h*const.c/(energy_eV*u.eV)).to(u.Angstrom).value

def make_catalog_unique(parent_path):

    catalog = pd.DataFrame()
    for con in glob.glob(f"{parent_path}**_logU-4.0.con"):
        parameters = con.replace(parent_path, '').replace('.con', '')
        # print(parameters)
        try:
            catalog[parameters] = clean_cloudy_con_file(con).copy()['incident']
        except:
            print(con)
            pass

    consdf_unique = catalog
    consdf_unique.columns = consdf_unique.columns.str.split('_hden3').str[0]
    consdf_unique['wave'] = df.wave

    return consdf_unique


def make_animation_ages(ages, df):
    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches(20,10)


    def animate(frame):
        ax.clear()
        age = ages[frame]
        models = df.filter(regex=f'age{np.round(age, decimals=1)}', axis=1)
        for model in models:
            ax.plot(df.wave, np.array(models[model])/models[df.wave == 1.50053e+03][model].iloc[0], c='k', alpha=0.5)
        ax.annotate(f'log age={np.round(age, decimals=1)}', (1475, 3.75),horizontalalignment='right', fontsize=25, color='k')

        ax.fill_betweenx([-0.5,4], 1, get_wavelength_from_ev(54.42), color='skyblue', alpha=0.3, zorder=-3)
        ax.fill_betweenx([-0.5,4], get_wavelength_from_ev(54.93), get_wavelength_from_ev(35.11), color='limegreen', alpha=0.2, zorder=-3)
        ax.fill_betweenx([-0.5,4], get_wavelength_from_ev(34.79), get_wavelength_from_ev(23.33), color='goldenrod', alpha=0.3, zorder=-3)
        ax.fill_betweenx([-0.5,4], get_wavelength_from_ev(29.60), get_wavelength_from_ev(14.53), color='violet', alpha=0.3, zorder=-4)

        ax.annotate('Very High', (np.mean([1, get_wavelength_from_ev(54.42)]), 3.75),horizontalalignment='center', fontsize=25, color='skyblue')
        ax.annotate('High', (np.mean([get_wavelength_from_ev(54.93), get_wavelength_from_ev(35.11)]), 3.5),horizontalalignment='center', fontsize=25, color='limegreen')
        ax.annotate('Intermediate', (np.mean([get_wavelength_from_ev(34.79), get_wavelength_from_ev(23.33)]), 3.75),horizontalalignment='center', fontsize=25, color='goldenrod')
        ax.annotate('Low', (np.mean([get_wavelength_from_ev(29.60),get_wavelength_from_ev(14.53)]), 3.5),horizontalalignment='center', fontsize=25, color='violet')
        ax.set_xlim(0, 1500)
        ax.set_ylim(-0.5,4)
        

    ani = FuncAnimation(fig, animate, frames=len(ages),
                        interval=10, repeat=True)
    ani.save('bpass_ages.gif', dpi=300, writer=PillowWriter(fps=2))


def make_animation_zstars(zstars, df):
    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches(20,10)


    def animate(frame):
        ax.clear()
        z = zstars[frame]
        models = df.filter(regex=f'zstar{z}', axis=1)
        for model in models:
            ax.plot(df.wave, np.array(models[model])/models[df.wave == 1.50053e+03][model].iloc[0], c='k', alpha=0.5)
        ax.annotate(f'Z/Z$_\odot$={z}', (1475, 3.75),horizontalalignment='right', fontsize=25, color='k')

        ax.fill_betweenx([-0.5,4], 1, get_wavelength_from_ev(54.42), color='skyblue', alpha=0.3, zorder=-3)
        ax.fill_betweenx([-0.5,4], get_wavelength_from_ev(54.93), get_wavelength_from_ev(35.11), color='limegreen', alpha=0.2, zorder=-3)
        ax.fill_betweenx([-0.5,4], get_wavelength_from_ev(34.79), get_wavelength_from_ev(23.33), color='goldenrod', alpha=0.3, zorder=-3)
        ax.fill_betweenx([-0.5,4], get_wavelength_from_ev(29.60), get_wavelength_from_ev(14.53), color='violet', alpha=0.3, zorder=-4)

        ax.annotate('Very High', (np.mean([1, get_wavelength_from_ev(54.42)]), 3.75),horizontalalignment='center', fontsize=25, color='skyblue')
        ax.annotate('High', (np.mean([get_wavelength_from_ev(54.93), get_wavelength_from_ev(35.11)]), 3.5),horizontalalignment='center', fontsize=25, color='limegreen')
        ax.annotate('Intermediate', (np.mean([get_wavelength_from_ev(34.79), get_wavelength_from_ev(23.33)]), 3.75),horizontalalignment='center', fontsize=25, color='goldenrod')
        ax.annotate('Low', (np.mean([get_wavelength_from_ev(29.60),get_wavelength_from_ev(14.53)]), 3.5),horizontalalignment='center', fontsize=25, color='violet')
        ax.set_xlim(0, 1500)
        ax.set_ylim(-0.5,4)
        

    ani = FuncAnimation(fig, animate, frames=len(bpass_z_sol),
                        interval=10, repeat=True)
    ani.save('bpass_zstar.gif', dpi=300, writer=PillowWriter(fps=2))


if __name__ == "__main__":
    BPASS_135_300_single_hden3_path = "/Users/njc5787/Research/cloudy_model_library/cloudy_model_library_complete/BPASS/solar_abundances/hden3/BPASSv2.2.1_imf135_300_burst_single_models/"
    path_string = "/Users/njc5787/Research/cloudy_model_library/cloudy_model_library_complete/BPASS/solar_abundances/hden2/BPASSv2.2.1_imf_chab300_burst_binary_models/sedBPASSv2.2.1_imf_chab300_burst_binary.ascii_age6.0_zstar0.1_hden2_z0.1_logU-1.5.con"
    df = clean_cloudy_con_file(path_string)

    ages = np.append(np.arange(6.0, 8.1, 0.1), np.arange(8.5, 11.5, 0.5))
    bpass_z_abs = np.array([0.00001, 0.0001, 0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.008, 0.010, 0.020, 0.040])
    bpass_z_sol = bpass_z_abs * 50

    consdf_unique = make_catalog_unique(BPASS_135_300_single_hden3_path)

    make_animation_ages(ages, consdf_unique)
    make_animation_zstars(bpass_z_sol, consdf_unique)
