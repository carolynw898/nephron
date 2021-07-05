import matplotlib
#matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import os
import argparse

compare = 2 #2 or 3
save_figs = 1 # if want to save figs

solute_list = ['Na','K','Cl','HCO3','urea','NH4','glu', 'TA', 'Volume']
#solute_list = ['Na']

direct1 = 'Male_rat_normal'
sex1 = 'male'

direct2 = 'female-original'
sex2 = 'female'

direct3 = 'female-updated'
sex3 = 'female'

label1 = direct1
label2 = direct2
label3 = direct3

segs_early = ['pt', 'sdl', 'mtal', 'dct', 'cnt']
segs_cd = ['ccd','imcd']
seg_labels = ['PT', 'DL', 'mTAL', 'DCT', 'CNT', 'CCD', 'urine']

humOrrat = 'rat'

sup_ratio = 2.0/3.0
jux_ratio = 1-sup_ratio
neph_weight = [sup_ratio, 0.4*jux_ratio, 0.3*jux_ratio, 0.15*jux_ratio, 0.1*jux_ratio, 0.05*jux_ratio ]

neph_per_kidney = 36000 #number of nephrons per kidney
p_to_mu = 1e-6 #convert pmol to micromole
cf = neph_per_kidney * p_to_mu

#==========================================================================
# save figures/comments options (note: requires save_figs == 1)
#==========================================================================
if save_figs:
    plot_folder = input('where to save plots? ')
    comments = input('any comments? ')
    
    if os.path.isdir(plot_folder) == False:
        os.makedirs(plot_folder)
        
    comments_file = open('./'+plot_folder+'/comments.txt', 'w')
    comments_file.write(comments)
    comments_file.close()
#===========================================================================
# functions used
#===========================================================================

def get_delivery(direct, sex, solute, segment, supOrjux):
    os.chdir(direct)
    if solute == 'TA':
        fname1 = sex+'_'+humOrrat+'_'+segment+'_flow_of_H2PO4_in_Lumen'+supOrjux+'.txt'
        fname2 = sex+'_'+humOrrat+'_'+segment+'_flow_of_HPO4_in_Lumen'+supOrjux+'.txt'
        file1 = open(fname1, 'r')
        file2 = open(fname2, 'r')
        H2PO4_del = float(file1.readline())
        HPO4_del = float(file2.readline())
        delivery = (10**(7.4-6.8) * H2PO4_del - HPO4_del)/(1 + 10**(7.4-6.8))
        file1.close()
        file2.close
    elif solute == 'Volume':
        fname = sex+'_'+humOrrat+'_'+segment+'_water_volume_in_Lumen'+supOrjux+'.txt'
        file = open(fname, 'r')
        delivery = file.readline()
        file.close()
    else:
        fname = sex+'_'+humOrrat+'_'+segment+'_flow_of_'+solute+'_in_Lumen'+supOrjux+'.txt'
        file = open(fname, 'r')
        delivery = file.readline()
        file.close()
    os.chdir('..')
    return delivery

def get_out_deliv(direct, sex, solute, segment, supOrjux):
    # flow at the end of given segment
    os.chdir(direct)
    if solute == 'TA':
        fname1 = sex+'_'+humOrrat+'_'+segment+'_flow_of_H2PO4_in_Lumen'+supOrjux+'.txt'
        fname2 = sex+'_'+humOrrat+'_'+segment+'_flow_of_HPO4_in_Lumen'+supOrjux+'.txt'
        file1 = open(fname1, 'r')
        file2 = open(fname2, 'r')
        H2PO4_del = float(np.loadtxt(fname1, delimiter = '\n', unpack = True)[-1])
        HPO4_del = float(np.loadtxt(fname2, delimiter = '\n', unpack = True)[-1])
        delivery = (10**(7.4-6.8) * H2PO4_del - HPO4_del)/(1 + 10**(7.4-6.8))
        delivery = delivery*cf
        file1.close()
        file2.close
    elif solute == 'Volume':
        fname = sex+'_'+humOrrat+'_'+segment+'_water_volume_in_Lumen'+supOrjux+'.txt'
        file = open(fname, 'r')
        delivery = float(np.loadtxt(fname, delimiter = '\n', unpack = True)[-1])*cf
        file.close()
    else:
        fname = sex+'_'+humOrrat+'_'+segment+'_flow_of_'+solute+'_in_Lumen'+supOrjux+'.txt'
        file = open(fname, 'r')
        delivery = float(np.loadtxt(fname, delimiter = '\n', unpack = True)[-1])*cf
        file.close()
    os.chdir('..')
    return delivery

def get_cd_data(direct, sex, solute, segments):
    # this is for the OMCD or IMCD
    direct_deliv = []
    for seg in segments:
        if seg[-2:].lower() != 'cd':
            raise Exception('only for the collecting duct')
        direct_deliv.append(float(get_delivery(direct, sex, solute, seg, ''))*cf)
    return direct_deliv

def get_data(direct, sex, solute, segments):
    direct_deliv_sup = []
    direct_deliv_jux1 = []
    direct_deliv_jux2 = []
    direct_deliv_jux3 = []
    direct_deliv_jux4 = []
    direct_deliv_jux5 = []
    
    for seg in segments:
        direct_deliv_sup.append(float(get_delivery(direct, sex, solute, seg, '_sup')))
        direct_deliv_jux1.append(float(get_delivery(direct, sex, solute, seg, '_jux1')))
        direct_deliv_jux2.append(float(get_delivery(direct, sex, solute, seg, '_jux2')))
        direct_deliv_jux3.append(float(get_delivery(direct, sex, solute, seg, '_jux3')))
        direct_deliv_jux4.append(float(get_delivery(direct, sex, solute, seg, '_jux4')))
        direct_deliv_jux5.append(float(get_delivery(direct, sex, solute, seg, '_jux5')))
    
        if seg.lower() == 'cnt':
            direct_deliv_sup.append(float(get_out_deliv(direct, sex, solute, 'cnt', '_sup')))
            direct_deliv_jux1.append(float(get_out_deliv(direct,sex, solute, 'cnt', '_jux1')))
            direct_deliv_jux2.append(float(get_out_deliv(direct, sex, solute, 'cnt', '_jux2')))
            direct_deliv_jux3.append(float(get_out_deliv(direct, sex, solute, 'cnt', '_jux3')))
            direct_deliv_jux4.append(float(get_out_deliv(direct, sex, solute, 'cnt', '_jux4')))
            direct_deliv_jux5.append(float(get_out_deliv(direct, sex, solute, 'cnt', '_jux5')))
        
    
    temp= np.array(direct_deliv_sup)*neph_weight[0] + np.array(direct_deliv_jux1)*neph_weight[1]\
        + np.array(direct_deliv_jux2)*neph_weight[2] + np.array(direct_deliv_jux3)*neph_weight[3] \
            + np.array(direct_deliv_jux4)*neph_weight[4] + np.array(direct_deliv_jux4)*neph_weight[5]
    direct_deliv_number = temp*cf
    
    # row 0 is superficial vals
    # row 1 is jux1, row 2 jux2,...,row5 jux5
    direct_vals = np.matrix([direct_deliv_sup, direct_deliv_jux1, direct_deliv_jux2, 
                            direct_deliv_jux3, direct_deliv_jux4, direct_deliv_jux5])*cf
    
    sup_temp = direct_vals[0] * neph_weight[0]
    sup_temp1 = np.array(sup_temp) * cf
    sup_vals_weight = sup_temp1[0]

    jux_temp = direct_vals[1]*neph_weight[1] + direct_vals[2]*neph_weight[2]+\
        direct_vals[3]*neph_weight[3] + direct_vals[4]*neph_weight[4] + direct_vals[5]*neph_weight[5]
    jux_temp1 = np.array(jux_temp) * cf
    jux_vals_weight = jux_temp1[0]
    
    return direct_deliv_number, direct_vals, sup_vals_weight, jux_vals_weight


#===========================================================================
# retrieving data
#===========================================================================

for solute in solute_list:
    print(solute)
    direct_deliv_num1, direct_vals1, sup_vals1, jux_vals1 = get_data(direct1, sex1, solute, segs_early)
    direct_deliv_num2, direct_vals2, sup_vals2, jux_vals2 = get_data(direct2, sex2, solute, segs_early)
    if compare > 2:
        direct_deliv_num3, direct_vals3, sup_vals3, jux_vals3 = get_data(direct3, sex3, solute, segs_early)
    
    
    dir_del_urine1 = get_out_deliv(direct1, sex1, solute, 'imcd','')
    dir_del_urine2 = get_out_deliv(direct2, sex2, solute, 'imcd', '')
    if compare > 2:
        dir_del_urine3 = get_out_deliv(direct3, sex3, solute, 'imcd', '')
 
#===================================================
# print relevant values
#==================================================
    print(direct1)
    print('sup vals: ' + str(sup_vals1))
    print('jux vals: ' + str(jux_vals1))
    print('urine delivery: ' + str(dir_del_urine1))
    print('\n')
    
    print(direct2)
    print('sup vals: ' + str(sup_vals2))
    print('jux vals: ' + str(jux_vals2))
    print('urine delivery: ' + str(dir_del_urine2))
    print('\n')
    
    if compare > 2:
        print(direct3)
        print('sup vals: ' + str(sup_vals3))
        print('jux vals: ' + str(jux_vals3))
        print('urine delivery: ' + str(dir_del_urine3))
        print('\n')
    
    # full_deliv1 = np.append(direct_deliv_num1, dir_del_urine1)
    # full_deliv2 = np.append(direct_deliv_num2,dir_del_urine2)
    # full_deliv3 = np.append(direct_deliv_num3, dir_del_urine3)
        
#===================================================
# make figure
#===================================================

    fig, ax = plt.subplots()
    # figure settings
    fig.set_figheight(10)
    fig.set_figwidth(12)
    
    bar_width = 0.25
    
    # colors
    c1 = 'c'
    c2 = 'mediumvioletred'
    c3 = 'green'
    
    # fontsizes
    xlab_size = 18
    xticklab_size = 20
    ylab_size = 18
    yticklab_size = 20
    title_size = 20
    leg_size = 18
    
    # positiions
    sup_pos = np.arange(len(seg_labels[:6]))
    #full_pos = np.arange(len(seg_labels))
    later_pos = np.arange(len(seg_labels[:6]), len(seg_labels))
    
    
    # bar1
    sup1 = ax.bar(sup_pos, sup_vals1, bar_width, align = 'center', edgecolor = 'black', color = c1, label = label1)
    jux1 = ax.bar(sup_pos, jux_vals1, bar_width, bottom = sup_vals1, align='center', edgecolor = 'black', color = 'white')
    urine1 = ax.bar(later_pos, dir_del_urine1, bar_width, align='center', edgecolor='black', color = c1)
    
    # bar2
    sup2 = ax.bar(sup_pos + bar_width, sup_vals2, bar_width, align = 'center', edgecolor = 'black', color = c2, label = label2)
    jux2 = ax.bar(sup_pos + bar_width, jux_vals2, bar_width, bottom = sup_vals2, align = 'center', edgecolor = 'black', color = 'white')
    urine2 = ax.bar(later_pos + bar_width, dir_del_urine2, bar_width, align='center', edgecolor='black', color=c2)
    
    if compare >2:
        # bar3
        sup3 = ax.bar(sup_pos + 2*bar_width, sup_vals3, bar_width, align = 'center', edgecolor = 'black', color = c3, label=label3)
        jux3 = ax.bar(sup_pos + 2*bar_width, jux_vals3, bar_width, bottom = sup_vals3, align = 'center', edgecolor = 'black', color = 'white')
        urine3 = ax.bar(later_pos + 2*bar_width, dir_del_urine3, bar_width, align = 'center', edgecolor = 'black', color = c3)
    
    ax.set_xticks(np.arange(len(seg_labels))+1*bar_width)
    ax.set_xticklabels(seg_labels, fontsize=xticklab_size)
    ax.legend(fontsize=leg_size)
    plt.yticks(fontsize=yticklab_size)
    if solute == 'Volume':
        ax.set_ylabel('Volume delivery (nl/min)', fontsize = ylab_size)
    else:
        ax.set_ylabel(solute + ' delivery ($\mu$mol/min)', fontsize = ylab_size)
    ax.set_title(solute + ' delivery', fontsize = title_size)
    
    if save_figs:
        plt.savefig('./'+plot_folder+'/'+solute+' delivery', bbox_inches = 'tight')