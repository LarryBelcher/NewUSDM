#!/usr/bin/python



import matplotlib as mpl
mpl.use('Agg')
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os, sys, subprocess, glob, calendar
from dbfread import DBF
import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt
import numpy as np


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

def m2fm(mmm):
	if(mmm == 'Jan'): fmm = 'January'
	if(mmm == 'Feb'): fmm = 'February'
	if(mmm == 'Mar'): fmm = 'March'
	if(mmm == 'Apr'): fmm = 'April'
	if(mmm == 'May'): fmm = 'May'
	if(mmm == 'Jun'): fmm = 'June'
	if(mmm == 'Jul'): fmm = 'July'
	if(mmm == 'Aug'): fmm = 'August'
	if(mmm == 'Sep'): fmm = 'September'
	if(mmm == 'Oct'): fmm = 'October'
	if(mmm == 'Nov'): fmm = 'November'
	if(mmm == 'Dec'): fmm = 'December'
	return fmm

#!!!!! Remeber to change the working directory back
#wDir = '/work/CPC_Monthly/')
wDir = '/work/NewUSDM/'
os.chdir(wDir)

fdate = sys.argv[1]   #expects format like: 201301
yyyy = fdate[0:4]		#NOTE a given date will process data for the following month
mm = fdate[4:]

fchk =  glob.glob('./Data/USDM_*.shp')

if(fdate != ' '):
	if(len(fchk) != 1):
		cmd = 'wget https://droughtmonitor.unl.edu/data/shapefiles_m/USDM_'+fdate+'_M.zip'
		subprocess.call(cmd,shell=True)
		cmd = 'unzip -o USDM_'+fdate+'_M.zip -d ./Data/'
		subprocess.call(cmd,shell=True)
	if(fdate != 'current'): dfile =  glob.glob('./Data/USDM_'+fdate+'.shp')
	if(fdate == 'current'): dfile =  glob.glob('./Data/USDM_*.shp')
	dfile = dfile[0].split('.shp')[0]
	fdate = dfile.split('_')[1]
	yyyy = fdate[0:4]
	mm = fdate[4:6]
	dd = fdate[6:8]
	ms = int2str(mm)
	ldd = dd
	if(int(dd) < 10): ldd = dd[1:]
	labdate = ms+' '+ldd+', '+yyyy
	actdate = yyyy+'-'+mm+'-'+dd


imgsize = sys.argv[2]   #(expects small, large, full_res_zips, kml)

figdpi = 72


if(imgsize == 'small'):
	p1 = subprocess.Popen("python "+wDir+"USDMSpecialDriver.py "+dfile+" small", shell=True)
	p1.wait()


if(imgsize == 'large'):
	p1 = subprocess.Popen("python "+wDir+"USDMSpecialDriver.py "+dfile+" large", shell=True)
	p1.wait()


if(imgsize == 'full_res_zips'):
	p1 = subprocess.Popen("python "+wDir+"USDMMap.py "+dfile+" DIY", shell=True)
	p1.wait()

if(imgsize == 'kml'):
	p2 = subprocess.Popen("python "+wDir+"USDMKML.py "+dfile+" "+actdate+' '+labdate, shell=True)
	p2.wait()



if(imgsize == 'full_res_zips'):
	t4x = 3; t4y = 100
	t5x = 3; t5y = 150
	im1 = "./temporary_map.png"
	imgs = Image.open(im1)
	imgw = str(imgs.size[0])
	imgh = str(imgs.size[1])
	img_path = './Images/04-'+imgsize.lower()+'/'
	img_name = 'Drought--Weekly--Drought-Monitor--US--'+yyyy+'-'+mm+'-'+dd+'--fullres.png'
	cmd = 'mv '+im1+' '+img_name
	subprocess.call(cmd,shell=True)
	

	cbar_x = 110
	cbar_y = 85
	figxsize = 8.89
	figysize = 2.44
	figdpi = 72
	fsiz1 = 12
	fsiz2 = 11
	t1x = 0.38; t1y = 0.685
	t2x = 0.2; t2y = 0.6
	t3x = 0.05; t3y = 0.82
	t4x = 0.84; t4y = 0.82
	t5x = 0.16; t5y = 0.420
	cbar_name = './USDMfullresLegend.eps'
	cred_name = 'Drought--Weekly--Drought-Monitor--US--'+yyyy+'-'+mm+'-'+dd+'--credits.eps'

	
	fig = plt.figure(figsize=(6.0,1.0))
	# create an axes instance, leaving room for colorbar at bottom.
	ax1 = fig.add_axes([0.0,0.0,1.0,1.0], facecolor='#F5F5F5')
	ax1.set_frame_on(False)
	ax1.set_xticks([])
	ax1.set_xticklabels([])
	ax1.set_yticks([])
	ax1.set_yticklabels([])

	path = './Fonts/SourceSansPro-Regular.ttf'
	propr = font_manager.FontProperties(fname=path)
	fsiz2 = 12
	t3x = 0.05; t3y = 0.82
	t4x = 0.6; t4y = 0.82

	plt.text(t3x, t3y, 'Weekly Drought Monitor', fontproperties=propr, size=fsiz2, color='#8D8D8D')
	plt.text(t3x, t3y-0.2, 'for '+labdate, fontproperties=propr, size=fsiz2, color='#8D8D8D')
	#plt.text(t3x, t3y-0.4, 'Issued '+idate, fontproperties=propr, size=fsiz2, color='#8D8D8D')

	plt.text(t4x, t4y, 'NDMC', fontproperties=propr, size=fsiz2, color='#8D8D8D')
	plt.text(t4x, t4y-0.2, 'Map by NOAA Climate.gov', fontproperties=propr, size=fsiz2, color='#8D8D8D')

	plt.savefig(cred_name, dpi=figdpi, orientation='portrait', bbox_inches='tight', pad_inches=0.0)


	zipname = 'Drought--Weekly--Drought-Monitor--US--'+yyyy+'-'+mm+'-'+dd+'--fullres.zip'
	
	
	cmd1 = 'zip '+zipname+' '+img_name+' '+cbar_name+' '+cred_name+' noaa_logo.eps '
	subprocess.call(cmd1,shell=True)
	
	
	
'''
	#Push the zip files
	cmd = 'scp -i /home/ubuntu/.ssh/NewEarl.pem -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ./Drought--Weekly--Drought*fullres.zip ubuntu@3.231.241.65:/var/www/Images/NewDSImages/Drought--Weekly--Drought-Monitor--US/04-full_res_zips/'
	subprocess.call(cmd, shell=True)
	
	cmd3 = 'rm '+img_name
	subprocess.call(cmd3,shell=True)
	



##### UNCOMMENT THE CLEANUP COMMANDS HERE
#cmd = 'rm ./Data/*'
#subprocess.call(cmd,shell=True)

cmd = 'rm ./*.zip'
subprocess.call(cmd,shell=True)
cmd = 'rm ./*--credits*'
subprocess.call(cmd,shell=True)
'''
