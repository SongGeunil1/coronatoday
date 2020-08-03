from flask import Blueprint, render_template, request, session
import requests
from bs4 import BeautifulSoup

main_blue = Blueprint('main_blue', __name__)

@main_blue.route('/')
def index() :
    req = requests.get('http://ncov.mohw.go.kr/bdBoardList_Real.do')
    soup = BeautifulSoup(req.text, 'html.parser')
    data = {'confirmator' : float([x.text for x in soup.select('dl > dd.ca_value')][0].replace(',','')), 
            'heal' : float([x.text for x in soup.select('dl > dd.ca_value')][2].replace(',','')),
            'die':float([x.text for x in soup.select('dl > dd.ca_value')][6].replace(',',''))}
    html = render_template('index.html', data = data)
    return html

@main_blue.route('/robots.txt')
def robots() :
    
    html = render_template('robots.txt')
    return html
