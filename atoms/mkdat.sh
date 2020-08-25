#! /bin/sh                                                                                                                                                     
#include<math.h>                                                                                                                                               
for i in {370..400};
do
lc=`echo "scale=6; $i / 100" | bc`
ax=`echo "scale=6; $lc" | bc`
by=`echo "scale=6; $lc * sqrt(3) / 2" | bc`
bx=`echo "scale=6; $lc / 2 * -1" | bc`
a=`grep "<Atoms.UnitVectors" $1.dat -A 3 | tail -n 3 | head -n 1 | awk '{print $1}'`
b=`grep "<Atoms.UnitVectors" $1.dat -A 3 | tail -n 2 | head -n 1 | awk '{print $1}'`
c=`grep "<Atoms.UnitVectors" $1.dat -A 2 | tail -n 1 | head -n 1 | awk '{print $1}'`


#mkdir -p ./p-ap1${i}
#mkdir -p ./p-ap1${i}
#mkdir -p ./p-ap1${i}
#mkdir -p ./p-ap1${i}
sed -e "s/$1/$1${i}/g"  -e "s/$a/$ax/g"  -e "s/$b/$bx/g" -e "s/$c/$by/g" $1.dat > $1${i}.dat

#mv p-ap1${i}.dat# /work/s1910010/openmx3.9/work/session6/p-ap1${i}
#mv p-ap1${i}.dat# /work/s1910010/openmx3.9/work/session6/p-ap1${i}
#mv p-ap1${i}.dat# /work/s1910010/openmx3.9/work/session6/p-ap1${i}
#mv p-ap1${i}.dat# /work/s1910010/openmx3.9/work/session6/p-ap1${i}
done
echo OK!