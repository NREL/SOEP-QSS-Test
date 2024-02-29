#!/usr/bin/env python

# Compare CVode and QSS simulations for a set of Buildings Library models

# Python imports
import datetime, os, subprocess, sys

# Find and change to mdl directory
mdl_dir = os.getcwd()
while os.path.basename( mdl_dir ) != 'mdl': # Move up one directory level
    mdl_dir = os.path.dirname( mdl_dir )
    if os.path.splitdrive( mdl_dir )[1] == os.sep: # At top of drive/mount
        print( 'Error: Not under a "mdl" directory' )
        sys.exit( 1 )
os.chdir( mdl_dir )

# Set up YAML comparison file
date_time = datetime.datetime.now().isoformat( timespec = 'seconds' )
yaml_file_name = 'cmp_CVode_QSS3_Buildings_' + date_time.replace( ':', '.' ).replace( 'T', '_' ) + '.yaml'
subprocess.run( 'cmp_PyFMI_QSS_hdr.py ' + yaml_file_name + ' ' + date_time, shell = True )
cmd = 'cmp_PyFMI_QSS.py --yaml=' + os.path.abspath( yaml_file_name )

# Run Buildings model comparisons # Wait for each to finish since they write to the same stdout and YAML file
with open( 'cmp_CVode_QSS3_Buildings.log', 'w', newline = '\n' ) as log:
#   print( 'ASHRAE2006' ); subprocess.run( 'cd ASHRAE2006 && ' + cmd + ' --dtND=1e-3 --dtInf=0.001 --dtOut=100 --bin --cmp=flo.sou.air.vol.T --cmp=flo.eas.air.vol.T --cmp=flo.nor.air.vol.T --cmp=flo.wes.air.vol.T --cmp=flo.cor.air.vol.T --cmp=TSup.T --cmp=sou.vav.m_flow --cmp=eas.vav.m_flow --cmp=nor.vav.m_flow --cmp=wes.vav.m_flow --cmp=cor.vav.m_flow_turbulent --cmp=conEco.yOA --cmp=dpRetDuc.m_flow --cmp=dpRetDuc.m_flow_nominal --cmp=fanSup.m_flow --cmp=fanSup.m_flow_nominal', stdout = log, stderr = subprocess.STDOUT, shell = True )
    print( 'Case600' ); subprocess.run( 'cd Case600 && ' + cmd + ' --bin=40:0.3 --dtND=1e-4 --dtOut=60 --tStop=604800 --cmp=TRooAir.T', stdout = log, stderr = subprocess.STDOUT, shell = True ) # Some event indicators have large/DBL_MAX values
    print( 'Case600FF' ); subprocess.run( 'cd Case600FF && ' + cmd + ' --bin=50:0.4 --dtND=2e-1 --zFac=2 --dtOut=60 --tStop=604800 --cmp=TRooAir.T', stdout = log, stderr = subprocess.STDOUT, shell = True ) # 7-day run
    print( 'DataCenterContinuousTimeControl' ); subprocess.run( 'cd DataCenterContinuousTimeControl && ' + cmd + ' --bin --dtND=1e-4 --zFac=2 --dtOut=60 --cmp=TAirSup.T --cmp=wseCon.TWetBul --cmp=wseCon.y1 --cmp=chiCon.y --cmp=pumCHW.m_flow', stdout = log, stderr = subprocess.STDOUT, shell = True ) # PyFMI run gives numerical warnings # No directional derivatives # Time range makes small PyFMI steps non-advancing # QSS run has noise causing excessive steps
    print( 'DataCenterDiscreteTimeControl' ); subprocess.run( 'cd DataCenterDiscreteTimeControl && ' + cmd + ' --bin --dtND=1e-4 --zFac=2 --dtOut=60 --cmp=TAirSup.T --cmp=wseCon.TWetBul --cmp=wseCon.y1 --cmp=chiCon.y --cmp=pumCHW.m_flow', stdout = log, stderr = subprocess.STDOUT, shell = True ) # No directional derivatives # Time range makes small PyFMI steps non-advancing # QSS run has noise and is slower than CVode (without tolerance matching)
#   print( 'Guideline36' ); subprocess.run( 'cd Guideline36 && ' + cmd + ' --bin --dtND=1e-4 --zFac=10 --dtOut=100 --cmp=con.TZonCooSet --cmp=con.TZonHeaSet --cmp=con.TZon --cmp=con.yFan --cmp=con.yHeaCoi --cmp=con.yCooCoi', stdout = log, stderr = subprocess.STDOUT, shell = True ) # Event indicator issues: QSS runs very slowly
    print( 'HeatingCoolingHotWater3Clusters' ); subprocess.run( 'cd HeatingCoolingHotWater3Clusters && ' + cmd + ' --bin=5:0.25 --dtND=1e-4 --zFac=10 --dtOut=60 --tStop=604800 --cmp=weaDat.weaBus.TDryBul --cmp=pla.sta_a.T --cmp=pla.sta_b.T --cmp=watTem.y[1] --cmp=pla.m_flow --cmp=EEleHea.y --cmp=EEleCoo.y --cmp=ETheHea.y --cmp=ETheCoo.y --cmp=ETheHotWat.y', stdout = log, stderr = subprocess.STDOUT, shell = True ) # 7-day run # QSS runs are slow
    print( 'HeatingCoolingHotWaterSmall' ); subprocess.run( 'cd HeatingCoolingHotWaterSmall && ' + cmd + ' --bin --dtND=1e-4 --zFac=10 --dtOut=60 --tStop=604800 --cmp=weaDat.weaBus.TDryBul --cmp=m_flow_nominal --cmp=pla.m_flow --cmp=pla.sta_a.T --cmp=pla.sta_b.T --cmp=watTem.y[1]', stdout = log, stderr = subprocess.STDOUT, shell = True ) # QSS runs are slow
#   print( 'OnOffController' ); subprocess.run( 'cd OnOffController && ' + cmd + ' --cmp=TRooK --cmp=vol.T --cmp=conQSS.y', stdout = log, stderr = subprocess.STDOUT, shell = True ) # OCT FMU doesn't run correctly with PyFMI or QSS: Zero crossings are not detected by the FMU
    print( 'SimpleHouse' ); subprocess.run( 'cd SimpleHouse && ' + cmd + ' --bin=10:0.3 --dtND=2e-4 --zMul=1e6 --zFac=1000 --dtOut=60 --tStop=604800 --cmp=zone.T --cmp=heaWat.u --cmp=vavDam.y --cmp=fan.sta_a.T --cmp=fan.sta_b.T', stdout = log, stderr = subprocess.STDOUT, shell = True ) # No directional derivative support causes zero-crossing detection issues
    print( 'SimpleHouseDiscreteTime' ); subprocess.run( 'cd SimpleHouseDiscreteTime && ' + cmd + ' --bin --dtND=5e-3 --dtOut=100 --cmp=zone.T --cmp=heaWat.u --cmp=vavDam.y --cmp=fan.sta_a.T --cmp=fan.sta_b.T', stdout = log, stderr = subprocess.STDOUT, shell = True ) # No directional derivative support: CVode run zero crossings are not stable and QSS event indicators have significant ND noise
#   print( 'TwoFloor_TwoZone' ); subprocess.run( 'cd TwoFloor_TwoZone && ' + cmd + ' --bin --zrFac=10000 --dtND=1e-4 --dtInf=0.001 --cmp=weaDat.weaBus.TDryBul --cmp=weaDat.weaBus.HDirNor --cmp=weaDat.weaBus.HGloHor --cmp=buiZon.theZon[1,1].roo.heaPorAir.T --cmp=buiZon.theZon[2,1].roo.heaPorAir.T --cmp=buiZon.theZon[1,1].heaCooPow --cmp=buiZon.theZon[2,1].heaCooPow', stdout = log, stderr = subprocess.STDOUT, shell = True ) # Derivative sensitivities cause the QSS runs to stall
