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
from PIL import Image, ImageEnhance, ImageFilter
import time

pytesseract.pytesseract.tesseract_cmd = "C:\\Users\\Austin\\Tesseract-OCR\\tesseract.exe"
    

def search_web(query):
    return search(query, tld="co.in", num=2, stop=1, pause=0)

def grab_text(url_list):

    try:
        html = urlopen(url_list[0])
        return html
    except urllib.error.HTTPError as err:
        print("http error in first site")
        html = urlopen(url_list[1])
        return html
    
#def screenshot():
    #pic = pyautogui.screenshot(region=(23,216,380,376))
    #image = pic.save('Screenshot.jpg')
    #image = Image.open('Screenshot.jpg')
    #return image

def grab_image():
    #question
    question_interface = numpy.array(PIL.ImageGrab.grab(bbox=(23,215,402,360))) #23,215,402,359
    question_interface = cv2.cvtColor(question_interface,cv2.COLOR_BGR2RGB)
    question_interface = cv2.resize(question_interface, (0,0),fx=2,fy=2) #3,3
    ret,question_interface = cv2.threshold(question_interface,127,255,cv2.THRESH_BINARY)
    question = pytesseract.image_to_string(question_interface)
    #answer 1
    ans_1_interface = numpy.array(PIL.ImageGrab.grab(bbox=(23,361,402,580))) #23,315,402,439
    ans_1_interface = cv2.cvtColor(ans_1_interface,cv2.COLOR_BGR2RGB)
    ans_1_interface = cv2.resize(ans_1_interface, (0,0),fx=3,fy=3) #3,3
    ret,ans_1_interface = cv2.threshold(ans_1_interface,127,255,cv2.THRESH_BINARY)
    answers = pytesseract.image_to_string(ans_1_interface)
    
    all_text = [question,answers]
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
    answers = all_text[1].split("\n\n")
    print("after grab image: "),
    print_time()
    
    print("after break_ans_ques: "),
    print_time()
    query = all_text[0]
    url_list = list(search_web(query))
    for link in url_list:
        if "quora" in link:
            url_list.remove(link)
    for link in url_list:
        print(link)
    print("after search_web: "),
    print_time()
    answers[0] = answers[0].replace(".","")
    answers[1] = answers[1].replace(".","")
    answers[2] = answers[2].replace(".","")
    page_html = (grab_text(url_list).read())
    print("after reading url: "),
    print_time()
    soup = BeautifulSoup(page_html, 'html.parser')
    print("after html parser: "),
    print_time()
    html_fixed = (soup.prettify())
    print("after html cleaning up: "),
    print_time()

    print("\n\n\n")

    result_analysis_1(answers)
    
