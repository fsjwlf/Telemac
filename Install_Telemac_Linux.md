本文参考：http://wiki.opentelemac.org/doku.php?id=installation_on_linux

# 1. 安装环境
## 1.1 安装依赖
```bash
sudo apt install gfortran-10 cmake
sudo apt install libopenmpi-dev openmpi-bin
sudo apt install python3-numpy python3-scipy python3-matplotlib
sudo apt install libhdf5-dev hdf5-tools
```

## 1.2 安装metis
下载 metis，https://github.com/fsjwlf/Telemac/raw/main/metis-5.1.0.tar.gz，并复制到当前文件夹
```bash
tar -xzvf metis-5.1.0.tar.gz
mv metis-5.1.0 metis
cd metis
make config prefix=~/metis/
make install
```
上述为精简安装，如需使用WAQTEL、Telemac3D、ARTEMIS module、MED format，请参考 http://wiki.opentelemac.org/doku.php?id=installation_on_linux 安装其他工具

## 1.3 下载telemac
```bash
wget https://gitlab.pam-retd.fr/otm/telemac-mascaret/-/archive/main/telemac-mascaret-main.tar.gz
tar -xzvf telemac-mascaret-main.tar.gz
mv telemac-mascaret-main telemac
```

# 2. 配置Telemac
打开  telemac/configs  文件夹  
新建 pysource.gfortranHPC.sh 文件，内容如下所示：  
（注意，这里一定要用Linux系统的 LF 作为换行符。（如果用windows下的CRLF作为换行符，在后续执行config.py时，会提示找不到 configs/systel.cfg 文件，因为CRLF是两个字符，而LF是一个字符）
```
export HOMETEL=$HOME/telemac
export PATH=$HOMETEL/scripts/python3:.:$PATH
export SYSTELCFG=$HOMETEL/configs/systel.cfg
export USETELCFG=gfortranHPC
export SOURCEFILE=$HOMETEL/configs/pysource.gfortranHPC.sh
export PYTHONUNBUFFERED='true'
export PYTHONPATH=$HOMETEL/scripts/python3:$PYTHONPATH
export LD_LIBRARY_PATH=$HOMETEL/builds/$USETELCFG/wrap_api/lib:$LD_LIBRARY_PATH
export PYTHONPATH=$HOMETEL/builds/$USETELCFG/wrap_api/lib:$PYTHONPATH
export MEDHOME=$HOME/metis
```

新建 systel.cfg 文件
```
[Configurations]
configs: gfortran gfortranHPC
[general]
language: 2
modules: system
options: api
f2py_name: f2py3
pyd_fcompiler: gnu95
mods_all:   -I <config>
sfx_zip:    .zip
sfx_lib:    .a
sfx_obj:    .o
sfx_mod:    .mod
sfx_exe:
val_root:   <root>/examples
val_rank:   all
cmd_obj_c: gcc -fPIC -c <srcName> -o <objName>

[gfortran]
brief: Gfortran compiler
cmd_obj:    gfortran -c -cpp -fPIC -O2 -fconvert=big-endian -frecord-marker=4 -DHAVE_VTK <mods> <incs> <f95name>
cmd_lib:    ar cru <libname> <objs>
cmd_exe:    gfortran -fPIC -fconvert=big-endian -frecord-marker=4 -lpthread -lm -o <exename> <objs> <libs>

[gfortranHPC]
brief: GFortran compiler using Open MPI
mpi_cmdexec: mpirun -machinefile MPI_HOSTFILE -np <ncsize> <exename>
cmd_obj:    mpif90 -c -cpp -fPIC -O2 -fconvert=big-endian -frecord-marker=4 -DHAVE_MPI -DHAVE_VTK <mods> <incs> <f95name>
cmd_lib:    ar cru <libname> <objs>
cmd_exe:    mpif90 -fPIC -fconvert=big-endian -frecord-marker=4 -lpthread -lm -o <exename> <objs> <libs>
libs_all: -L$HOME/metis/lib -lmetis
```


# 3. 编译
```bash
cd $HOME/telemac/configs
source pysource.gfortranHPC.sh
cd $HOME/telemac/scripts/python3
config.py
compile_telemac.py
```

# 4. 运行
```bash
cd $HOME/telemac/configs
source pysource.gfortranHPC.sh
cd $HOME/telemac/examples/telemac2d/canal
telemac2d.py t2d_canal.cas --ncsize=4
```

后台运行
```bash
nohup telemac2d.py run.cas --ncsize=10 >run.log &
```
