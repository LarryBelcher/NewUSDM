#!/usr/bin/python

import sys, os
import subprocess
from dbfread import DBF
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

'''
Notes: This will be the new special monthly MDO driver with calls to the new map makers, 
       which produce CONUS with the AK and HI insets

1) Ensure we are changing to the correct directory just below (i.e., uncomment os.chdir...)
		This program needs to know where it's operating since
		it uses os commands (e.g., "cp" or copy)


'''

os.chdir('/work/NewUSDM')


def int2str(mmi):
    if(mmi == '00'):
        ms = 'No Data'
    if(mmi == '01'):
        ms = 'January'
    if(mmi == '02'):
        ms = 'February'
    if(mmi == '03'):
        ms = 'March'
    if(mmi == '04'):
        ms = 'April'
    if(mmi == '05'):
        ms = 'May'
    if(mmi == '06'):
        ms = 'June'
    if(mmi == '07'):
        ms = 'July'
    if(mmi == '08'):
        ms = 'August'
    if(mmi == '09'):
        ms = 'September'
    if(mmi == '10'):
        ms = 'October'
    if(mmi == '11'):
        ms = 'November'
    if(mmi == '12'):
        ms = 'December'
    return ms


def m2fm(mmm):
    if(mmm == 'Jan'):
        fmm = ['January', '01']
    if(mmm == 'Feb'):
        fmm = ['February', '02']
    if(mmm == 'Mar'):
        fmm = ['March', '03']
    if(mmm == 'Apr'):
        fmm = ['April', '04']
    if(mmm == 'May'):
        fmm = ['May', '05']
    if(mmm == 'Jun'):
        fmm = ['June', '06']
    if(mmm == 'Jul'):
        fmm = ['July', '07']
    if(mmm == 'Aug'):
        fmm = ['August', '08']
    if(mmm == 'Sep'):
        fmm = ['September', '09']
    if(mmm == 'Oct'):
        fmm = ['October', '10']
    if(mmm == 'Nov'):
        fmm = ['November', '11']
    if(mmm == 'Dec'):
        fmm = ['December', '12']
    return fmm


dfile = sys.argv[1]
gdfile = dfile+'.shp'
fdate = dfile.split('_')[1]
yyyy = fdate[0:4]
mm = fdate[4:6]
dd = fdate[6:8]
ms = int2str(mm)
ldd = dd
if(int(dd) < 10): ldd = dd[1:]
labdate = ms+' '+ldd+', '+yyyy
fcastdate = yyyy+'-'+mm+'-'+dd

imgsize = sys.argv[2]  # (expects small or large)



if(imgsize == 'small'):
    p1 = subprocess.Popen(
        "python USDMConusMap.py "+dfile+" small", shell=True)
    p1.wait()
    p2 = subprocess.Popen(
        "python USDMAkMap.py "+dfile+" small", shell=True)
    p2.wait()
    p3 = subprocess.Popen(
        "python  USDMHIMap.py "+dfile+" small", shell=True)
    p3.wait()

    img = Image.new("RGB", size=(620, 585), color=(255, 255, 254))
    imgtextarea = ImageDraw.Draw(img)
    conusimg = Image.open("conus_map-"+imgsize+".png")
    akimg = Image.open("ak-inset-small.png")
    hiimg = Image.open("hi-inset-small.png")
    hiimg = hiimg.resize((110, 147), Image.ANTIALIAS)
    legend = Image.open("USDMLegendSmall.png")
    #smallLegend = legend.resize((322, 147), Image.ANTIALIAS)

    img.paste(conusimg, (0, 0))
    img.paste(akimg, (0, 402))
    img.paste(hiimg, (186, 402))
    img.paste(legend, (298, 402))

    # Add the text at the bottom
    fntpath = './Fonts/SourceSansPro-Regular.ttf'
    fntpathb = './Fonts/SourceSansPro-Bold.ttf'
    fnt1 = ImageFont.truetype(fntpath, 12)

    textproduct = "Weekly Drought Monitor"
    imgtextarea.text((2, 547), textproduct, (141, 141, 141), font=fnt1)

    fordate = "for "+labdate
    imgtextarea.text((2, 558), fordate, (141, 141, 141), font=fnt1)


    textdatasource = "NDMC"
    imgtextarea.text((462, 547), textdatasource, (141, 141, 141), font=fnt1)

    textcred = "Map by NOAA Climate.gov"
    imgtextarea.text((462, 558), textcred, (141, 141, 141), font=fnt1)

    img.save("Drought--Weekly--Drought-Monitor--US--"+fcastdate+"--small.png")
    
    '''
    cmd = 'cp Drought--Monthly--Drought-Outlook--US--'+fcastdate+'--small.png Outlook--Monthly--Drought--US--'+fcastdate+'--small.png'
    subprocess.call(cmd, shell=True)
    cmd = 'scp -i /home/ubuntu/.ssh/NewEarl.pem -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ./Drought--Monthly--Drought-Outlook*small.png ubuntu@3.231.241.65:/var/www/Images/NewDSImages/Drought--Monthly--Drought-Outlook--US/01-small/'
    subprocess.call(cmd, shell=True)
    cmd = 'scp -i /home/ubuntu/.ssh/NewEarl.pem -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ./Outlook--Monthly--Drought*small.png ubuntu@3.231.241.65:/var/www/Images/NewDSImages/Outlook--Monthly--Drought--US/01-small/'
    subprocess.call(cmd, shell=True)

    cmd = 'rm ./Drought--Monthly--Drought-Outlook*small.png'
    subprocess.call(cmd, shell=True)
    cmd = 'rm ./Outlook--Monthly--Drought*small.png'
    subprocess.call(cmd, shell=True)
    '''
    


if(imgsize == 'large'):
    p1 = subprocess.Popen(
        "python USDMConusMap.py "+gdfile+" large", shell=True)
    p1.wait()
    p2 = subprocess.Popen(
        "python USDMAkMap.py "+gdfile+" large", shell=True)
    p2.wait()
    p3 = subprocess.Popen(
        "python USDMHIMap.py "+gdfile+" large", shell=True)
    p3.wait()

    img = Image.new("RGB", size=(1000, 938), color=(255, 255, 254))
    imgtextarea = ImageDraw.Draw(img)
    conusimg = Image.open("conus_map-large.png")
    akimg = Image.open("ak-inset-large.png")
    hiimg = Image.open("hi-inset-large.png")
    hiimg = hiimg.resize((179, 237), Image.ANTIALIAS)
    legend = Image.open("USDMLegendLarge.png")
    #largeLegend = legend.resize((507, 237), Image.ANTIALIAS)

    img.paste(conusimg, (0, 0))
    img.paste(akimg, (0, 642))
    img.paste(hiimg, (299, 642))
    img.paste(legend, (480, 642))

    # Add the text at the bottom
    fntpath = './Fonts/SourceSansPro-Regular.ttf'
    fntpathb = './Fonts/SourceSansPro-Bold.ttf'
    fnt1 = ImageFont.truetype(fntpath, 20)

    textproduct = "Weekly Drought Monitor"
    imgtextarea.text((2, 876), textproduct, (141, 141, 141), font=fnt1)

    fordate = "for "+labdate
    imgtextarea.text((2, 895), fordate, (141, 141, 141), font=fnt1)

    textdatasource = "NDMC"
    imgtextarea.text((735, 876), textdatasource, (141, 141, 141), font=fnt1)

    textcred = "Map by NOAA Climate.gov"
    imgtextarea.text((735, 895), textcred, (141, 141, 141), font=fnt1)

    img.save("Drought--Weekly--Drought-Monitor--US--"+fcastdate+"--large.png")
'''
    cmd = 'cp Drought--Monthly--Drought-Outlook--US--'+fcastdate+'--large.png Outlook--Monthly--Drought--US--'+fcastdate+'--large.png'
    subprocess.call(cmd, shell=True)
    cmd = 'scp -i /home/ubuntu/.ssh/NewEarl.pem -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ./Drought--Monthly--Drought-Outlook*large.png ubuntu@3.231.241.65:/var/www/Images/NewDSImages/Drought--Monthly--Drought-Outlook--US/02-large/'
    subprocess.call(cmd, shell=True)
    cmd = 'scp -i /home/ubuntu/.ssh/NewEarl.pem -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null ./Outlook--Monthly--Drought*large.png ubuntu@3.231.241.65:/var/www/Images/NewDSImages/Outlook--Monthly--Drought--US/02-large/'
    subprocess.call(cmd, shell=True)

    cmd = 'rm ./Drought--Monthly--Drought-Outlook*large.png'
    subprocess.call(cmd, shell=True)
    cmd = 'rm ./Outlook--Monthly--Drought*large.png'
    subprocess.call(cmd, shell=True)
'''