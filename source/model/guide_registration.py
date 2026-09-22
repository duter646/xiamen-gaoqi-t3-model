"""Separate registrations for the guide's separately scaled exploded levels.

Coordinates refer to full resolution cached guide images, not raised icons.
These affine maps are diagram estimates, not surveyed metric calibration.
"""
import numpy as np

CHECKIN_WORLD = np.array([[-104.5,12,1],[147.5,12,1],[147.5,96,1],[-104.5,96,1]])
CHECKIN_PIXELS = np.array([[853,1443],[1590,1010],[1865,1170],[1090,1600]])
CHECKIN = np.linalg.lstsq(CHECKIN_WORLD, CHECKIN_PIXELS, rcond=None)[0].T
ARRIVAL_WORLD = np.array([[-86.5,52,1],[129.5,52,1],[-86.5,61,1]])
ARRIVAL_PIXELS = np.array([[646,1019],[1200,706],[673.5,1035.5]])
ARRIVAL = np.linalg.solve(ARRIVAL_WORLD, ARRIVAL_PIXELS).T
ARRIVAL_CENTRES = {1:[646,1019],2:[711,979],3:[781,944],4:[833,906],5:[894,867],6:[956,831],7:[986,791],8:[1080,769],9:[1142,736],10:[1200,706]}
UPPER=np.array([[2.39,2.35,1175.135],[-1.42,1.4,830.22]])
# Visible orange equipment centres, in the verified 2x crop at (910,630).
SECURITY_DOMESTIC=[[551.1,597.7],[570.1,587.1],[593.9,573.2],[614.2,561.6],[636,548.6],[657.4,536.4],[683.4,521.5],[703.7,509.7],[724.9,497.3],[745.7,485.3],[771.5,470],[792.1,458.3],[815.9,444.6],[836.2,432.5],[857.6,420.3],[879,407.7],[901.4,394.8],[924,381.7],[946.4,368.7],[969,355.3]]
SECURITY_INTERNATIONAL=[[1259.5,130.2],[1279.2,141.6],[1298.6,152.6],[1318.2,164.0],[1337.9,175.4],[1369.3,193.7],[1389.1,205.4],[1408.8,216.6]]
SHOP_TOPS={
 'D-SH01':[(420,631),(476,598),(550,617),(550,631),(536,638),(483,623),(447,651)],
 'D-SH02':[(444,657),(479,639),(528,644),(539,654),(538,666),(500,683),(444,677)],
 'D-SH03':[(378,813),(441,776),(395,747),(395,729),(565,666),(605,666),(630,683),(478,773)],
 'D-CF01':[(305,785),(340,768),(361,771),(360,784),(331,801),(307,797)],
 'I-SH01':[(1141,104),(1180,82),(1246,116),(1244,132),(1199,153),(1159,132)]}


def shop_outline(id):
    # Blue blocks show a 10-14 crop-pixel vertical side; use its base, not roof.
    return unproject(np.asarray(SHOP_TOPS[id])/2+[910,636],UPPER)


def shop_model_outline(id):
    poly=shop_outline(id)
    if id=='D-SH01':
        # Recess the controlled wall around the existing column at (-38.5,42).
        a,b=poly[1],poly[2]
        entry=a+(b-a)*(41.2-a[1])/(b[1]-a[1])
        exit=a+(b-a)*(42.8-a[1])/(b[1]-a[1])
        poly=np.array([poly[0],a,entry,[-39.3,41.2],[-39.3,42.8],exit,*poly[2:]])
    if id=='I-SH01':poly[:,0]=np.maximum(poly[:,0],111.25)
    return poly


def unproject(pixels, matrix):
    return (np.asarray(pixels) - matrix[:,2]) @ np.linalg.inv(matrix[:,:2]).T
