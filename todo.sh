#! /usr/bin/bash

NOM=uno

DIR_WRK=.
DIR_LOG=$DIR_WRK/LOG
FIC_LOG=$DIR_LOG/$(basename $0 .sh).$NOM.LOG
[ -d $DIR_LOG ] || mkdir -p $DIR_LOG

exec > >(tee $FIC_LOG) 2>&1

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

lisMod=$DIR_WRK/Lis/vocales.lis

DIR_SEN=$DIR_WRK/Sen
DIR_PRM=$DIR_WRK/prm/$NOM
DIR_MOD=$DIR_WRK/mod/$NOM
DIR_REC=$DIR_WRK/rec/$NOM

ficRes=$DIR_WRK/res/$NOM.res
[ -d $(dirname $ficRes) ] || mkdir -p $(dirname $ficRes)

dirSen="-s $DIR_SEN"
dirPrm="-p $DIR_PRM"
exec="parametriza.py $dirSen $dirPrm $GuiEnt $GuiDev"
$PRM && echo $exec && $exec || exit 1

dirPrm="-p $DIR_PRM"
dirMar="-a $DIR_SEN"
dirIni=""
dirMod="-m $DIR_MOD"
exec="entrena.py $dirPrm $dirMar $dirIni $dirMod $lisMod $GuiEnt"
$ENT && echo $exec && $exec || exit 1

dirRec="-r $DIR_REC"
dirPrm="-p $DIR_PRM"
dirMod="-m $DIR_MOD"
lisMod="-l $lisMod"
exec="reconoce.py $dirRec $dirPrm $dirMod $lisMod $GuiDev"
$REC && echo $exec && $exec || exit 1

dirRec="-r $DIR_REC"
dirMar="-a $DIR_SEN"
exec="evalua.py $dirRec $dirMar $GuiDev"
$EVA && echo $exec && $exec | tee $ficRes || exit 1

date
echo KONETS