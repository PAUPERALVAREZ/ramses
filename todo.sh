#! /usr/bin/bash

NOM=uno

DIR_WRK=.
DIR_LOG=$DIR_WRK/LOG
FICLOG=$DIR_LOG/$(basename $0 .sh).$NOM.LOG
[ -d $DIR_LOG ] || mkdir -p $DIR_LOG

exec > >(tee $FICLOG) 2>&1

hostname
pwd
date

PRM=true
ENT=true
REC=true
EVA=true

DIR_GUI=$DIR_WRK/Gui
GuiEnt=$DIR_GUI/train.gui
GuiDev=$DIR_GUI/devel.gui

LisMod=$DIR_WRK/Lis/vocales.lis

DIR_SEN=$DIR_WRK/Sen
DIR_PRM=$DIR_WRK/prm/$NOM
DIR_MOD=$DIR_WRK/mod/$NOM
DIR_REC=$DIR_WRK/rec/$NOM

ficRes=$DIR_WRK/res/$NOM.res
[ -d $(dirname $ficRes) ] || mkdir -p $(dirname $ficRes)

#Parametriza
dirsen="-s $DIR_SEN"
dirprm="-p $DIR_PRM"
exec="parametriza.py $dirsen $dirprm $GuiEnt $GuiDev"

$PRM && echo $exec && $exec || exit 1

#Entrena
dirprm="-p $DIR_PRM"
dirmar="-a $DIR_SEN"
dirini=
dirmod="-m $DIR_MOD"
exec="entorch.py $dirprm $dirmar $dirini $dirmod $LisMod $GuiEnt"

$ENT && echo $exec && $exec || exit 1

#Reconoce
dirrec="-r $DIR_REC"
dirprm="-p $DIR_PRM"
dirmod="-m $DIR_MOD"
lismod="-l $LisMod"
exec="reconoce.py $dirrec $dirprm $dirmod $lismod $GuiDev"

$REC && echo $exec && $exec || exit 1

#Evalua
dirrec="-r $DIR_REC"
dirmar="-a $DIR_SEN"
exec="evalua.py $dirrec $dirmar $GuiDev"

$EVA && echo $exec && $exec | tee $ficRes || exit 1

#Cierre
date
echo se acabo
