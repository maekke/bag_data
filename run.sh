#!/bin/sh

[[ -d tmp ]] && rm -r tmp

out_file="bag_data.csv"
echo "date;total_number_of_tests;isolated;quarantined;source_file" > ${out_file}

mkdir -p tmp
pushd tmp > /dev/null

wget https://www.bag.admin.ch/dam/bag/de/dokumente/mt/k-und-i/aktuelle-ausbrueche-pandemien/2019-nCoV/bisherige-lageberichte-zip.zip.download.zip/Epidemiologische_Lage_Schweiz.zip
unzip Epidemiologische_Lage_Schweiz.zip
pushd Deutsch > /dev/null

for i in *.pdf ; do
	python ../../parse-data.py "${i}" >> ../../${out_file}
done

popd > /dev/null
popd > /dev/null
rm -r tmp
