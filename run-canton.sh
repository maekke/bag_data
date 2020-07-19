#!/bin/bash

if [[ -d tmp ]] ; then
	rm -r tmp
fi

cantons=(
	"AG"
	"AI"
	"AR"
	"BE"
	"BL"
	"BS"
	"FR"
	"GE"
	"GL"
	"GR"
	"JU"
	"LU"
	"NE"
	"NW"
	"OW"
	"SG"
	"SH"
	"SO"
	"SZ"
	"TG"
	"TI"
	"UR"
	"VD"
	"VS"
	"ZG"
	"ZH"
	"FL"
)

out_dir="daten_pro_kanton"
mkdir -p ${out_dir}

if [[ ${1} == "--all" ]] ; then
	for canton in ${cantons[*]} ; do
		echo "week,total_number_of_tests,source_file" > ${out_dir}/bag_data_${canton}.csv
	done
fi

mkdir -p tmp

pushd tmp > /dev/null

if [[ ${1} == "--all" ]] ; then
	wget https://www.bag.admin.ch/dam/bag/de/dokumente/mt/k-und-i/aktuelle-ausbrueche-pandemien/2019-nCoV/bisherige-lageberichte-zip.zip.download.zip/Epidemiologische_Lage_Schweiz.zip
	unzip Epidemiologische_Lage_Schweiz.zip
	pushd Deutsch > /dev/null

	for i in *KW*.pdf ; do
		for canton in ${cantons[*]} ; do
			python ../../parse-canton-data.py ${canton} "${i}" >> ../../${out_dir}/bag_data_${canton}.csv
		done
	done

	popd > /dev/null
else
	wget https://www.bag.admin.ch/dam/bag/de/dokumente/mt/k-und-i/aktuelle-ausbrueche-pandemien/2019-nCoV/covid-19-woechentlicher-lagebericht.pdf.download.pdf/BAG_COVID-19_Woechentliche_Lage.pdf
	for canton in ${cantons[*]} ; do
		python ../parse-canton-data.py ${canton} BAG_COVID-19_Woechentliche_Lage.pdf >> ../${out_dir}/bag_data_${canton}.csv
	done
fi

popd > /dev/null
rm -r tmp
