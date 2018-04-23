from googlesearch import search
from urllib.request import urlopen
import urllib.request
from bs4 import BeautifulSoup
import re
import pyautogui
import os
import pytesseract
import numpy
import cv2
import PIL
from PIL import Image
import time

pytesseract.pytesseract.tesseract_cmd = "C:\\Users\\Austin\\Tesseract-OCR\\tesseract.exe"

def search_web(query):
    return search(query, tld="co.in", num=2, stop=1, pause=1)

def grab_text(url_list):

    try:
        html = urlopen(url_list[0])
        return html
    except urllib.error.HTTPError as err:
        print("http error in first site")
        html = urlopen(url_list[1])
        return html
    

def grab_image():
    question_interface = numpy.array(PIL.ImageGrab.grab(bbox=(343,402,677,725))) #650,218,946,500
    question_interface = cv2.cvtColor(question_interface,cv2.COLOR_BGR2RGB)
    question_interface = cv2.resize(question_interface, (0,0),fx=2,fy=2) #3,3
    ret,question_interface = cv2.threshold(question_interface,127,255,cv2.THRESH_BINARY)
    question_interface = PIL.Image.fromarray(question_interface,'RGB')
    return pytesseract.image_to_string(question_interface)

def break_ans_ques(text):
    first_break = text.find("\n\n")
    question = text[0:first_break+1]
    print("this is the question: " + question)
    text = text[first_break+2:].replace("\n\n","\n")
    print("these are the answers : " + text)
    ans_1,ans_2,ans_3 = text.split("\n")
    all_text = [question,ans_1,ans_2,ans_3]
    return all_text

def result_analysis_1(answers):
    sum = 0
    results = [html_fixed.count(answers[0]),html_fixed.count(answers[1]),html_fixed.count(answers[2])]
    
    for result in results:
        sum = sum + result

    print(answers[0], end="")    
    print(' : {0:.2f}'.format((results[0]/sum)))
    print(answers[1], end="")    
    print(' : {0:.2f}'.format((results[1]/sum)))
    print(answers[2], end="")    
    print(' : {0:.2f}'.format((results[2]/sum)))

#def result_analysis_2(answers):

def print_time():
    millis = int(round(time.time()*1000))
    print(millis)
    

if __name__ == '__main__':
    print("start of program")
    print_time()
    all_text = grab_image()
    print("after grab image: "),
    print_time()
    all_text = break_ans_ques(all_text)
    print("after break_ans_ques: "),
    print_time()
    query = all_text[0]
    url_list = list(search_web(query))
    print("after search_web: "),
    print_time()
    sample_ans_1 = all_text[1]
    sample_ans_2 = all_text[2]
    sample_ans_3 = all_text[3]
    page_html = (grab_text(url_list).read())
    print("after reading url: "),
    print_time()
    soup = BeautifulSoup(page_html, 'html.parser')
    print("after html parser: "),
    print_time()
    html_fixed = (soup.prettify())
    print("after html cleaning up: "),
    print_time()
    answers = [sample_ans_1,sample_ans_2,sample_ans_3]

    result_analysis_1(answers)
    print("after analysis: "),
    print_time()
    
    
    
