#!/usr/bin/env python
import os
#import time
import sys
#import subprocess
import numpy as np
from partricol import tripar
from partricol import cypar
import astropy
from astropy.io import ascii
from astropy.table import Table, Column

def run_trilegal(par_file, tri_bin='./main', out_options='-fits -iso iso_str'):

   #parsing the parameter file
   #if (len(sys.argv) < 2):
   #   print 'trilegal.py usage: trilegal par_file tri_bin [-fits] [-iso iso_str]' #tri_bin: trilegal executable, must be after par_file if exists
   #   sys.exit(2)

   trilegal_object=tripar.def_par_trilegal()
   cmd_object=trilegal_object.cmd
   tri_object=trilegal_object.tri

   str_uniq=par_file.replace('.par','')
   mod_par=cypar.read(par_file)
   par_name=mod_par.par_name
   par_val=mod_par.par_val


   #trilegal executable
   if (not os.path.isfile(tri_bin)):
      old_tri_bin=tri_bin
      tri_bin=os.path.join(os.environ.get('TRILEGAL_DIR'),'code/main')
      old_tri_bin=old_tri_bin+' '+tri_bin
      if (not os.path.isfile(tri_bin)):
         tri_bin=os.path.join(os.environ.get('TRILEGALDIR'),'code/main')
         old_tri_bin=old_tri_bin+' '+tri_bin
         if (not os.path.isfile(tri_bin)):
            print('not exist: '+old_tri_bin)

   print(tri_bin)
   fits_output=''
   options0=''

   if ('-fits' in out_options):
      print('fits output')
      fits_output='.fits'
   if ('-iso' in out_options):
      print('isochrone output:')
      fits_output='.iso.output' #for the moment no fits output support for isochrones
      options0='-i '+out_options[out_options.rfind("-iso"):]

   #time=str(time.time())



   #sfr
   sfr_object={}
   for key_name in ['age', 'age_width', 'age_bin', 'age_l', 'age_u']:
      i1=-1
      for par_id in par_name:
         i1=i1+1
         if (par_id == key_name):
            sfr_object[key_name]=float(par_val[i1])

   i1=-1
   for par_id in par_name:
      i1=i1+1
      if (par_id == 'age_res'):
         age_res=par_val[i1]


   i1=-1
   for par_id in par_name:
      i1=i1+1
      if (par_id == 'ZZ'):
         Zs=(par_val[i1]).split()

   #print "Zs", Zs
   for s1 in Zs:
      sfr_object['ZZ']=float(s1)


      ages=np.arange(sfr_object['age_l'],sfr_object['age_u']+sfr_object['age_bin'],sfr_object['age_bin'])
      sfr=ages*0
      ZZ=ages*0+sfr_object['ZZ']

      id=np.where((ages >= sfr_object['age']-sfr_object['age_width']) & (ages <= sfr_object['age']+sfr_object['age_width']))
      sfr[id]=1

      sfh = Table([10.**ages, sfr, ZZ])

   #   file_sfr='/tmp/trilegal/trilegal_sfr_Z'+s1+'.dat_'+time
   #   while True:
   #      timex=str(time.time())
   #      file_sfr='/tmp/trilegal/trilegal_sfr_Z'+s1+'.dat_'+timex
      file_sfr=str_uniq+'_tri_sfr.dat'
   #   print "sfr file:", file_sfr
   #   if (not os.path.isfile(file_sfr)): break

      tri_object.file_sfr=file_sfr
   #write_trilegal_sfr_file()

      ascii.write(sfh, file_sfr,names=['age','sfr','z'],format='no_header')
   #   tmpstr="'1 i 6.6:10.3:"+age_res+" -5.02:-1.00:0.02'"
      tmpstr="'1 i 9.0:10.0:"+age_res+" -2.40:-2.10:0.02'"
      os.system("sed -i "+tmpstr+" "+file_sfr)  
   #the resolution in age should be larger than 0.002


   #write_cmd_input_files()
   #   cmdinput_file='/tmp/trilegal/cmd_input_Z'+s1+'.dat_'+timex
      cmdinput_file=str_uniq+'_cmd_input.dat'
   #write_trilegal_input_files()
   #   triinput_file='/tmp/trilegal/tri_input_Z'+s1+'.dat_'+timex
      triinput_file=str_uniq+'_tri_input.dat'
   #output log file
   #   log_file='/tmp/trilegal/log_Z'+s1+'.dat_'+timex
      log_file=str_uniq+'_log.dat'
   #trilegal_object=def_par_trilegal()
   #cmd_object=trilegal_object.cmd
   #tri_object=trilegal_object.tri

   ##modify cmd parameters
      for key_name in cmd_object.__dict__.keys():
         i1=-1
         for par_id in par_name:
            i1=i1+1
            if (par_id == key_name):
   #         cmd_object.key_namea=par_val[i1]
               setattr(cmd_object,key_name, par_val[i1])
   ##modify tri parameters
      for key_name in tri_object.__dict__.keys():
         i1=-1
         for par_id in par_name:
            i1=i1+1
            if (par_id == key_name):
   #         tri_object.key_nameb=par_val[i1]
               setattr(tri_object,key_name, par_val[i1])
   ####write out the modified cmd and tri input paramter files
      tripar.write_par_trilegal(cmd_object, cmdinput_file, tri_object, triinput_file)








   #trilegal command line
      options=options0+' -s -a -l -f'
                    #-i: print isochrone(s) and exit
                    #-f: cmdinputfile followed
                    #-t: ?
                    #-k: output kinematics
                    #-a: output AGB data
                    #-l: output labels (TP-AGB=8, E-AGB, ...)
                    #-s: output star variables
                    #-b: print full info on binaries
                    #output file name with ".fits": output in fits format
   # output isochrone with fits will result in segmentation faultcommon/colori.c
   #output simulation with fits lacks some properties as output with ascii format

   #   output_file=par_file+'_output_Z'+s1 #_'+time
      if ((len(Zs) == 1) and ('_Z' in par_file)):
   #      output_file=par_file.replace('.par','.output')
         output_file=par_file.replace('.par','') #changed to trilegal fits output
      else:
   #      output_file=par_file.replace('.par','_Z'+s1+'.output')
         output_file=par_file.replace('.par','_Z'+s1+'')
   #mass, age and other parameters can be added to the file name 



   #   command="/bin/bash -i -c '"+'$trilegal '+options+' '+cmdinput_file+' '+triinput_file+' '+output_file+"'&"
   #   command=tri_bin+' '+options+' '+cmdinput_file+' '+triinput_file+' '+output_file+fits_output + '>' + log_file #+ '&'
      command='nice -20 '+tri_bin+' '+options+' '+cmdinput_file+' '+triinput_file+' '+output_file +fits_output + '>' + log_file #+ '&'
      print(command)
      os.system(command)
   #   subprocess.Popen(command, shell=False)
   #   os.system('fg')
   #   os.system('pid=$!')
   #   pid=os.system('echo $pid')
   #   os.system('fg %'+pid)

   #time.sleep(10)
   #for s1 in Zs:
   #   os.system('fg')


   return
