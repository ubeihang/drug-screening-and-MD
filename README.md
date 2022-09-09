# drug-screening-and-MD

这里提供了一个使用AutoDock vine进行批量分子对接，并对分子对接结果进行自动化处理的

本研究所用到的工具包：
1. AutoDock Tools
2. AutoDock Vina
3. Open Babel
4. Raccoon
5. gromacs-2022.2
6. Discovery Studio Visualizer 


# 1. Receptor  and Ligands preparation
1) The complex crystal structure of Mpro (PDB ID:6lu7, download from  http://www.rcsb.org)
2) The drug molecule data set (download from https://www.drugbank.ca/)

#2.  Receptor and Ligands processing
1) Mpro and inhibitor N3 isolated
Tool: Pymol
processing :  remove waters---add hydrogens--- gasteiger charges
![image](https://user-images.githubusercontent.com/65847000/189270594-7072201f-5107-4cac-8e69-2b0d8fc85e01.png)

