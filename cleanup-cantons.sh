#!/bin/bash

for csv in daten_pro_kanton/*.csv ; do
	./do-cleanup.sh "${csv}"
done

