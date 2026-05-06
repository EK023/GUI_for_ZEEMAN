import numpy as np
import os
import pandas as pd
import json
import configparser
import sys

def check_model_atm(model_atm_folder="./data/ATLAS9"):
    # Change model atmospheres and updates the lma executable

    if not os.path.isdir(model_atm_folder):
        raise FileNotFoundError("No File Found")
    model_atm_folder = os.path.join(model_atm_folder,'')

    update_model_atm = False
    filename = "lmau-zuc0.9.5.2-dil.f"

    with open(filename,"r") as file:
        lines = file.readlines()
        for iline in [1046,1452]:
            if model_atm_folder in lines[iline]:
                continue
            else:
                indmin,indmax = lines[iline].find("\'"),lines[iline].find("\'",-1)
                lines[iline] = lines[iline].replace(lines[iline][indmin+1:indmax-2],model_atm_folder)
                print(lines[iline])
                update_model_atm = True

    if update_model_atm:
        with open(filename,"w") as file:
            for line in lines:
                file.write(line)

        os.system("make lma")

    else:
        print("Model atmosphere and lma are up-to-date!")

def update_zmodel(wave_range_list,res,run_format,vsini=0,vmic=0,vmac=0):
    path = "data/zmodel.dat"

    # copies a typical format of zmodel.dat file and edit it with the new parameters.
    # there are better ways of doing this. Will improve it later!!
    os.system("cp zmodel_format.dat data/zmodel.dat")
    zmodelfile = open(path)
    lines = zmodelfile.readlines()
    zmodelfile.close()
    lines[3] = f"{len(wave_range_list)}\n"
    lines[7] = f"1   {res}\n"
    if run_format=='syn':
        lines[13] = f' 90.0  {vsini}E+05  {vmic}E+05  {vmac}E+05\n'
    temp_lines = []
    for wave_range in wave_range_list:
        w1 = wave_range[0]
        w2 = wave_range[1]
        temp_lines.append(f"{w1}  {w2}\n")

    lines = lines[0:5]+temp_lines+lines[6:]
    with open(path,"w") as file:
        for line in lines:
            file.write(line)

def update_inlmam(vr,vsini,vmic,vmac,teff,logg,metal,fitvr,fitvsini,fitvmic,fitvmac,fitteff,fitlogg,fitmetal,contpoly,elements):

    # a dictionary of atomic numbers and their respective element names
    with open('elementdic.dat') as f:
        elementdic = json.load(f)

    elementkey_list = list(elementdic.keys())
    elementval_list = list(elementdic.values())

    # copies a typical format of inlmam.dat file and edit it with the new parameters.
    # there are better ways of doing this. Will improve it later!!
    inlmamfile = open("inlmam_format.dat")
    inlmam_lines = inlmamfile.readlines()
    inlmamfile.close()
    inlmam_lines[3] = f'{vr}E+5   {fitvr}\n'
    inlmam_lines[5] = f'{vsini}E+5   {fitvsini}\n'
    inlmam_lines[7] = f'{vmic}E+5   {fitvmic}\n'
    inlmam_lines[9] = f'{vmac}E+5   {fitvmac}\n'
    inlmam_lines[11] = f'{teff}   {fitteff}\n'
    inlmam_lines[13] = f'{logg}   {fitlogg}\n'
    inlmam_lines[15] = f'{metal}   {fitmetal}\n'
    inlmam_lines[25] = f'{contpoly}\n'

    with open("inlmam.dat", "w") as file:
        for iinlmam_line,inlmam_line in enumerate(inlmam_lines):
             if iinlmam_line==27 and len(elements) != 0:
                for element in elements:
                    if isinstance(element[0],int):
                        zeroth_pos = element[0]
                        file.write(
                            f'{zeroth_pos}       {element[1]}     {element[2]}    {elementdic[str(element[0])]}\n')
                    else:
                        position = elementval_list.index(element[0])
                        zeroth_pos = elementkey_list[position]
                        file.write(
                            f'{zeroth_pos}       {element[1]}     {element[2]}    {element[0]}\n')
             file.write(inlmam_line)

def fit_wave_ranges(vr,vsini,vmic,vmac,teff,logg,metal,fitvr,fitvsini,fitvmic,fitvmac,
                    fitteff,fitlogg,fitmetal,contpoly,wave_range_lists,res,mainpath,vlinespath,obsspecpath,elements=[],
                    fitinlmam=True, fitzmodel=True,savefile=True,showplot=True, run_format='fit'):

    fitlist = [fitteff, fitlogg, fitvsini, fitvmic, fitvmac, fitvr, fitmetal, 0]

    os.system(f"cp {vlinespath} data/vlines.dat")
    if run_format=='fit':
        os.system(f"cp {obsspecpath} observed.dat")

    if len(elements)!=0:
        for elem in elements:
            if elem[2]==1:
                fitlist = fitlist+[elem[2]]

    if savefile==True:
        if not os.path.exists(mainpath):
            os.mkdir(mainpath)

        if len(os.listdir(mainpath)) == 0:
            foldernum = 1
        else:
            mainpath_filelist = os.listdir(mainpath)
            filelist_nums = [int(i.split("/")[-1].split("_")[-1].replace("paramfit", "")) for i in mainpath_filelist]
            foldernum = max(filelist_nums) + 1

        # maybe better way of naming the folder in which results.dat and plotff1i are saved. mainpath variable
        # stores the name of the folder in which the above-mentioned files are stored
        wmin = wave_range_lists[0][0][0]
        wmax = wave_range_lists[0][-1][-1]
        mainpath = os.path.join(mainpath, f"{wmin}-{wmax}_paramfit{foldernum}")

        if not os.path.exists(mainpath):
            os.mkdir(mainpath)

    resultslist = []
    wave_range_namelist = []
    for wave_range_list in wave_range_lists:
        wave_range_name = f"{wave_range_list[0][0]}-{wave_range_list[-1][-1]}"
        print(wave_range_name)
        path = f"{mainpath}/{wave_range_name}"
        wave_range_namelist.append(f"{wave_range_name}")

        if fitinlmam:
            update_inlmam(vr,vsini,vmic,vmac,teff,logg,metal,fitvr,fitvsini,fitvmic,fitvmac,fitteff,fitlogg,fitmetal,contpoly,elements)

        if fitzmodel:
            update_zmodel(wave_range_list, res,run_format,vsini, vmic, vmac)

        # runs the Zeeman code here
        if run_format=='fit':
            os.system("./lma")
        elif run_format=='syn':
            os.system('./zuc')
            return

        else:
            raise ValueError("Unexpected value for 'run_format', expected one of ['fit', 'syn'], but got %s"% run_format)

        # saving the files to the "mainpath" folder
        if savefile:
            os.mkdir(path)
            os.system(f"cp plotff1i {path}/plotff1i")
            os.system(f"cp results.dat {path}/results.dat")
        result = open("results.dat").read()
        resultslist.append(result)

        # plotting the synthetic and observed spectrum
        if showplot:
            os.system(f"python3 plotspec-vald-gui3c.py plotff1i")
    outputfile = os.path.join(mainpath,"results.csv")

    # making a csv file storing the parameter values, and whether they were used for fitting or not
    df = results_to_csv(resultslist,wave_range_namelist,fitlist,outputfile,elements,savefile)
    return df

def results_to_csv(resultslist,waverangelist,fitlist,outputfile,elements,savefile=False):

    with open('elementdic.dat') as f:
        elementdic = json.load(f)
    dfsavedict = {}

    # reading the results.dat file for the parameters and abundances used to fit
    for iresults,results in enumerate(resultslist):

        # choosing the regions where the final results are displayed in the results.dat file
        redchisqrbegind = results.rfind("reduced chi^2")
        redchisqrendind = results.find("points in fit")
        redchisqrlist = results[redchisqrbegind:redchisqrendind].split()
        redchisqr,delredchisqr = redchisqrlist[2],redchisqrlist[-1]

        parambegind = results.find("Teff")
        paramendind = results.find("El   Abundance")
        abunbegind = paramendind

        contcoeff = False
        if "cont coeff" in results:
            contcoeff = True

        if contcoeff:
            abunendind = results.find('cont coeff')
        else:
            abunendind = len(results)

        abunsstrlist = results[abunbegind:abunendind].split("\n")[1:-1]

        paramsstrlist = results[parambegind:paramendind-1].split("\n")


        paramlist = []

        # reading the parameters
        for paramstr in paramsstrlist:
            paramstrlist = paramstr.split(" ")
            params = []
            for iparam,param in enumerate(paramstrlist):
                if len(param)!=0:
                    if iparam == 0:
                        params.append(param)
                    else:
                        params.append(float(param))
            paramlist.append(params)

        # reading the abundances used to fit
        if len(abunsstrlist)>0:
            abunlist = []
            for abunstr in abunsstrlist:
                abunstr = abunstr.strip()
                abunstrlist = abunstr.split(" ")
                abuns = []
                for iabun, abun in enumerate(abunstrlist):
                    if len(abun) != 0:
                        if iabun==0:
                            abuns.append(elementdic[abun])
                        else:
                            abuns.append(float(abun))
                abunlist.append(abuns)

            paramlist = paramlist+abunlist

        paramlist = [['redchisqr',redchisqr+"("+delredchisqr+")",0]] + paramlist
        paramlist = np.array(paramlist)

        # making a dictionary of parameters and their values and also if they were fit or not
        if iresults==0:
            dfsavedict["params"] = paramlist[:,0]
            dfsavedict["fit"] = ['0']+fitlist


        # saved the parameter values estimated based on their respective wavelength regions
        dfsavedict[f"{waverangelist[iresults]}"] = paramlist[:,1]

    # reading the elemental abundances used which were not fit
    tempelement = []
    for el in elements:
        if el[2]==0:
            tempelement.append(el)
        else:
            continue

    tempelement = np.array(tempelement)

    elparams = []
    if len(tempelement)!=0:
        for ii,i in enumerate(tempelement[:,0]):
            try:
                elname = elementdic[i]

            except:
                elname = i
            elparams.append(elname)
        elparams = np.array(elparams)

        # appending the abundanced to the dictionary of parameters
        dfsavedict["params"] = np.append(dfsavedict["params"],elparams)
        dfsavedict["fit"] = np.append(dfsavedict["fit"],tempelement[:,2])
        for i in list(dfsavedict.keys())[2:]:
            dfsavedict[i] = np.append(dfsavedict[i],tempelement[:,1])

    # converting the dictionary to a dataframe and saving it
    ind = np.where(dfsavedict['params'] == 'Teff')[0][0]
    dfsavedict['params'][ind] = 'teff'
    df = pd.DataFrame(dfsavedict)
    if savefile:
        df.to_csv(outputfile, index = False, encoding='utf-8')
    print(df)
    return df

def convert_wave_from_text(filename = "wave-regions.txt"):
    wave_range_lists = []
    lines = open(filename).readlines()
    lines = np.array(lines)
    ind = np.where(lines == 'n\n')[0]
    linesList = np.split(lines, ind)
    for lines in linesList:
        wave_range_sublists = []

        condition = lines != 'n\n'
        lines = lines[condition]

        for line in lines:
            w1, w2 = line.split("\t")
            w1, w2 = float(w1), float(w2)
            maxdiff = 200
            n = (w2 - w1) / maxdiff
            n = int(n)
            if w2 - w1 > maxdiff:
                for i in range(n):
                    wave_range_lists.append([w1 + i * maxdiff, w1 + (i + 1) * maxdiff])
                    if i == n - 1 and w1 + (i + 1) * maxdiff != w2:
                        wave_range_sublists.append([w1 + (i + 1) * maxdiff, w2])

            else:
                wave_range_sublists.append([w1, w2])
        wave_range_lists.append(wave_range_sublists)

    return wave_range_lists

# this is the code to run the Zeeman from Python. You need to provide a configuration file here. The default filename is
# config. You can either run it from the terminal or using an IDE.
def run(configfile,**kwargs):
    Config = configparser.ConfigParser(inline_comment_prefixes="#")
    Config.read(configfile)
    res = json.loads(Config.get('Params','res'))
    vr,fitvr = json.loads(Config.get('Params','vr,fitvr'))
    vsini, fitvsini = json.loads(Config.get('Params', 'vsini,fitvsini'))
    vmic, fitvmic = json.loads(Config.get('Params', 'vmic,fitvmic'))
    vmac, fitvmac = json.loads(Config.get('Params', 'vmac,fitvmac'))
    teff,fitteff = json.loads(Config.get('Params', 'teff,fitteff'))
    logg,fitlogg = json.loads(Config.get('Params', 'logg,fitlogg'))
    metal, fitmetal = json.loads(Config.get('Params', 'metal,fitmetal'))
    contpoly = json.loads(Config.get('Params','contpoly'))
    elements = json.loads(Config.get('Params', 'elements'))
    savefile = bool(int(json.loads(Config.get('Params', 'savefile'))))
    showplot = bool(int(json.loads(Config.get('Params', 'showplot'))))
    read_wave_from_text = bool(int(json.loads(Config.get('Params', 'read_wave_from_text'))))
    mainpath = json.loads(Config.get('Params', 'mainpath'))
    vlinespath = json.loads(Config.get('Params', 'vlinespath'))
    obsspecpath = json.loads(Config.get('Params', 'obsspecpath'))
    wave_range_lists = json.loads(Config.get('Params', 'wave_range_lists'))
    iterlist = json.loads(Config.get('Params', 'iterlist'))
    n_iter = json.loads(Config.get('Params', 'n_iter'))

    res = kwargs.get("res", res)
    vr = kwargs.get("vr", vr)
    vsini = kwargs.get("vsini", vsini)
    vmic = kwargs.get("vmic", vmic)
    vmac = kwargs.get("vmac", vmac)
    teff = kwargs.get("teff", teff)
    logg = kwargs.get("logg", logg)
    metal = kwargs.get("metal", metal)
    contpoly = kwargs.get("contpoly",contpoly)
    wave_range_lists = kwargs.get("wave_range_lists", wave_range_lists)
    obsspecpath = kwargs.get("obsspecpath", obsspecpath)
    vlinespath = kwargs.get("vlinespath",vlinespath)
    mainpath = kwargs.get("mainpath", mainpath)
    savefile = kwargs.get("savefile", savefile)
    showplot = kwargs.get("showplot",showplot)
    iterlist = kwargs.get("iterlist",iterlist)
    try:
        run_format = json.loads(Config.get('Params', 'run_format'))
    except:
        run_format = "fit"

    run_format = kwargs.get("run_format",run_format)

    try:
        model_atm_folder = json.loads(Config.get('Params', 'model_atm_folder'))
    except:
        model_atm_folder = "ATLAS9"

    model_atm_folder = kwargs.get("model_atm_folder",model_atm_folder)

    if "elements" in kwargs.keys():
        elements.append(kwargs["elements"])

    # Check the model atmosphere
    check_model_atm(model_atm_folder=model_atm_folder)

    # Read wavelength range from wave-region.txt
    if read_wave_from_text:
        wave_range_lists=convert_wave_from_text()

    if run_format=='syn':
        try:
            model_atm_file = json.loads(Config.get('Params', 'model_atm_file'))
            model_atm_file = kwargs.get("model_atm_file", model_atm_file)
            if not os.path.exists(model_atm_file):
                raise FileNotFoundError(f"No file with filename - {model_atm_file} found")
            os.system(f"cp {model_atm_file} ./data/atmosphere.krz")

        except:
            raise ValueError("No parameter named model_atm_file found.")

    if len(iterlist)==0:
        fit_wave_ranges(vr, vsini, vmic, vmac, teff, logg, metal, fitvr, fitvsini, fitvmic, fitvmac, fitteff, fitlogg,
                        fitmetal,contpoly,wave_range_lists, res, mainpath, savefile=savefile, vlinespath=vlinespath, obsspecpath=obsspecpath,
                        showplot=showplot, elements=elements,run_format=run_format)

    else:
        iter_param_dic = {}
        track_df_dict = {}
        for iwave_range_list,wave_range_list in enumerate(wave_range_lists):
            iterteff, iterlogg, itervr, itervsini, itervmic, itervmac, itermetal,itercontpoly,iterelements =  teff,logg,vr,vsini,vmic,vmac,metal,contpoly,elements
            wave_range_name = f'{wave_range_list[0][0]}-{wave_range_list[-1][1]}'
            track_df_dict[wave_range_name] = pd.DataFrame()
            for iter in range(n_iter):
                for iterparams in iterlist:
                    paramdict = {'teff': iterteff, 'logg': iterlogg, 'vr': itervr, 'vsini': itervsini, 'metal': itermetal, 'vmic': itervmic,'vmac': itervmac,'contpoly':contpoly}
                    fitparamdict = {'teff': 0, 'logg': 0, 'vr': 0, 'vsini': 0, 'metal': 0, 'vmic': 0, 'vmac': 0,'contpoly':0}
                    paramList = np.array(list(fitparamdict.keys()))
                    for iterparam in iterparams:
                        if iterparam in paramList:
                            ind = np.where(paramList==iterparam)[0][0]
                            fitparamdict[paramList[ind]] = 1
                        else:
                            for iterelement in iterelements:
                                if iterelement[0]==iterparam:
                                    iterelement[2]=1

                    
                    df = fit_wave_ranges(vr=paramdict['vr'], vsini=paramdict['vsini'], vmic=paramdict['vmic'], vmac=paramdict['vmac'],
                                         teff=paramdict['teff'], logg=paramdict['logg'], metal=paramdict['metal'], contpoly=paramdict['contpoly'], fitvr=fitparamdict['vr'],
                                         fitvsini=fitparamdict['vsini'], fitvmic=fitparamdict['vmic'],fitvmac=fitparamdict['vmac'],
                                         fitteff=fitparamdict['teff'],fitlogg=fitparamdict['logg'],fitmetal=fitparamdict['metal'],
                                         wave_range_lists=[wave_range_list], res=res, mainpath=mainpath, savefile=savefile, vlinespath=vlinespath,
                                         obsspecpath=obsspecpath,showplot=showplot, elements=iterelements,run_format=run_format)



                    newfitparams = dict(zip(df['params'],df[df.columns[-1]]))
                    iterteff,iterlogg,itervr,itervsini,itervmic,itervmac,itermetal,itercontpoly = (newfitparams['teff'],newfitparams['logg'],newfitparams['v_r'],newfitparams['vsini'],
                                                      newfitparams['vmic'],newfitparams['vmac'],newfitparams['metal'],newfitparams['contpoly'])
                    if len(newfitparams.keys())>8:
                        elnames = list(newfitparams.keys())[9:]
                        elabuns = list(newfitparams.values())[9:]
                        iterelements = []
                        for i in range(len(elnames)):
                            iterelements.append([elnames[i],elabuns[i],0])

                    if iwave_range_list==0:
                        iter_param_dic['params'] = df['params']

                temp_df = df.rename(columns={wave_range_name: f"{iter}-iter"})
                temp_df.drop('fit', axis=1, inplace=True)
                if iter == 0:
                    track_df_dict[wave_range_name] = pd.concat([track_df_dict[wave_range_name], temp_df], axis=1)
                else:
                    track_df_dict[wave_range_name] = pd.concat([track_df_dict[wave_range_name], temp_df.iloc[:, 1]], axis=1)

            iter_param_dic[df.columns[-1]] = df[df.columns[-1]]

        for wave_range_name in track_df_dict.keys():
            track_df_dict[wave_range_name].to_csv(os.path.join(mainpath,wave_range_name)+".csv",index=False)
        iter_param_df = pd.DataFrame(iter_param_dic)
        print(iter_param_df)
        iter_param_df.to_csv(os.path.join(mainpath,"summary.csv"),index=False)

if __name__=="__main__":
    try:
        configfile = sys.argv[1]
    except:
        configfile = "config"
    run(configfile=configfile)
