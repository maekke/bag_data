#!/bin/bash

if [[ -d tmp ]] ; then
	rm -r tmp
fi

out_file="bag_data.csv"

mkdir -p tmp
pushd tmp > /dev/null

wget https://www.bag.admin.ch/dam/bag/de/dokumente/mt/k-und-i/aktuelle-ausbrueche-pandemien/2019-nCoV/covid-19-lagebericht.pdf.download.pdf/COVID-19_Epidemiologische_Lage_Schweiz.pdf

for i in *.pdf ; do
	python ../scripts/parse-data.py "${i}" >> ../${out_file}
done

popd > /dev/null
rm -r tmp
