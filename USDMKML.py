#!/usr/bin/python

import pyproj, glob, shapefile, sys, os, subprocess
from matplotlib.patches import Polygon
from matplotlib.patches import Path, PathPatch
from pyproj import Proj, transform
from PIL import ImageDraw
from PIL import ImageFont
from PIL import Image
from simplekml import (Kml, OverlayXY, ScreenXY, Units, RotationXY, AltitudeMode, Camera)
import matplotlib.font_manager as font_manager
from mpl_toolkits.basemap import Basemap
from matplotlib.collections import LineCollection
import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
# from dbfread import DBF

mpl.rcParams['savefig.pad_inches'] = 0


def make_kml(llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat,
             figs, colorbar=None, **kw):

    kml = Kml()
    altitude = kw.pop('altitude', 2e7)
    roll = kw.pop('roll', 0)
    tilt = kw.pop('tilt', 0)
    altitudemode = kw.pop('altitudemode', AltitudeMode.relativetoground)
    camera = Camera(latitude=np.mean([urcrnrlat, llcrnrlat]),
                    longitude=np.mean([urcrnrlon, llcrnrlon]),
                    altitude=altitude, roll=roll, tilt=tilt,
                    altitudemode=altitudemode)

    kml.document.camera = camera
    draworder = 0
    for fig in figs:  # NOTE: Overlays are limited to the same bbox.
        draworder += 1
        ground = kml.newgroundoverlay(name='GroundOverlay')
        ground.draworder = draworder
        ground.visibility = kw.pop('visibility', 1)
        ground.name = kw.pop('name', 'overlay')
        ground.color = kw.pop('color', '9effffff')
        ground.latlonbox.rotation = kw.pop('rotation', 0)
        ground.description = kw.pop(
            'description', 'Climate.gov Weekly Drought Monitor; Data: NDMC')
        ground.gxaltitudemode = kw.pop('gxaltitudemode',
                                       'clampToSeaFloor')
        ground.icon.href = fig
        ground.latlonbox.east = llcrnrlon
        ground.latlonbox.south = llcrnrlat
        ground.latlonbox.north = urcrnrlat
        ground.latlonbox.west = urcrnrlon

    if colorbar:  # Options for colorbar are hard-coded (to avoid a big mess).
        screen = kml.newscreenoverlay(name='ScreenOverlay')
        screen.icon.href = colorbar
        screen.overlayxy = OverlayXY(x=0, y=0,
                                     xunits=Units.fraction,
                                     yunits=Units.fraction)
        screen.screenxy = ScreenXY(x=0.015, y=0.075,
                                   xunits=Units.fraction,
                                   yunits=Units.fraction)
        screen.rotationXY = RotationXY(x=0.5, y=0.5,
                                       xunits=Units.fraction,
                                       yunits=Units.fraction)
        screen.size.x = 0
        screen.size.y = 0
        screen.size.xunits = Units.fraction
        screen.size.yunits = Units.fraction
        screen.visibility = 1

    filename = figs[0].split('.png')[0]+'.kmz'
    kmzfile = kw.pop('kmzfile', figs[0])
    kml.savekmz(kmzfile)


def gearth_fig(llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat, pixels=1024):
    """Return a Matplotlib `fig` and `ax` handles for a Google-Earth Image."""
    aspect = np.cos(np.mean([llcrnrlat, urcrnrlat]) * np.pi/180.0)
    xsize = np.ptp([urcrnrlon, llcrnrlon]) * aspect
    ysize = np.ptp([urcrnrlat, llcrnrlat])
    aspect = ysize / xsize

    if aspect > 1.0:
        figsize = (10.0 / aspect, 10.0)
    else:
        figsize = (10.0, 10.0 * aspect)

    if False:
        plt.ioff()  # Make `True` to prevent the KML components from poping-up.

    fig = plt.figure(figsize=figsize, frameon=False, dpi=pixels//10)

    # KML friendly image.  If using basemap try: `fix_aspect=False`.
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(llcrnrlon, urcrnrlon)
    ax.set_ylim(llcrnrlat, urcrnrlat)
    ax.axis('off')
    return fig, ax

def int2str(mmi):
    if(mmi == '00'): ms = 'No Data'
    if(mmi == '01'): ms = 'January'
    if(mmi == '02'): ms = 'February'
    if(mmi == '03'): ms = 'March'
    if(mmi == '04'): ms = 'April'
    if(mmi == '05'): ms = 'May'
    if(mmi == '06'): ms = 'June'
    if(mmi == '07'): ms = 'July'
    if(mmi == '08'): ms = 'August'
    if(mmi == '09'): ms = 'September'
    if(mmi == '10'): ms = 'October'
    if(mmi == '11'): ms = 'November'
    if(mmi == '12'): ms = 'December'
    return ms

def add1(mc):
    if(mc == '01'): mm = '02'
    if(mc == '02'): mm = '03'
    if(mc == '03'): mm = '04'
    if(mc == '04'): mm = '05'
    if(mc == '05'): mm = '06'
    if(mc == '06'): mm = '07'
    if(mc == '07'): mm = '08'
    if(mc == '08'): mm = '09'
    if(mc == '09'): mm = '10'
    if(mc == '10'): mm = '11'
    if(mc == '11'): mm = '12'
    if(mc == '12'): mm = '01'
    return mm


if __name__ == "__main__":

    dfile = sys.argv[1]
    actdate = sys.argv[2]
    labdate = sys.argv[3]
   
    
    path = './Fonts/Trebuchet_MS.ttf'
    propr = font_manager.FontProperties(fname=path)
    path = './Fonts/Trebuchet_MS_Bold.ttf'
    propb = font_manager.FontProperties(fname=path)

    pixels = 1024 * 10

    lllon, lllat, urlon, urlat = [-179.9999, 15.0, -60.0, 75.0]

    fig, ax = gearth_fig(llcrnrlon=lllon,
                     llcrnrlat=lllat,
                     urcrnrlon=urlon,
                     urcrnrlat=urlat,
                     pixels=pixels)
    
    fig1, ax1 = gearth_fig(llcrnrlon=lllon,
                     llcrnrlat=lllat,
                     urcrnrlon=urlon,
                     urcrnrlat=urlat,
                     pixels=pixels)

    kwargs = {'epsg': '4326',
              'resolution': 'i',
              'llcrnrlon': lllon,
              'llcrnrlat': lllat,
              'urcrnrlon': urlon,
              'urcrnrlat': urlat,
              'lon_0': -119.9853516,
              'lat_0': 44.9853516,
              'area_thresh': 15000,
                      'ax': ax,
                      'fix_aspect': False
              }


    #Make the transparent version of the map
    # Set up the Basemap
    m1 = Basemap(**kwargs)
    
    if(dfile != 'ND'):
       # Now read in the Shapes and fill the basemap
        r = shapefile.Reader(dfile)
        shapes = r.shapes()
        records = r.records()
    
    mm = ' '
    if(mm != '00'):
        
        # Fill States w/ white "No Drought"
        shp_info = m1.readshapefile('/work/NewUSDM/Shapefiles/cb_2017_us_state_500k', 'states', drawbounds=True, color=(0.698,0.698,0.698,0.8), zorder=8)
        for nshape, seg in enumerate(m1.states):
            poly = Polygon(seg, facecolor=(0.698,0.698,0.698,0.8), edgecolor=(0.698,0.698,0.698,0.8), linewidth=0.1, zorder=8)
            ax1.add_patch(poly)


        # Now fill the ploy's with appropriate color
        for record, shape in zip(records, shapes):
            #eastings, northings = zip(*shape.points)
            #orgproj = pyproj.Proj(init='esri:102003')
            #wgs84 = pyproj.Proj(init='epsg:4326')
            #lons, lats = pyproj.transform(orgproj, wgs84, eastings, northings)
            
            #data = np.array(m1(lons, lats)).T

            lons, lats = zip(*shape.points)
            data = np.array(m1(lons, lats)).T

            if len(shape.parts) == 1:
                segs = [data, ]
            else:
                segs = []
                for i in range(1, len(shape.parts)):
                    index = shape.parts[i-1]
                    index2 = shape.parts[i]
                    segs.append(data[index:index2])
                segs.append(data[index2:])

               # assuming that the longest segment is the enclosing
                # line and ordering the segments by length:
                lens = np.array([len(s) for s in segs])
                order = lens.argsort()[::-1]
                segs = [segs[i] for i in order]
            
            lines = LineCollection(segs, antialiaseds=(1,), zorder=9)
            # Now obtain the data in a given poly and assign a color to the value

            col0 = (1.0,1.0,0.0,0.8)
            col1 = (0.984, 0.82,0.49,0.8)
            col2 = (1.0,0.667,0.0,0.8)
            col3 = (0.902,0.0,0.0,0.8)
            col4 = (0.451,0.0,0.0,0.8)
            
            dict1={0: col0, 1: col1, 2: col2, 3: col3, 4: col4}
            col = dict1[int(float(record[1]))]
            edgcol = dict1[int(float(record[1]))]

            lines.set_edgecolor(edgcol)
            lines.set_linewidth(1.0)
            lines.set_zorder(9)
            ax1.add_collection(lines)
            
            # producing a path from the line segments:
            segs_lin = [v for s in segs for v in s]
            codes = [[Path.MOVETO]+[Path.LINETO for p in s[1:]] for s in segs]
            codes_lin = [c for s in codes for c in s]
            path = Path(segs_lin, codes_lin)
            # patch = PathPatch(path, facecolor="#abc0d3", lw=0, zorder = 3)
            patch = PathPatch(path, facecolor=col, lw=0, zorder=9)
            ax1.add_patch(patch)
        

    ofile = 'Drought--Weekly--Drought-Monitor--US--'+actdate+'_'
    

    fig1.savefig(ofile+'transparent.png', transparent='True')    
    

    
    # Set up the Basemap
    m = Basemap(**kwargs)

    #Make the opaque version of the map
    if(dfile != 'ND'):
       # Now read in the Shapes and fill the basemap
        r = shapefile.Reader(dfile)
        shapes = r.shapes()
        records = r.records()

    if(mm != '00'):
        # Fill States w/ white "No Drought"
        shp_info = m.readshapefile('/work/CPC_MDO/Shapefiles/cb_2017_us_state_500k', 'states', drawbounds=True, color='#b2b2b2', zorder=8)
        for nshape, seg in enumerate(m.states):
            poly = Polygon(seg, facecolor='#b2b2b2', edgecolor='#b2b2b2', linewidth=0.1, zorder=8)
            ax.add_patch(poly)
        
        # Now fill the ploy's with appropriate color
        for record, shape in zip(records, shapes):
            #eastings, northings = zip(*shape.points)
            #orgproj = pyproj.Proj(init='esri:102003')
            #wgs84 = pyproj.Proj(init='epsg:4326')
            #lons, lats = pyproj.transform(orgproj, wgs84, eastings, northings)
            
            #data = np.array(m(lons, lats)).T
            lons, lats = zip(*shape.points)
            data = np.array(m(lons, lats)).T
            
            if len(shape.parts) == 1:
                segs = [data, ]
            else:
                segs = []
                for i in range(1, len(shape.parts)):
                    index = shape.parts[i-1]
                    index2 = shape.parts[i]
                    segs.append(data[index:index2])
                segs.append(data[index2:])

               # assuming that the longest segment is the enclosing
                # line and ordering the segments by length:
                lens = np.array([len(s) for s in segs])
                order = lens.argsort()[::-1]
                segs = [segs[i] for i in order]
            
            lines = LineCollection(segs, antialiaseds=(1,), zorder=9)
            # Now obtain the data in a given poly and assign a color to the value

            dict1={0: '#ffff00', 1: '#fbd17d', 2: '#ffaa00', 3: '#e60000', 4: '#730000'}

            col = dict1[int(float(record[1]))]
            edgcol = dict1[int(float(record[1]))]

            lines.set_edgecolor(edgcol)
            lines.set_linewidth(1.0)
            lines.set_zorder(9)
            ax.add_collection(lines)
            
            # producing a path from the line segments:
            segs_lin = [v for s in segs for v in s]
            codes = [[Path.MOVETO]+[Path.LINETO for p in s[1:]] for s in segs]
            codes_lin = [c for s in codes for c in s]
            path = Path(segs_lin, codes_lin)
            # patch = PathPatch(path, facecolor="#abc0d3", lw=0, zorder = 3)
            patch = PathPatch(path, facecolor=col, lw=0, zorder=9)
            ax.add_patch(patch)



    fig.savefig(ofile+'opaque.png', transparent='False')  
    
    

    #Now make the kmz's
    ###Create Drought... version
    make_kml(llcrnrlon=lllon, llcrnrlat=lllat, urcrnrlon=urlon, urcrnrlat=urlat, figs=[ofile+'transparent.png'], 
                kmzfile=ofile+'transparent.kmz', name='Weekly Drought Monitor for '+labdate)

    
    cmd = "unzip "+ofile+"transparent.kmz 'doc.kml' > "+ofile+"transparent.kml"
    subprocess.call(cmd, shell=True)
    cmd = 'mv doc.kml '+ofile+'transparent.kml'
    subprocess.call(cmd, shell=True)

    make_kml(llcrnrlon=lllon, llcrnrlat=lllat, urcrnrlon=urlon, urcrnrlat=urlat, figs=[ofile+'opaque.png'], 
                kmzfile=ofile+'opaque.kmz', name='Weekly Drought Monitor for '+labdate)
    
    cmd = "unzip "+ofile+"opaque.kmz 'doc.kml'> "+ofile+"opaque.kml"
    subprocess.call(cmd, shell=True)
    cmd = 'mv doc.kml '+ofile+'opaque.kml'
    subprocess.call(cmd, shell=True)

    cmd = 'mkdir files'
    subprocess.call(cmd, shell=True)
    cmd = 'mv '+ofile+'*.png files/'
    subprocess.call(cmd, shell=True)
    cmd = 'cp USDMKMLLegend.png '+ofile+'legend.png'
    subprocess.call(cmd, shell=True)

    cmd = 'zip '+ofile+'KML-assets.zip '+ofile+'transparent.kml '+ofile+'opaque.kml '+ofile+'legend.png files/Drought*'
    subprocess.call(cmd, shell=True)
    
    cmd = 'scp -i /home/ubuntu/.ssh/NewEarl.pem -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ./Drought*KML-assets.zip ubuntu@3.231.241.65:/var/www/Images/NewDSImages/Drought--Weekly--Drought-Monitor--US/05-kml/'
    #subprocess.call(cmd, shell=True)


    #Cleanup
    #cmd = 'rm *.zip'
    #subprocess.call(cmd, shell=True)
    cmd = 'rm *.kml'
    subprocess.call(cmd, shell=True)
    cmd = 'rm *.kmz'
    subprocess.call(cmd, shell=True)
    cmd = 'rm -rf files/'
    #subprocess.call(cmd, shell=True)
    cmd = 'rm Drought--Weekly--Drought-Monitor--US*.png'
    subprocess.call(cmd, shell=True)