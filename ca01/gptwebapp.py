'''
gptwebapp shows how to create a web app which ask the user for a prompt
and then sends it to openai's GPT API to get a response. You can use this
as your own GPT interface and not have to go through openai's web pages.

We assume that the APIKEY has been put into the shell environment.
Run this server as follows:

On Mac
% pip3 install openai
% pip3 install flask
% export APIKEY="......."  # in bash
% python3 gptwebapp.py

On Windows:
% pip install openai
% pip install flask
% $env:APIKEY="....." # in powershell
% python gptwebapp.py
'''
from flask import request,redirect,url_for,Flask
from gpt import GPT
import os

app = Flask(__name__)
gptAPI = GPT(os.environ.get('APIKEY'))

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q789789uioujkkljkl...8z\n\xec]/'

@app.route('/')
def index():
    ''' displays a link to the general query page '''
    print('processing / route')
    return f'''
        <h1>About Page</h1>
        <a href="{url_for('about')}">An about page which explains what your program does</a>
        <h1>Team Page</h1>
        <a href="{url_for('team')}">A team page which has a short bio of each member of the team and what their role was</a>
        <h1>Form Page</h1>
        <a href="{url_for('form')}">A form page for each team member which ask the user for some input, then calls the appropriate GPT method to get the response, which it sends back to the browser.</a>
    '''

@app.route('/gptdemo', methods=['GET', 'POST'])
def gptdemo():
    ''' handle a get request by sending a form 
        and a post request by returning the GPT response
    '''
    if request.method == 'POST':
        prompt = request.form['prompt']
        answer = gptAPI.getResponse(prompt)
        return f'''
        <h1>GPT Demo</h1>
        <pre style="bgcolor:yellow">{prompt}</pre>
        <hr>
        Here is the answer in text mode:
        <div style="border:thin solid black">{answer}</div>
        Here is the answer in "pre" mode:
        <pre style="border:thin solid black">{answer}</pre>
        <a href={url_for('gptdemo')}> make another query</a>
        '''
    else:
        return '''
        <h1>GPT Demo App</h1>
        Enter your query below
        <form method="post">
            <textarea name="prompt"></textarea>
            <p><input type=submit value="get response">
        </form>
        '''

@app.route('/about')
def about():
    ''' explains what your program does '''
    return '''
    <h1>About Page</h1>
    This program could read formulas from the user and calculate the result.
    It can also read a number from the user and show how many prime numbers
    are there within that number.
    '''

@app.route('/team')
def team():
    ''' has a short bio of each member of the team and what their role was '''
    return '''
    <h1>Team Page</h1>
    Yuxuan Xiong: CS major; leader of the team
    Zone Zhang: CS major; member of the team
    '''

@app.route('/form')
def form():
    ''' links to each team member's methods '''
    return f'''
    <h1>Zone Zhang - Calculate Formula</h1>
    <a href="{url_for('formula')}">Use GPT to calculate a formula</a>
    <h1>Yuxuan Xiong - Get The Number of Prime</h1>
    <a href="{url_for('getPrime')}">Use gpt to find the number of Prime in a certain range</a>
    '''

@app.route('/formula', methods=['GET', 'POST'])
def formula():
    ''' reads the formula and use GPT to calculate it '''
    if request.method == 'POST':
        formula = request.form['prompt']
        result = gptAPI.calculateFormula(formula)
        return f'''
        <h1>GPT Demo</h1>
        <pre style="bgcolor:yellow">{formula}</pre>
        <hr>
        Here is the result in text mode:
        <div style="border:thin solid black">{result}</div>
        Here is the result in "pre" mode:
        <pre style="border:thin solid black">{result}</pre>
        <a href={url_for('formula')}> Do you want to find the result of another fomula?</a>
        '''
    else:
        return '''
        <h1>Calculate Formula</h1>
        Please enter a formula, we will calculate the result for you!
        <form method="post">
            <textarea name="prompt"></textarea>
            <p><input type=submit value="get response">
        </form>
        '''
    
@app.route('/Get_Prime', methods=['GET', 'POST'])
def getPrime():
    ''' handle a get request by sending a form 
        and a post request by returning the GPT response
    '''
    if request.method == 'POST':
        prompt = request.form['prompt']
        answer = gptAPI.getNumPrime(prompt)
        return f'''
        <h1>Get The Number of Prime in Ceartain Range</h1>
        <pre style="bgcolor:yellow">{prompt}</pre>
        <hr>
        Here is the answer in text mode:
        <div style="border:thin solid black">{answer}</div>
        Here is the answer in "pre" mode:
        <pre style="border:thin solid black">{answer}</pre>
        <a href={url_for('getPrime')}> make another query</a>
        '''
    else:
        return '''
        <h1>Get The Number of Prime in Ceartain Range</h1>
        Please enter a number, we will help you find how many prime number inside this range
        <form method="post">
            <textarea name="prompt"></textarea>
            <p><input type=submit value="get response">
        </form>
        '''

if __name__=='__main__':
    # run the code on port 5001, MacOS uses port 5000 for its own service :(
    app.run(debug=True,port=5001)