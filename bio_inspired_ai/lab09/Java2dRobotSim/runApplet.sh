#!/bin/bash

TMP_APPLET=myApplet.html
TMP_POLICY=myPolicy

if [ $# -ne 4 ];
then
    echo "usage: ./runApplet.sh [PROPERTY_FILE WORK_DIR ROBOTS_FILE RANDOM_SEED]"


    PROPERTY_FILE="config/config2d.txt"
    WORK_DIR="."
    RANDOM_SEED=$RANDOM
    echo "       using default values [$PROPERTY_FILE $WORK_DIR $RANDOM_SEED]"
else
    PROPERTY_FILE=$1
    WORK_DIR=$2
    ROBOTS_FILE=$3
    RANDOM_SEED=$4
fi

# create the HTML and visualize the applet
echo "<HTML>" > $TMP_APPLET
echo "    <HEAD>" >> $TMP_APPLET
echo "        <TITLE>Applet Viewer</TITLE>" >> $TMP_APPLET
echo "    </HEAD>" >> $TMP_APPLET
echo "    <BODY>" >> $TMP_APPLET
echo "        <CENTER><B>Java 2D Robot Simulator</B>" >> $TMP_APPLET
echo "            <BR>" >> $TMP_APPLET
echo "            <APPLET CODE=simulator/SimulatorGui.class ARCHIVE=Java2dRobotSim.jar WIDTH=800 HEIGHT=600>" >> $TMP_APPLET
echo "            <PARAM name=propertyFile value=$PROPERTY_FILE>" >> $TMP_APPLET
echo "            <PARAM name=workDir value=$WORK_DIR>" >> $TMP_APPLET
if [ -n "$ROBOTS_FILE" ];
then
echo "            <PARAM name=robotsFile value=$ROBOTS_FILE>" >> $TMP_APPLET
fi
echo "            <PARAM name=randomSeed value=$RANDOM_SEED>" >> $TMP_APPLET
echo "            </APPLET>" >> $TMP_APPLET
echo "        </CENTER>" >> $TMP_APPLET
echo "    </BODY>" >> $TMP_APPLET
echo "</HTML>" >> $TMP_APPLET

# create the policy file (needed to execute local applets)
echo "grant codeBase \"file://$PWD/-\" { permission java.security.AllPermission; };" > $TMP_POLICY

# run the applet
appletviewer -J-Djava.security.policy=$TMP_POLICY $TMP_APPLET
#/Library/Java/JavaVirtualMachines/jdk1.8.0_192.jdk/Contents/Home/bin/appletviewer -J-Djava.security.policy=$TMP_POLICY $TMP_APPLET

# delete temp files
rm -rf $TMP_APPLET $TMP_POLICY
#rm -rf results.txt
