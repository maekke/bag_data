#!/bin/bash

for csv in daten_pro_kanton/*.csv ; do
	./scripts/do-cleanup.sh "${csv}"
done

