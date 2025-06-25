import numpy as np

def ohno_backhaus_2022(logneiiioii):
	'''
	defining the unv087 dividing line from Backhaus et al. 2021.
	Singularity at log(NeIII/OII) = 0.285
	'''    
	return 0.35/(2.8*logneiiioii - 0.8) + 0.64


def plot_ohno_backhaus_2022(ax, label=True):
    xohno = np.linspace(-2,0.285, 1000)
    ax.plot(10**xohno, 10**ohno_backhaus_2022(xohno), c='black', ls='-', lw=3, label='Backhaus et al. 2022' if label else None, zorder=-9)
  

def bpt_kewley_2001(logniiha):
	'''
	Defining the BPT AGN/SF dividing line from Kewley 2001.
	'''    
	return 0.61/(logniiha - 0.47) + 1.19   

def plot_bpt_kewley_2001(ax, label=True):
    x = np.linspace(-2,0.46, 1000)
    ax.plot(10**x, 10**bpt_kewley_2001(x), c='black', ls='-', lw=3, label='Kewley et al. 2001' if label else None, zorder=-9)
    

def bpt_kauffmann_2003(logniiha):
	'''
	Defining the BPT AGN/SF dividing line from Kauffmann 2003.
	'''    
	return 0.61/(logniiha - 0.05) + 1.3    

    
def plot_bpt_kauffmann_2003(ax, label=True, lw=3):
    x = np.linspace(-2,0.04, 1000)
    ax.plot(10**x, 10**bpt_kauffmann_2003(x), c='black', ls='--', lw=lw, label='Kauffmann et al. 2003' if label else None, zorder=-9)

def vo87_trump_2015(logsiiha):
	'''
	Defining the unVO87 AGN/SF dividing line from Trump et al. 2015.
	Singularity at log(SII/Ha) = 0.0917
	'''    
	return 0.48/(1.09*logsiiha - 0.10) + 1.3    


def plot_vo87_trump_2015(ax, label=True):
    x = np.linspace(-2,0.09, 1000)
    ax.plot(10**x, 10**vo87_trump_2015(x), c='black', ls='-', lw=3, label= 'Trump et al. 2015' if label else None, zorder=-9)
