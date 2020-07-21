#!/bin/bash

keep_temp=
if [[ ${1} == "--keep-temp" ]] ; then
	keep_temp="yes"
fi

if [[ -d tmp && -z ${keep_temp} ]] ; then
	rm -r tmp
fi

out_file="bag_data.csv"
echo "date,total_number_of_tests,positivity_rate_percent,isolated,quarantined,source_file" > ${out_file}

mkdir -p tmp
pushd tmp > /dev/null

if [[ ! -f Epidemiologische_Lage_Schweiz.zip ]] ; then
	wget https://www.bag.admin.ch/dam/bag/de/dokumente/mt/k-und-i/aktuelle-ausbrueche-pandemien/2019-nCoV/bisherige-lageberichte-zip.zip.download.zip/Epidemiologische_Lage_Schweiz.zip
fi

if [[ ! -d Deutsch ]] ; then
	unzip Epidemiologische_Lage_Schweiz.zip
fi

pushd Deutsch > /dev/null

for i in *.pdf ; do
	python ../../parse-data.py "${i}" >> ../../${out_file}
done

popd > /dev/null
popd > /dev/null

if [[ -z ${keep_temp} ]] ; then
	rm -r tmp
fi
