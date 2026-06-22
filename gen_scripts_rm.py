import pandas as pd


run_bat_file = "run"
names = [
    "codrnaNorm",
    "covtype",
    "banana",
    "phoneme",
    "ring",
    "twonorm",
    "magic",
    "shuttle2"
    ]

javaSrc = 'C:\\PROGRA~1\\RapidMiner\\RAPIDM~1\\jre\\bin\\java'
javaCP =  'C:\\PROGRA~1\\RapidMiner\\RAPIDM~1\\lib\\*'
#javaSrc = 'C:\\Programs\\RapidMiner\\jre\\bin\\java'
#javaCP = 'C:\\Programs\\RapidMiner\\lib\\*'
javaMain = 'com.rapidminer.launcher.CommandLineLauncher'
scriptName = "process_v15"
scriptDir =  f'//Projects/2023/PairProtoEns/{scriptName}'

javaStart = f'{javaSrc} -Xmx10g -Xms10g -cp {javaCP} {javaMain} {scriptDir}'

dfDic = {"javaProg":[],
      "-MresultsDir=":[],
      "-MdataRepositoryDir=":[],
      "-MentryNameTest=":[],
      "-MentryName=":[]}
singleScript = True
run_bat=[]
for name in names:
    run_bat_cv = []
    for cvIndex in range(1,11):
        resultsDir      = f"d:\\mblachnik\\RMResults\\{scriptName}\\{name}\\"
        dataRepositoryDir = f'//Datasets/KeelNorm/{name}/'
        #dataRepositoryDir = f'//Datasets/AdditionalNorm/{name}/'
        #dataRepositoryDir = f'//Datasets/additional/{name}/'
        entryName       = f'{name}-10-{cvIndex}tra.dat'
        entryNameTest   = f'{name}-10-{cvIndex}tst.dat'

        stri = f'{javaStart} -MresultsDir={resultsDir} -MdataRepositoryDir={dataRepositoryDir} -MentryNameTest={entryNameTest} -MentryName={entryName}'
        if cvIndex<10:
            stri = f'start "{name}_{cvIndex}" {stri}'
        dfDic["javaProg"].append(javaStart)
        dfDic["-MresultsDir="].append(resultsDir)
        dfDic["-MdataRepositoryDir="].append(dataRepositoryDir)
        dfDic["-MentryNameTest="].append(entryNameTest)
        dfDic["-MentryName="].append(entryName)
        print(stri)
        run_bat_cv.append(stri)
        stri="@ECHO ===================================="
        print(stri)
        run_bat_cv.append(stri)
        stri= f"@ECHO ================ CV {cvIndex} file {name}"
        print(stri)
        run_bat_cv.append(stri)
        stri= "@ECHO ===================================="
        print(stri)
        run_bat_cv.append(stri)
    if not singleScript:
        run_bat_cv.append("TIMEOUT 60")
    bat_content = '\n'.join(run_bat_cv)
    if not singleScript:
        bat_name= f"{run_bat_file}_{name}.bat"
        with open(bat_name, 'w') as file:
            # Write the data to the file
            file.write(bat_content)
        run_bat.append(f"call {bat_name}") #If not single file then it creates a speparate bat file for every dataset.
    else: #Otherwise all content is included in the main bat file
        run_bat.append("@ECHO -------------------------------------------")
        run_bat.append(bat_content)
        run_bat.append("timeout /t 300")
        run_bat.append("@ECHO -------------------------------------------")

bat_name= f"{run_bat_file}.bat"
with open(bat_name, 'w') as file:
    # Join the list elements into a single string with a newline character
    data_to_write = '\n'.join(run_bat)
    # Write the data to the file
    file.write(data_to_write)

df = pd.DataFrame(dfDic)
df.to_csv("data\\scripts.csv",index=False)