"""
Interacting plots from SKIRT's simulations data cubes.
This script shows the white image of a galaxy and clicking on a random pixel
plots the corresponding spaxel. At the end, it plots all the clicked spaxels.
Written by Mariana Rivas.
"""

#Importing libraries
import matplotlib.pyplot as plt
import matplotlib
import matplotlib.colors as colors
from matplotlib import colors, cm, pyplot as plt
from astropy.io import fits
import numpy as np
from scipy import ndimage

#Loading file: modify this to your needs
subhalo_id = 476266 #from TNG50-1
path = '/Users/...' #directory of datacube

#Opening FITS file and storing useul data 
hdulist = fits.open(path)
prihdr = hdulist[0].header
muse_data = hdulist[0].data
pix_size_x = prihdr['CDELT1']
pix_size_y = prihdr['CDELT2']
x = prihdr['NAXIS1'] #x dimension
y = prihdr['NAXIS2'] #y dimension
z = prihdr['NAXIS3'] #number of wavelengths
centre_x = int(prihdr['CRPIX1'])
centre_y = int(prihdr['CRPIX2'])
z_i = prihdr['CRVAL3']
z_delt = prihdr['CD3_3']

#Wavelengths in Angstrom
wave = np.zeros(z,dtype=float)
for i in range(z):
    wave[i] = z_i + i*z_delt

#Creating white image
white_image = hdulist[0].data
_wimage = np.zeros((y,x))
for _y in range (0,y):
    for _x in range (0,x):
        _wimage[_y,_x] = sum(white_image[:,_y,_x])
#_wimage = np.transpose(_wimage)

#Defining lists to store (x,y) pixels
_xi = []
_yi = []

#Rotate image as python inverts the axis
rotated_img = ndimage.rotate(_wimage, 90)
_vmin = np.min(_wimage[np.nonzero(_wimage)]) #min nonzero value to not mess up with lognorm
im = plt.imshow(rotated_img,cmap=cm.hsv,origin="lower",rasterized=True,
                interpolation='nearest',
                norm=colors.LogNorm(vmin=_vmin))
fig = plt.gcf()
ax = plt.gca()

#colorbar doesn't work with EventHandler
#fig = plt.colorbar(im,label='Flux [$erg$ $s^{-1}$ $cm^{-2}$ $\mathring A^{-1}$]')
#plt.axis([0, 300, 0, 300])
plt.title('Subhalo '+str(subhalo_id), color='black',fontsize='16')
plt.axis('off')
plt.ylabel('Pixel')
plt.xlabel('Pixel')
plt.legend(handles=[im],loc="upper right")

#Function of interacting plot
class EventHandler:
    def __init__(self):
        fig.canvas.mpl_connect('button_press_event', self.onpress)

    def onpress(self, event):
        if event.inaxes!=ax:
            return
        xi, yi = (int(round(n)) for n in (event.xdata, event.ydata))
        value = im.get_array()[xi,yi]
        color = im.cmap(im.norm(value))
        print (xi,yi,value,color)
        _xi.append(xi)
        _yi.append(yi)

        #Plot of random spaxel
        fig_ = plt.figure()
        #Plot size dimensions
        fig_.set_figheight(5)
        fig_.set_figwidth(10)
        plt.plot(wave, muse_data[:,yi,xi],color='hotpink',label='({},{})'.format(xi, yi))
        plt.title('Subhalo '+str(subhalo_id), color='black',fontsize='16')
        plt.xlim([min(wave),max(wave)])
        plt.xlabel('Wavelength [$\mathring A$]')
        plt.ylabel('F$_\lambda$ [$erg$ $s^{-1}$ $cm^{-2}$ $\mathring A^{-1}$]')
        plt.grid(color='lightgrey', linestyle='-', linewidth=0.75,which='both')
        plt.legend()
        plt.show()

handler = EventHandler()
plt.show()

#Figure with all clicked spaxels
fig__ = plt.figure()
fig__.set_figheight(5)
fig__.set_figwidth(10)
for i in range(len(_xi)):
    plt.plot(wave, muse_data[:,_yi[i],_xi[i]],label='({},{})'.format(_xi[i], _yi[i]))
plt.title('Subhalo '+str(subhalo_id), color='black',fontsize='16')
plt.xlim([min(wave),max(wave)])
plt.xlabel('Wavelength [$\mathring A$]')
plt.ylabel('F$_\lambda$ [$erg$ $s^{-1}$ $cm^{-2}$ $\mathring A^{-1}$]')
plt.grid(which='minor', linewidth=0.6)
plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
plt.show()
