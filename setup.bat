pip install -r requirements.txt
pyinstaller --hidden-import babel.numbers --onefile Group_project21.py
mkdir AllFiles
move Group_project21.spec Allfiles
move requirements.txt Allfiles
move Group_project21.py Allfiles
move build Allfiles
move __pycache__ Allfiles
SET test=%cd%
move %test%\dist\Group_Project21.exe %test%

move setup.bat Allfiles