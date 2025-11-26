from flask import Flask, redirect, url_for, render_template, request
import numpy as np
from functions import *


app = Flask(__name__)
title = ""
response_items = []
questions = []
frequencies = []
total_respondents = 0
list_of_requencies = []
q_and_frequencies = {}
q_and_tweights = {}
ranks = {}
means = {}
overall_mean = 0
medians = {}
    

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/goto_part1',methods = ['POST','GET'])
def  goto_part1():
    return render_template('part1.html')

@app.route('/goto_part2',methods = ['POST','GET'])
def  goto_part2():
    global title
    global response_items
    title = request.form['title']
    response_items =  request.form.getlist('question')
    print(title)
    print(response_items)
    return render_template('part2.html',items = response_items)


@app.route('/goto_part3', methods = ['POST', 'GET'])
def goto_part3():
    global questions
    global frequencies
    global list_of_requencies
    global q_and_frequencies
    global total_respondents

    questions = request.form.getlist('question')
    frequencies = list(map(int,request.form.getlist('num')))


    list_of_requencies = to_list_of_lists(np.array(frequencies), response_items)


    q_and_frequencies = {}

    for i in range(len(questions)):
        q_and_frequencies[questions[i]] = list_of_requencies[i]

    
    print(title)
    print(response_items)
    print(questions)
    print(frequencies)
    print(type(frequencies[0]))
    print(list_of_requencies)
    print(q_and_frequencies)
    return render_template('part3.html', title = title, response_items = response_items, q_and_f = q_and_frequencies)

@app.route('/return_part2', methods = ['POST', 'GET'])
def return_part2():
    return render_template('part2.html', items = response_items)

@app.route('/goto_part4', methods = ['POST', 'GET'])
def goto_part4():
    global questions
    global total_respondents
    global q_and_tweights
    global q_and_frequencies
    global ranks
    global means
    global overall_mean

    for q in q_and_frequencies:
        weights = []

        index = 1
        for f in q_and_frequencies[q]:
            weights.append(f * index)
            index += 1
        q_and_tweights[q] = sum(weights)
            
    total_respondents = sum(frequencies) / len(questions)

    print(q_and_tweights)

    # Sort the questions : weights in descending order
    q_and_tweights = dict(sorted(q_and_tweights.items(), key=lambda x:x[1], reverse = True))


    means = getMean(q_and_frequencies, q_and_tweights)

    prev_weight = None
    prev_rank = None
    rank = 1
    for q in q_and_tweights:
        # get the weight, since q_and_tweights are alr sorted ASC
        weight = q_and_tweights[q]

        # utilize the previous weight to compare if they have the same weight
        #   if different weight from prev weight, assign new rank
        if weight != prev_weight:
            ranks[weight] = rank
            prev_rank = rank
        prev_weight = weight

        # increment the rank always even if there are 2 Questions with same mean
        rank += 1



    for q in means:
        overall_mean += means[q]

    overall_mean = round(overall_mean, 2)

    print(q_and_frequencies)
    print(q_and_tweights)
    print(means)
    print(medians)
    return render_template('part4.html', 
                           title = title, total_questions = len(questions), 
                           total_items = len(response_items), 
                           total_respondents = total_respondents, 
                           response_items = response_items, 
                           q_and_f = q_and_frequencies, 
                           tweight = q_and_tweights, 
                           ranks = ranks, 
                           means = means, 
                           overall_mean = overall_mean, 
                           questions = questions,
                           )


if __name__ == '__main__':
    app.run(debug = True)