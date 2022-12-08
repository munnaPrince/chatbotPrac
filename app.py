from flask import Flask, render_template,request, jsonify, send_file
#from chatbot import get_response,intents,predict_class
from search import SearchData
import os
#creating the flask app
app = Flask(__name__)
#creating the flags for determining the search type
jobflag,abendflag,jobabendflag,downloadflag = False,False,False,False
printflag=True
message,search_name,response,downloadText = "","","",""
#starting page
@app.route("/")
def index_get():
    value = f"Hi {searchdata.get_user_name()}, {searchdata.get_time()}"
    html_data = "please enter  <br>  1. To search by JobName <br> 2. To search by Abend code  <br> 3. To search by Jobname & Abend code"
    
    data_to_pass = {"start":value+"<br>"+html_data}
    return render_template("base.html",data = data_to_pass)      
#for downloading the output file        
@app.route("/download1")
def download_file():
    path = "Outputfiles"
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        return send_file(file_path,as_attachment=True,cache_timeout=0)
#for predicting the messages
@app.route("/predict", methods = ["GET", "POST"])
def predict(): 
    global jobflag,abendflag,jobabendflag,message,downloadflag,response,search_name,printflag
    text = request.get_json().get("message").upper()
    #searchdata.find_number(text)
    try:
        print("number trying in try")
        ans,jobflag,abendflag,jobabendflag = searchdata.find_number(text)
        #print(searchdata.find_number(text))
        #ans="ans"
        print(ans)
        message = {"answer":ans}
        return jsonify(message)
    except:
        if downloadflag== False and text.lower() =="yes":
            downloadflag = True
            
        print(jobflag,abendflag,jobabendflag)
        if jobflag:
            search_name = text
            response = searchdata.search_by_jobname(text)
        elif abendflag:
            search_name = text
            response = searchdata.search_by_abendCode(text)
        elif jobabendflag:
            search_name = text
            text = text.split(" ")
            if(len(text)==2):
                response = searchdata.search_by_jobname_abendcode(text[0], text[1])
            else:
                response = "please enter the jobname and abend code with a space between them"
                return jsonify({"answer":response})
            
    try:
        if response.shape[0]>1:
            message = searchdata.downloadable_text(response, search_name)

        else:
            message = {"answer": "no abend is present for this jobname in database"} 
        
        jobflag,abendflag,jobabendflag = False,False,False
    except:
        #if the list is empty it means, there is no data is present for the particular input
        #ints = predict_class(text.lower())
        #respon = get_response(ints,intents)
        message = {"answer": "tensorflow text will be printed here"}
    #returning the message/output in the json format            
    return jsonify(message)
if __name__ == "__main__":
    searchdata = SearchData()
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.run(debug=True)
    