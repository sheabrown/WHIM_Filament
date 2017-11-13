import pyfits
import numpy as np
import healpy as hp
import sys
import matplotlib.pyplot as plt

f = open('wiseScosPhotoz160708.csv', 'r')
header1 = f.readline()
print header1
l = []
b = []
z = []
RadPerDeg = np.pi / 180.0 #Radians per degree multiplier factor

for row in f:
	t = row.split(',')
	l.append(float(t[9]))
	b.append(float(t[10]))
	z.append(float(t[16]))	

l=np.array(l)
b=np.array(b)
z=np.array(z)

def ang2pix_radec(nside,ra, dec):
        phi = RadPerDeg * ra
        theta = (np.pi / 2.0 )- (RadPerDeg * dec)
	theta_gal, phi_gal = hp.Rotator(coord=['C','G'])(theta, phi)
        ipix = hp.ang2pix(nside, theta_gal, phi_gal,nest=False)
        return ipix

def ang2pix_count(nside,l,b):
    map=np.zeros(hp.nside2npix(nside))
    
    for x in range(0,len(l),1):
	sys.stdout.write("\rProcessing epoch %i" % x)
	sys.stdout.flush()    
	tpix=hp.ang2pix(nside,l[x],b[x],nest=False,lonlat=True)
	map[tpix]=map[tpix]+1
    return map

index=where(z<0.10)
l=l[index]
b=b[index]
z=z[index]
index=where(z>0.08)
l=l[index]
b=b[index]
z=z[index] 
print len(l)

map=ang2pix_count(256,l,b)
hp.fitsfunc.write_map('wise_z0.08-0.10.fits', map)
#hp.mollview(map)
#plt.hist(z, bins=30)
#plt.show()
