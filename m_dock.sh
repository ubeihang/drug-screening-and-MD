#!/bin/bash
for f in dbank*pdbqt;do
echo Processing Ligand $(basename $f .pdbqt)
mkdir -p $(basename $f .pdbqt)
vina --config conf.txt --ligand $f --out $(basename $f .pdbqt)/out.pdbqt --log $(basename $f .pdbqt)/log.txt
done

