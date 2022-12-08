import pandas as pd
import os
import datetime
import random

class SearchData:
    def __init__(self):
        self.data = pd.read_excel("Download_Input_files/Data.xlsx")
    def downloadable_text(self,response,search_name):
        '''
        this function returns the message text in the json format
        '''
        link_text = self.download_file(response, search_name)
        response = response.values.tolist()
        big_ans = ""
        headinglist = [
            "<br> JOBNAME : ",
            "<br> INCIDENT : ",
            "<br> ABEND CODE : ",
            "<br> ABEND REASON : ",
            "<br> RESOLUTION : ",
            "<br> ROOT CAUSE : "
                       ]
        for sublist in response:
            for i in range(0,min([len(sublist),len(headinglist)])):
                big_ans+=headinglist[i]+str(sublist[i+1])
            big_ans+="<br>"+"*"*50+"<br>"
        big_ans +="<br><br>"+link_text
        message = {"answer":big_ans} 
        return message
    def get_user_name(self):
        '''
        this function returns the local user's name in the string format
        '''
        return os.getlogin()
    def find_number(self,text):
        '''
        this function returns the text if the given parameter is an numbers
        '''
        print("in findNumber")
        text = int(text)
        print("text is",text)
        flags = [False,False,False]
        if text>0 and text<4:
            if text == 1:
                response = "please enter the Job Name"
            elif text == 2:
                response = "please enter the Abend Code"
            else:
                response = "please enter the Job Name and Abend code"
            flags[text-1]= True
        else:
            response = "please enter numbers between 1 and 3"
        return response,*flags
    #deleting all files in output folder
    def del_output_file(self):
        '''
        this function deletes the available files in the Outputfiles folder
        Returns
        -------
        None.
        '''
        path = "Outputfiles"
        for file in os.listdir(path):
            file_path = os.path.join(path, file)
            if os.path.exists(file_path):
                print(file_path,"file is removed")
                os.remove(file_path)    
    def get_time(self):
        '''
        this function gets the greeting according to the local time
        Returns
        -------
        string : TYPE
            DESCRIPTION.
        '''
        time = datetime.datetime.now().hour
        greetings =["Good","Marvelous","Fabulous","Great"]
        string = random.choice(greetings)
        if(time>0 and time <12):
            string += " Morning"
        elif(time>=12 and time<=17):
            string += " Afternoon"
        else:
            string += " Evening"
        return string
    def download_file(self,response,search_name):
        '''
        this function returns the html string to download the output file
        '''
        
        self.del_output_file()
        output_filename = "outputfiles/output"+search_name+".xlsx"
        print(output_filename)
        #response.to_excel("outputfiles/output.xlsx")
        response.to_excel(output_filename)
        on_click ='"'+"window.location.href='/download1';"+'"'
        anchor_string = "<a onclick="+on_click+"><b>HERE</b></a>"
        response_string = f'please click {anchor_string} to download the file'
        return response_string
    def search_by_abendCode(self,abendcode):
        '''
        this function return the resultant dataframe by the abend code
        '''
        self.response = self.data.loc[self.data["Abend Code"] == abendcode.upper()]
        return self.response
    def search_by_jobname(self,jobname):
        '''
        this function return the resultant dataframe by the given job name
        '''
        self.response = self.data.loc[self.data["Job Name"] == jobname.upper()]
        return self.response
    def search_by_jobname_abendcode(self,job,abend):
        '''
        this function return the resultant dataframe by the abend code and by the given
        job name
        '''
        self.response = self.data.loc[(self.data['Job Name']==job.upper()) &
                                      (self.data["Abend Code"]==abend.upper())]
        return self.response
    

