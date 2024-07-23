在.cas文件目录中，新建run.bat文件，内容如下方所示，并根据中文提示修改模型文件名、telemac安装位置和并行参数

```powershell
@echo off
rem 下方输入模型文件名称
set FILENAME=t2d_canal.cas

rem 下方输入telemac安装位置
set HOMETEL=D:\Program\Telemac

set WORKDIR=%~dp0
set EXTERNAL=%HOMETEL%\external
set SYSTELCFG=%HOMETEL%\configs\systel.cfg
set USETELCFG=gnu.static
set PATH=%EXTERNAL%\python-3.10.9\Scripts;%EXTERNAL%\python-3.10.9;%PATH%
set PATH=%EXTERNAL%\mingw64-12.2.0\bin;%PATH%
set PATH=%HOMETEL%\builds\%USETELCFG%\lib;%PATH%
set PATH=%HOMETEL%\scripts\python3;%PATH%
set PYTHONPATH=%HOMETEL%\scripts\python3
set PYTHONPATH=%HOMETEL%\builds\%USETELCFG%\wrap_api\lib;%PYTHONPATH%
set HDF5HOME=%EXTERNAL%\hdf5-1.10.9
set PATH=%HDF5HOME%\bin;%PATH%
set MEDHOME=%EXTERNAL%\med-4.1.1
set PATH=%MEDHOME%\bin;%PATH%
set METISHOME=%EXTERNAL%\metis-5.1.0
set PATH=%METISHOME%\bin;%PATH%
set MPIHOME=%EXTERNAL%\msmpi-10.1.2
set PATH=%MPIHOME%\bin;%PATH%
set OPENBLASHOME=%EXTERNAL%\openblas-0.3.21
set SCALAPACKHOME=%EXTERNAL%\scalapack-2.1.0
set MUMPSHOME=%EXTERNAL%\mumps-5.2.1
set AEDHOME=%EXTERNAL%\libaed2-1.2.0
set GOTMHOME=%EXTERNAL%\gotm-2019-06-14-opentelemac
set PATH=%GOTMHOME%\bin;%PATH%

cd %WORKDIR%
rem 这里输入需要多少个CPU并行
python.exe %HOMETEL%\scripts\python3\telemac2d.py %FILENAME% --ncsize=4 -s
```
