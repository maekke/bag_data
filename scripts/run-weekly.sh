#!/bin/bash

if [[ -d tmp ]] ; then
	rm -r tmp
fi

if [[ ${1} == "--all" ]] ; then
	echo "week,total_number_of_tests,positivity_rate_percent,source_file" > ${out_dir}/bag_weekly_data.csv
fi

mkdir -p tmp

pushd tmp > /dev/null

if [[ ${1} == "--all" ]] ; then
	wget https://www.bag.admin.ch/dam/bag/de/dokumente/mt/k-und-i/aktuelle-ausbrueche-pandemien/2019-nCoV/bisherige-lageberichte-zip.zip.download.zip/Epidemiologische_Lage_Schweiz.zip
	unzip Epidemiologische_Lage_Schweiz.zip
	pushd Deutsch > /dev/null

	for i in *KW*.pdf ; do
		python ../../scripts/parse_weekly_data.py "${i}" >> ../../bag_weekly_data.csv
	done

	popd > /dev/null
else
	wget https://www.bag.admin.ch/dam/bag/de/dokumente/mt/k-und-i/aktuelle-ausbrueche-pandemien/2019-nCoV/covid-19-woechentlicher-lagebericht.pdf.download.pdf/BAG_COVID-19_Woechentliche_Lage.pdf
	python ../scripts/parse_weekly_data.py BAG_COVID-19_Woechentliche_Lage.pdf >> ../${out_dir}/bag_weekly_data.csv
fi

popd > /dev/null
rm -r tmp
