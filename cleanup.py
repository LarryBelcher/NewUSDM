#!/usr/bin/python

import os, subprocess


cmd = "rm /work/NewUSDM/*.zip"
subprocess.call(cmd,shell=True)

cmd = "rm /work/NewUSDM/Data/*"
subprocess.call(cmd,shell=True)
