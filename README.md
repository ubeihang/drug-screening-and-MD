# drug-screening-and-MD

这里提供了一个使用AutoDock vine进行批量分子对接，并对分子对接结果进行自动化处理的

toolkits used in this study:
1. AutoDock Tools
2. AutoDock Vina
3. Open Babel
4. Raccoon
5. gromacs-2022.2
6. Discovery Studio Visualizer 


## 1. Receptor  and Ligands preparation
1) The complex crystal structure of Mpro (PDB ID:6lu7, download from  http://www.rcsb.org)
2) The drug molecule data set (download from https://www.drugbank.ca/)

## 2.  Receptor and Ligands processing
1) Mpro and inhibitor N3 isolated
Tool: Pymol
processing :  remove waters
<br />
![image](https://user-images.githubusercontent.com/65847000/189270594-7072201f-5107-4cac-8e69-2b0d8fc85e01.png)
<br />
2) setting  grid box
Tool: Autodock tools
<br />
![image](https://user-images.githubusercontent.com/65847000/189270955-52cabb5c-c1a3-444d-90bd-0a25773ca1e3.png)

3) Mpro standardization
(a) gasteiger charges and the addition of polar hydrogen atoms.
(b) format from Protein Data Bank (PDB) format to PDBQT using AutoDock Tools.

4) The drug molecules and inhibitor N3 processing
(a) add polar hydrogen atoms using Open Babel software.
(b) gasteiger charges  using Raccoon.
(c) save as PDBQT format.

## 3.  Molecular docking and Screening

Molecular docking using autodock vina, the specific process is as follows：

1）parameter settings
 

2)Perform molecular docking
> bash ./m_dock.sh

3)Extraction of docking results 
> python ./hb.py
Extract the docked scoring results into one file.

## 4. Dynamic simulation analysis 

Dynamic simulation analysis using  gromacs-2022.2 version.

 4.1 Preparation of protein and ligands 
 1) Receptor: Mpro
 2) Ligands:  N3 and 5 drug molecules（）

 4.2 Construction of protein topology files
 > gmx pdb2gmx -f MPro.pdb -o MPro_processed.gro -water spc -ignh  
 > forcefield choose: Gromos96 53A6
 > generate three files: Mpro_processed.gro, topol.top, posre.itp
  
 4.3 Construction of Ligand Small Molecule Topology
1) Using the PRODRG server（http://davapc1.bioch.dundee.ac.uk/cgi-bin/prodrg/）, the molecular topology files (prodrg .zip) were generated and downloaded.
2) Unzip the file
 > tar -zxvf prodrg.zip   
3) do the following two operations:
(a) DRGGMX.ITP renamed to ligand.itp.
(b) DRGAPH.GRO renamed to ligand.gro.

 4.4  complex construction
 1) Copy 6lu7_processed.gro and name it complex.gro
 2) Copy the coordinate part of the ligand gro file (ligand.gro) after the protein atom coordinates of complex.gro.
 3) Update the number of atoms in the header of the complex.gro file.
 4) Modify the topol.top file and add the include section at the end of the file.

![image](https://user-images.githubusercontent.com/65847000/189318533-2a087090-0355-47a3-8e8f-8624f31c6e57.png)

![image](https://user-images.githubusercontent.com/65847000/189318608-ac186108-57f2-42ca-8396-ecf0937f5030.png)

 4.5 Define the box and add solvent and charged ions
 1)  Define the box
 > gmx editconf -f complex.gro -o newbox.gro -bt cubic -d 1.0
   • -f: input complex structure file
   • -o: output the structure file of the complex, containing information about the new box
   • -bt: define box shape: triclinic (triclinic), cubic (cube), dodecahedron (dodecahedron), octahedron (octahedron)
   • -d: define the distance from the edge of the box to the edge of the molecule (unit: nm), usually not less than 0.85 nm

 2) add solvent
 > gmx solvate -cp newbox.gro -cs spc216.gro -p topol.top -o solv.gro 
   • -cp: input struct file with boxes
   • -cs: specify spc water box
   • -p: output complex topology file with solvent
   • -o: output complex structure file with solvent

 3) add charged ions
 > gmx grompp -f em.mdp -c solv.gro -p topol.top -o ions.tpr -maxwarn 2
Based on the results of the previous command, you can view the amount of charge on the protein to determine the type and amount of ions added in the next command.

 > gmx genion -s ions.tpr -o solv_ions.gro -p topol.top -pname NA -nname CL -np 3
   • -s ions.tpr: input preprocessed tpr file
   • -o solv_ions.gro: output the structure file with counterions added
   • -p topol.top: output topology file
   • -pname NA: added cation type
   • -nname CL: added anion type
   • -np 3: number of sodium ions added 3
   • -nn : number of anions added
   After running the above command, when prompted to Select a continuous group of solvent molecules, select the solvent Group 15 ( SOL).
   
 4.6 Energy minimization
   > gmx grompp -f em_real.mdp -c solv_ions.gro -p topol.top -o em.tpr -maxwarn 1
   Or use GPU acceleration, the command is:
   > gmx mdrun -gpu_id 7 -pin on -nt 10 -v -deffnm em (or use nohup command: > nohup gmx mdrun -gpu_id 7 -pin on -nt 10 -v -deffnm em >em_min.log 2>&1 &)

 4.7 NVT balance
  > gmx make_ndx -f ligand.gro -o index_ligand.ndx
     > 0 & ! a H*
     > q
  > gmx genrestr -f ligand.gro -n index_ligand.ndx -o posre_UNL.itp -fc 1000 1000 1000
    • -f UNL.gro: structure file for input ligand
    • -o posre_UNL.itp: output itp file with positional constraints imposed by ligands
    • -fc 1000 1000 1000: force constant for position limitation (unit: kJ/mol-nm2)
    
  > gmx make_ndx -f em.gro -o index.ndx 
  input: 1 |13 
  input： q (Exit)
  
  In the NVT.mdp file:
  (1) Specify define = -DPOSRES -DPOSRES_LIG
  (2) Set tc_grps = Protein_UNL Water_and_ions
  
  >gmx grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -n index.ndx -o nvt.tpr -maxwarn 2
  
  > gmx mdrun -deffnm nvt -v 
  Or use GPU acceleration, the command is:
  > gmx mdrun -deffnm nvt -pin on -gpu_id 5 -nt 10 -v 
  
 4.8 NVT balance
  In the NTP.mdp file:
  (1) Specify define = -DPOSRES -DPOSRES_LIG
  (2) Set tc_grps = Protein_UNL Water_and_ions
 > gmx grompp -f npt.mdp -c nvt.gro -r nvt.gro -t nvt.cpt -p topol.top -n index.ndx -o npt.tpr -maxwarn 2
 > gmx mdrun -deffnm npt  -v
 Or use GPU acceleration, the command is:
 >nohup gmx mdrun -deffnm npt -pin on -gpu_id 5 -nt 10 -v >mdrun_npt.log 2>&1 &
   
 4.9 Production MD
 > gmx grompp -f md.mdp -c npt.gro -t npt.cpt -p topol.top -n index.ndx -o md_result.tpr -maxwarn 2
 > gmx mdrun -deffnm md_result
Or use GPU acceleration, the command is:
 > gmx mdrun -deffnm md_result -gpu_id 5 -pin on -nt 10 -v 

## 5. Molecular dynamics simulation analysis
 5.1 Recentering and Rewrapping Coordinates
  > gmx trjconv -s md_result.tpr -f md_result.xtc -o md_result_noPBC.xtc -pbc mol -ur compact
   > choose: 0 ("System") 
 5.2 RMSD
 > gmx rms -s md_result.tpr -f md_result_noPBC.xtc -o rmsd_protein.xvg -tu ns
   > choose: 4 (backbone)--- 4(backbone)
 > gmx rms -s md_result.tpr -f md_result_noPBC.xtc -o rmsd_ligand.xvg -tu ns 
   > choose 13（UNL）----- choose 13（UNL）
 5.3 RMSF
 > gmx rmsf -s md_result.tpr -f md_result_noPBC.xtc -o fws-rmsf.xvg -ox fws-avg.pdb -res -oq fws-bafc.pdb 
 5.4 radius of gyration
 > gmx gyrate -s md_result.tpr -f md_result.xtc -o fws-gyrate.xvg
 5.5 hydrogen bond
 > gmx hbond -s md_result.tpr -f md_result.xtc -num fws_hnum.xvg 
 
 Dynamic simulation analysis visualization tool using grance.

 
 



 
 
 
