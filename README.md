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





**Doctor-Aid**

This chatbot interacts with user by firstly asking their name, gender and age.

![Chatbot_image](https://github.com/Keerthana203/Microsoft_Hackathon/assets/129830843/1042e858-6dbb-495c-bd0e-16ea085c562a)

Then asks for the main symptoms and give recommendations for symptoms in which you have to select Yes/No


![chatbot_img](https://github.com/Keerthana203/Microsoft_Hackathon/assets/129830843/590fd806-02c6-414e-8db8-bc9b238bf7c8)


Then as a result of its prediction it gives the output and the description if needed

![chatbot_im](https://github.com/Keerthana203/Microsoft_Hackathon/assets/129830843/3e65965e-8a33-4c6a-8213-aaf1ae12157f)


This is the working flow of thi Doctor-Aid Healthcare chatbot which serves as a robust bot by utilizing NLP and some Machine Learning algorithms


