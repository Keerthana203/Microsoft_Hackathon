**HOW TO RUN:**
1. Install Virtual Environment
command - .pip install virtualenv

2. Create Virtual Environment
command - virtualenv venv

3. Activate the Virtual Envirinment
command -  .venv\Scripts\activate

5. Install Requirements.txt
command - pip install -r requirements.txt

6. Download the spacy model 'en_core_web_sm'
command - python -m spacy download en_core_web_sm

--Ensure you have numpy 1.26.4 version

if needed or in case of error --when you are using powershell, by default it restricts some scripts, so you can change the execution policy to allow the scripts to run
command - 'Get-ExecutionPolicy' (to check the execution policy defaultly restricted)
and use this to change - 'Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass', then continue from step 3.

