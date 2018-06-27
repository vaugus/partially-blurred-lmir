#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""stats file."""

import sys
import numpy as np

case = str(sys.argv[1]).rstrip()

rmse_opt = []
rmse_rest = []
psnr_opt = []
psnr_rest = []
time = []

for i in range(1,11):
    f = open('../output/test_cases/' + case + '/' + str(i) + '.out')
    rmse_opt.append(float(f.readline().rstrip()))
    rmse_rest.append(float(f.readline().rstrip()))
    psnr_opt.append(float(f.readline().rstrip()))
    psnr_rest.append(float(f.readline().rstrip()))
    time.append(float(f.readline().rstrip()))


rmse_opt = np.array(rmse_opt)
rmse_rest = np.array(rmse_rest)
psnr_opt = np.array(psnr_opt)
psnr_rest = np.array(psnr_rest)
time = np.array(time)

print ('= MEAN ====================\n')
print ('RMSE Optimal - Degraded: ' + str(rmse_opt.mean()))
print ('RMSE Optimal - Restored: ' + str(rmse_rest.mean()))
print ('PSNR Optimal - Degraded: ' + str(psnr_opt.mean()))
print ('PSNR Optimal - Restored: ' + str(psnr_rest.mean()))
print ('Time: ' + str(time.mean()) + '\n')

print ('= STD =====================\n')
print ('RMSE Optimal - Degraded: ' + str(rmse_opt.std()))
print ('RMSE Optimal - Restored: ' + str(rmse_rest.std()))
print ('PSNR Optimal - Degraded: ' + str(psnr_opt.std()))
print ('PSNR Optimal - Restored: ' + str(psnr_rest.std()))
print ('Time: ' + str(time.std()) + '\n')

print ('= VAR =====================\n')
print ('RMSE Optimal - Degraded: ' + str(rmse_opt.var()))
print ('RMSE Optimal - Restored: ' + str(rmse_rest.var()))
print ('PSNR Optimal - Degraded: ' + str(psnr_opt.var()))
print ('PSNR Optimal - Restored: ' + str(psnr_rest.var()))
print ('Time: ' + str(time.var()))
