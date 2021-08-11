from defs import *
from values import *
import flux
import electrochemical 
import glucose
import NHE3
import ATPase
import NKCC
import KCC
import NCC
import ENaC
import Pendrin
import AE1
import NHE1

solute = ['Na','K','Cl','HCO3','H2CO3','CO2','HPO4','H2PO4','urea','NH3','NH4','H','HCO2','H2CO2','glu']
compart = ['Lumen','Cell','ICA','ICB','LIS','Bath']
cw=Vref*60e6

def output_segment_results(cell,sup_or_jux,Scaletorq,file_to_save,N):

    #========================================================
    # output concentrations in Lumen and Cell
    #========================================================
    for i in range(NS):
        file=open('./'+file_to_save+'/'+cell[0].sex+'_'+cell[0].humOrrat+'_'+cell[0].segment+'_con_of_'+solute[i]+'_in_Lumen_'+sup_or_jux+'.txt','w')
        for j in range(N):
            file.write(str(cell[j].conc[i,0])+'\n')
        file.close()
    for i in range(NS):
        file=open('./'+file_to_save+'/'+cell[0].sex+'_'+cell[0].humOrrat+'_'+cell[0].segment+'_con_of_'+solute[i]+'_in_Cell_'+sup_or_jux+'.txt','w')
        for j in range(N):
            file.write(str(cell[j].conc[i,1])+'\n')
        file.close()
    for i in range(NS):
        file=open('./'+file_to_save+'/'+cell[0].sex+'_'+cell[0].humOrrat+'_'+cell[0].segment+'_con_of_'+solute[i]+'_in_Bath_'+sup_or_jux+'.txt','w')
        for j in range(N):
            file.write(str(cell[j].conc[i,5])+'\n')
        file.close()

    #========================================================
    # output water volume in Lumen and Cell
    #========================================================
    file=open('./'+file_to_save+'/'+cell[0].sex+'_'+cell[0].humOrrat+'_'+cell[0].segment+'_water_volume_in_Lumen_'+sup_or_jux+'.txt','w')
    for j in range(N):
        file.write(str(cell[j].vol[0]*cw)+'\n')
    file.close()
    file=open('./'+file_to_save+'/'+cell[0].sex+'_'+cell[0].humOrrat+'_'+cell[0].segment+'_water_volume_in_Cell_'+sup_or_jux+'.txt','w')
    for j in range(N):
        file.write(str(cell[j].vol[1]*cw)+'\n')
    file.close()
    
    #========================================================
    # output solute flows in Lumen and Cell
    #========================================================
    for i in range(NS):
        file=open('./'+file_to_save+'/'+cell[0].sex+'_'+cell[0].humOrrat+'_'+cell[0].segment+'_flow_of_'+solute[i]+'_in_Lumen_'+sup_or_jux+'.txt','w')
        for j in range(N):
            file.write(str(cell[j].conc[i,0]*cell[j].vol[0]*cw)+'\n')
        file.close()
    for i in range(NS):
        file=open('./'+file_to_save+'/'+cell[0].sex+'_'+cell[0].humOrrat+'_'+cell[0].segment+'_flow_of_'+solute[i]+'_in_Cell_'+sup_or_jux+'.txt','w')
        for j in range(N):
            file.write(str(cell[j].conc[i,1]*cell[j].vol[1]*cw)+'\n')
        file.close()
        
    #========================================================
    # output osmolality in Lumen, Cell, LIS, Bath
    #========================================================
    file_lumen = open('./'+file_to_save+'/'+cell[0].sex+'_'+cell[0].humOrrat+'_'+cell[0].segment+'_osmolality_in_Lumen_'+sup_or_jux+'.txt','w')
    file_cell = open('./'+file_to_save+'/'+cell[0].sex+'_'+cell[0].humOrrat+'_'+cell[0].segment+'_osmolality_in_Cell_'+sup_or_jux+'.txt','w')
    file_lis = open('./'+file_to_save+'/'+cell[0].sex+'_'+cell[0].humOrrat+'_'+cell[0].segment+'_osmolality_in_LIS_'+sup_or_jux+'.txt','w')
    file_bath = open('./'+file_to_save+'/'+cell[0].sex+'_'+cell[0].humOrrat+'_'+cell[0].segment+'_osmolality_in_Bath_'+sup_or_jux+'.txt','w')
    for j in range(N):
        osm_l = 0
        osm_c = 0
        osm_lis = 0
        osm_b = 0
        for i in range(NS):
            osm_l = osm_l +cell[j].conc[i,0]
            osm_c = osm_c +cell[j].conc[i,1]
            osm_lis = osm_lis+cell[j].conc[i,4]
            osm_b = osm_b +cell[j].conc[i,5]

        file_lumen.write(str(osm_l)+'\n')
        file_cell.write(str(osm_c)+'\n')
        file_lis.write(str(osm_lis)+'\n')
        file_bath.write(str(osm_b)+'\n')
    file_lumen.close()
    file_cell.close()
    file_lis.close()
    file_bath.close()
    
    #========================================================
    # output luminal pressure
    #========================================================
    file=open('./'+file_to_save+'/'+cell[0].sex+'_'+cell[0].humOrrat+'_'+cell[0].segment+'_pressure_in_Lumen_'+sup_or_jux+'.txt','w')
    for j in range(N):
        file.write(str(cell[j].pres[0])+'\n')
    file.close()

    #========================================================
    # output transcellular and paralcelluar Na fluxes 
    #========================================================
    for j in range(N):

        cell[j].area[4][5] = 0.02*max(cell[j].vol[4]/cell[j].volref[4],1.0)
        cell[j].area[5][4] = cell[j].area[4][5]

        jvol,jsol = flux.compute_fluxes(cell[j],j)            

        file_Na_apical = open('./'+file_to_save+'/'+cell[j].sex+'_'+cell[0].humOrrat+'_'+cell[j].segment+'_apical_Na_'+sup_or_jux+'.txt','a')
        file_Na_apical.write(str(jsol[0,0,1])+'\n')

        file_Na_para = open('./'+file_to_save+'/'+cell[j].sex+'_'+cell[0].humOrrat+'_'+cell[j].segment+'_paracellular_Na_'+sup_or_jux+'.txt','a')
        file_Na_para.write(str(jsol[0,0,4])+'\n')

    #========================================================
    # output transporter-mediated fluxes 
    #========================================================

        if cell[j].segment!='SDL' and cell[j].segment!='LDL' and cell[j].segment!='LAL':
            for i in range(len(cell[j].trans)):
                transporter_type = cell[j].trans[i].type
                memb_id = cell[j].trans[i].membrane_id
                
                if transporter_type == 'SGLT1':
                    solute_id,fluxs = glucose.sglt1(cell[j],cell[j].ep,memb_id,cell[j].trans[i].act,cell[j].area)
                    for k in range(len(solute_id)):
                        file = open('./'+file_to_save+'/'+cell[j].sex+'_'+cell[0].humOrrat+'_'+cell[j].segment+'_'+transporter_type+'_'+solute[solute_id[k]]+'_'+sup_or_jux+'.txt','a')
                        file.write(str(fluxs[k]*Scaletorq[j])+'\n')
                elif transporter_type == 'SGLT2':
                    solute_id,fluxs = glucose.sglt2(cell[j],cell[j].ep,memb_id,cell[j].trans[i].act,cell[j].area)
                    for k in range(len(solute_id)):
                        file = open('./'+file_to_save+'/'+cell[j].sex+'_'+cell[0].humOrrat+'_'+cell[j].segment+'_'+transporter_type+'_'+solute[solute_id[k]]+'_'+sup_or_jux+'.txt','a')
                        file.write(str(fluxs[k]*Scaletorq[j])+'\n')
                elif transporter_type == 'GLUT1':
                    solute_id,fluxs=glucose.glut1(cell[j],cell[j].ep,memb_id,cell[j].trans[i].act,cell[j].area)
                    for k in range(len([solute_id])):
                        file = open('./'+file_to_save+'/'+cell[j].sex+'_'+cell[0].humOrrat+'_'+cell[j].segment+'_'+transporter_type+'_'+solute[solute_id]+str(memb_id[0])+str(memb_id[1])+'_'+sup_or_jux+'.txt','a')
                        file.write(str(fluxs*Scaletorq[j])+'\n')
                elif transporter_type == 'GLUT2':
                    solute_id,fluxs=glucose.glut2(cell[j],cell[j].ep,memb_id,cell[j].trans[i].act,cell[j].area)
                    for k in range(len([solute_id])):
                        file = open('./'+file_to_save+'/'+cell[j].sex+'_'+cell[0].humOrrat+'_'+cell[j].segment+'_'+transporter_type+'_'+solute[solute_id]+str(memb_id[0])+str(memb_id[1])+'_'+sup_or_jux+'.txt','a')
                        file.write(str(fluxs*Scaletorq[j])+'\n')			
                elif transporter_type == 'NHE3':
                    solute_id,fluxs=NHE3.nhe3(cell[j],cell[j].ep,memb_id,cell[j].trans[i].act,cell[j].area)
                    for k in range(len(solute_id)):
                        file = open('./'+file_to_save+'/'+cell[j].sex+'_'+cell[0].humOrrat+'_'+cell[j].segment+'_'+transporter_type+'_'+solute[solute_id[k]]+'_'+sup_or_jux+'.txt','a')
                        file.write(str(fluxs[k]*Scaletorq[j])+'\n')
                elif transporter_type == 'NaKATPase':
                    solute_id,fluxs=ATPase.nakatpase(cell[j],cell[j].ep,memb_id,cell[j].trans[i].act,cell[j].area)
                    for k in range(len(solute_id)):
                        file = open('./'+file_to_save+'/'+cell[j].sex+'_'+cell[0].humOrrat+'_'+cell[j].segment+'_'+transporter_type+'_'+solute[solute_id[k]]+str(memb_id[0])+str(memb_id[1])+'_'+sup_or_jux+'.txt','a')
                        file.write(str(fluxs[k]*Scaletorq[j])+'\n')
                        
                elif transporter_type == 'HATPase':
                    solute_id,fluxs=ATPase.hatpase(cell[j],cell[j].ep,memb_id,cell[j].trans[i].act,cell[j].area)
                    for k in range(len(solute_id)):
                        file = open('./'+file_to_save+'/'+cell[j].sex+'_'+cell[0].humOrrat+'_'+cell[j].segment+'_'+transporter_type+'_'+solute[solute_id[k]]+'_'+sup_or_jux+'.txt','a')
                        file.write(str(fluxs[k]*Scaletorq[j])+'\n')
                elif transporter_type == 'NKCC2A':
                    solute_id,fluxs=NKCC.nkcc2(cell[j],memb_id,cell[j].trans[i].act,cell[j].area,'A')
                    for k in range(len(solute_id)):
                        file = open('./'+file_to_save+'/'+cell[j].sex+'_'+cell[0].humOrrat+'_'+cell[j].segment+'_'+transporter_type+'_'+solute[solute_id[k]]+'_'+sup_or_jux+'.txt','a')
                        file.write(str(fluxs[k]*Scaletorq[j])+'\n')
                elif transporter_type == 'NKCC2B':
                    solute_id,fluxs=NKCC.nkcc2(cell[j],memb_id,cell[j].trans[i].act,cell[j].area,'B')
                    for k in range(len(solute_id)):
                        file = open('./'+file_to_save+'/'+cell[j].sex+'_'+cell[0].humOrrat+'_'+cell[j].segment+'_'+transporter_type+'_'+solute[solute_id[k]]+'_'+sup_or_jux+'.txt','a')
                        file.write(str(fluxs[k]*Scaletorq[j])+'\n')
                elif transporter_type == 'NKCC2F':
                    solute_id,fluxs=NKCC.nkcc2(cell[j],memb_id,cell[j].trans[i].act,cell[j].area,'F')
                    for k in range(len(solute_id)):
                        file = open('./'+file_to_save+'/'+cell[j].sex+'_'+cell[0].humOrrat+'_'+cell[j].segment+'_'+transporter_type+'_'+solute[solute_id[k]]+'_'+sup_or_jux+'.txt','a')
                        file.write(str(fluxs[k]*Scaletorq[j])+'\n')       
                elif transporter_type == 'KCC4':
                    solute_id,fluxs=KCC.kcc4(cell[j].conc,memb_id,cell[j].trans[i].act,cell[j].area)
                    for k in range(len(solute_id)):
                        file = open('./'+file_to_save+'/'+cell[j].sex+'_'+cell[0].humOrrat+'_'+cell[j].segment+'_'+transporter_type+'_'+solute[solute_id[k]]+'_'+sup_or_jux+'.txt','a')
                        file.write(str(fluxs[k]*Scaletorq[j])+'\n')
                elif transporter_type == 'ENaC':
                    solute_id,fluxs=ENaC.ENaC(cell[j],j,memb_id,cell[j].trans[i].act,cell[j].area,jvol)
                    for k in range(len(solute_id)):
                        file = open('./'+file_to_save+'/'+cell[j].sex+'_'+cell[0].humOrrat+'_'+cell[j].segment+'_'+transporter_type+'_'+solute[solute_id[k]]+'_'+sup_or_jux+'.txt','a')
                        file.write(str(fluxs[k]*Scaletorq[j])+'\n')
                elif transporter_type == 'NCC':
                    solute_id,fluxs=NCC.NCC(cell[j],j,memb_id,cell[j].trans[i].act,cell[j].area)
                    for k in range(len(solute_id)):
                        file = open('./'+file_to_save+'/'+cell[j].sex+'_'+cell[0].humOrrat+'_'+cell[j].segment+'_'+transporter_type+'_'+solute[solute_id[k]]+'_'+sup_or_jux+'.txt','a')
                        file.write(str(fluxs[k]*Scaletorq[j])+'\n')
                elif transporter_type == 'Pendrin':
                    solute_id,fluxs=Pendrin.Pendrin(cell[j],memb_id,cell[j].trans[i].act,cell[j].area)
                    for k in range(len(solute_id)):
                        file = open('./'+file_to_save+'/'+cell[j].sex+'_'+cell[0].humOrrat+'_'+cell[j].segment+'_'+transporter_type+'_'+solute[solute_id[k]]+'_'+sup_or_jux+'.txt','a')
                        file.write(str(fluxs[k]*Scaletorq[j])+'\n')
                elif transporter_type =='AE1':
                    solute_id,fluxs=AE1.AE1(cell[j],memb_id,cell[j].trans[i].act,cell[j].area)
                    for k in range(len(solute_id)):
                        file = open('./'+file_to_save+'/'+cell[j].sex+'_'+cell[0].humOrrat+'_'+cell[j].segment+'_'+transporter_type+'_'+solute[solute_id[k]]+'_'+sup_or_jux+'.txt','a')
                        file.write(str(fluxs[k]*Scaletorq[j])+'\n')
                elif transporter_type == 'HKATPase':
                    solute_id,fluxs=ATPase.hkatpase(cell[j],memb_id,cell[j].trans[i].act,cell[j].area)
                    for k in range(len(solute_id)):
                        file = open('./'+file_to_save+'/'+cell[j].sex+'_'+cell[0].humOrrat+'_'+cell[j].segment+'_'+transporter_type+'_'+solute[solute_id[k]]+'_'+sup_or_jux+'.txt','a')
                        file.write(str(fluxs[k]*Scaletorq[j])+'\n')
                elif transporter_type == 'NHE1':
                    solute_id,fluxs=NHE1.NHE1(cell[j],memb_id,cell[j].trans[i].act,cell[j].area)
                    for k in range(len(solute_id)):
                        file = open('./'+file_to_save+'/'+cell[j].sex+'_'+cell[0].humOrrat+'_'+cell[j].segment+'_'+transporter_type+'_'+solute[solute_id[k]]+'_'+sup_or_jux+'.txt','a')
                        file.write(str(fluxs[k]*Scaletorq[j])+'\n')
                elif transporter_type == 'NKCC1':
                    jsol,delmu = electrochemical.compute_ecd_fluxes(cell[j],jvol)
                    solute_id,fluxs=NKCC.nkcc1(cell[j],memb_id,cell[j].trans[i].act,delmu)
                    for k in range(len(solute_id)):
                        file = open('./'+file_to_save+'/'+cell[j].sex+'_'+cell[0].humOrrat+'_'+cell[j].segment+'_'+transporter_type+'_'+solute[solute_id[k]]+'_'+sup_or_jux+'.txt','a')
                        file.write(str(fluxs[k]*Scaletorq[j])+'\n')
                else:
                    raise Exception('What is this?',transporter_type)
