import subprocess
import shutil
import os
import time
import glob

# Note: I'm well aware that a much easier alternative approach is to simply create a batch file setting path to the desired Qt installation/version (in case of multiple Qt versions) and calling the "windeployqt" from that batch file. This Python version is just an alternative.

dir_deploy = r'D:\partpartA\someProjDeployed'
fpath_deployed_exe = r"dirPart1\x64\Release\someProgram.exe"
fpath_qtDeployTool_exe = r"D:\Qt\5.12.0\msvc2017_64\bin\windeployqt.exe"
fpaths_dlls_others = [r"D:\OpenCV\opencv-4.0.1-vc14_vc15\opencv\build\x64\vc15\bin\opencv_world401.dll", r"D:\OpenCV\opencv-4.0.1-vc14_vc15\opencv\build\x64\vc15\bin\opencv_ffmpeg401_64.dll"]
dir_qt_base = r'D:\Qt\5.12.0\msvc2017_64'

dir_qt_bin = os.path.join(dir_qt_base, 'bin')
dir_qt_iconengines = os.path.join(dir_qt_base, 'plugins', 'iconengines')
dir_qt_imageformats = os.path.join(dir_qt_base, 'plugins', 'imageformats')
dir_qt_platforms = os.path.join(dir_qt_base, 'plugins', 'platforms')

print('Cleaning up the deployed folder')
if os.path.exists(dir_deploy):
	shutil.rmtree(dir_deploy)
os.makedirs(dir_deploy)

print('Calling Qt tool to gather Qt dependencies and put all these dlls in deployed folder')
subprocess.call([fpath_qtDeployTool_exe, '--compiler-runtime', '--no-translations', '--dir', dir_deploy, fpath_deployed_exe], shell=False)

## /////////////////////////////////////////////////////////// ##
## /////////////////////////////////////////////////////////// ##
## /////////////////////////////////////////////////////////// ##

# Note: windeployqt.exe probably internally uses windows PATH environment to find Qt
# dependencies. This means that it will fetch other different versions of Qt dlls
# which will cause the application to not even start or give errors when starting.
# To counter against this, I will use the windeployqt.exe tool just a means of collecting/gathering
# needed names of dll (to know which). Then I will use the actual qt base directory (set by dir_qt_base)
# to get the dlls and replace the ones gather by the windeployqt.exe tool with my own correctly
# found ones.

# Note: the step below is neeeded due to the windeployqt.exe fetching dlls from wrong paths
print('Getting the names of these dlls and taking them from Qt bin directory')
fpaths_dlls_gathered = glob.glob(os.path.join(dir_deploy, 'Qt*.dll'))
for f in fpaths_dlls_gathered:
	dll_name = os.path.basename(f)
	print('Getting {} from dir_qt_bin and replacing the one gathered in the deployed folder'.format(dll_name))
	shutil.copy(os.path.join(dir_qt_bin, dll_name), dir_deploy)

# Note: the step below is neeeded due to the windeployqt.exe fetching dlls from wrong paths
print('Getting the names of these dlls and taking them from Qt bin directory')
fpaths_dlls_gathered = glob.glob(os.path.join(dir_deploy, 'iconengines', '*.dll'))
for f in fpaths_dlls_gathered:
	dll_name = os.path.basename(f)
	print('Getting {} from dir_qt_iconengines, and replacing the one gathered in the deployed folder'.format(dll_name))
	shutil.copy(os.path.join(dir_qt_iconengines, dll_name), os.path.join(dir_deploy, 'iconengines'))

# Note: the step below is neeeded due to the windeployqt.exe fetching dlls from wrong paths
print('Getting the names of these dlls and taking them from Qt bin directory')
fpaths_dlls_gathered = glob.glob(os.path.join(dir_deploy, 'imageformats', '*.dll'))
for f in fpaths_dlls_gathered:
	dll_name = os.path.basename(f)
	print('Getting {} from dir_qt_imageformats and replacing the one gathered in the deployed folder'.format(dll_name))
	shutil.copy(os.path.join(dir_qt_imageformats, dll_name), os.path.join(dir_deploy, 'imageformats'))
	
# Note: the step below is neeeded due to the windeployqt.exe fetching dlls from wrong paths
print('Getting the names of these dlls and taking them from Qt bin directory')
fpaths_dlls_gathered = glob.glob(os.path.join(dir_deploy, 'platforms', '*.dll'))
for f in fpaths_dlls_gathered:
	dll_name = os.path.basename(f)
	print('Getting {} from dir_qt_platforms and replacing the one gathered in the deployed folder'.format(dll_name))
	shutil.copy(os.path.join(dir_qt_platforms, dll_name), os.path.join(dir_deploy, 'platforms'))
		
## /////////////////////////////////////////////////////////// ##
## /////////////////////////////////////////////////////////// ##
## /////////////////////////////////////////////////////////// ##
		
print('Copying other dependencies and putting the deployed folder')
for f in fpaths_dlls_others:
	shutil.copy(f, dir_deploy)

print('Copying the program exe and putting the deployed folder')
shutil.copy(fpath_deployed_exe, dir_deploy)

print('All done')
input()


