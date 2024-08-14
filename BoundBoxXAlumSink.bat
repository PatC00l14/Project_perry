pause

set /p project_name= What is your project name?:

mkdir %project_name%

cd .\..

mkdir C:\ElmerFEM\ElmerFEM\bin\%project_name%
mkdir C:\ElmerFEM\ElmerFEM\bin\%project_name%\dummy
mkdir C:\ElmerFEM\ElmerFEM\bin\%project_name%\UNV
mkdir C:\ElmerFEM\ElmerFEM\bin\%project_name%\VTU
mkdir C:\Projects\%project_name%\Logs
mkdir C:\Projects\%project_name%\Input_data




echo > C:\ElmerFEM\ElmerFEM\bin\%project_name%\case.sif

pause

echo %cd%

rem execute Salome and store in ELMER

cd C:\Projects\bin


python .\global_write.py %project_name%

copy input_csv.csv ..\%project_name%\Input_data\input_data.csv
copy .\XXdata_analysis.ipynb ..\%project_name%\XXdata_analysis.ipynb
copy .\XPythonPostProcessing.py ..\%project_name%\XPythonPostProcessing.py

cd .\..\..

C:\SALOME-9.12.0\W64\Python\python3.exe SALOME-9.12.0\salome -t BoundBoxXAlumSink.py args:%project_name%



cd .\..\..\ElmerFEM\ElmerFEM\bin

for %%x in  (%project_name%\UNV\*.*) do (
    echo Processing file: %%x
    elmergrid 8 2 "%%x" -autoclean -out %project_name%\dummy
    elmersolver > %project_name%\convergence_log.log 2>&1

    copy %project_name%\case_t0001.vtu %project_name%\VTU\%%~nx.vtu
    copy %project_name%\convergence_log.log ..\..\..\Projects\%project_name%\Logs\%%~nx.vtu
)

rem elmergrid 8 2 %project_name%\%project_name%.unv -autoclean -out %project_name%\dummy

cd .\..\..\..\Paraview\Paraview\bin

pvbatch.exe .\BoundBoxXAlumSink.py %project_name%

cd .\..\..\..\Projects\%project_name%

python .\XPythonPostProcessing.py



echo it has been a pleasure!

pause