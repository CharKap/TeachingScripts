#! /usr/bin/env python3


"""
Author: Charlie Kapsiak    
Modified: 2021-01-19
Description: Take an input csv where the header rows are group names and the columns represent groups and convert it
            into a form suitable for upload to zoom for breakout rooms
            
""" 


import pandas as pd
import argparse
import re
import sys

def getStudentEmailExact(student_name, students):
    temp = students[students["Student"] == student_name]
    return temp.iloc[0]["SIS Login ID"]

def getStudentEmailRough(student_name, students):
    parts = student_name.split(" ")
    first = parts[0]
    last = None
    narrowed = students[students["First Name"].str.startswith(first)]
    if len(parts) > 1:
        last = parts[1]
        narrowed = narrowed[narrowed["Last Name"].str.startswith(last)]

    if len(narrowed) == 0 :
        print(f"Name not found: {student_name}")
        raise Exception
    elif len(narrowed) > 1:
        print(f"Not unique name: {student_name}")
        print(f"Found several students with the name {student_name}.")
        for x in narrowed['Last Name']:
            print(x)
        raise Exception
    return narrowed.iloc[0]["SIS Login ID"]

def getStudentEmail(student_name, students):
    if ',' in student_name:
        return getStudentEmailExact(student_name,students)
    else:
        return getStudentEmailRough(student_name,students)


    

parser = argparse.ArgumentParser()
parser.add_argument("--students", "-s",  type=str, nargs='+')
parser.add_argument("--groups", "-g", type=str, nargs="*")

args = parser.parse_args()



students = [pd.read_csv(x, sep=",") for x in args.students]
students = pd.concat(students)

groups=None

if args.groups:
    groups = [pd.read_csv(x) for x in args.groups]
    groups = pd.concat(groups)
else:
    groups = pd.read_csv(sys.stdin)




for column in groups.columns:
    group = groups.loc[:, column]

rows = [
    [(column, getStudentEmail(name, students)) for name in groups.loc[:, column] if type(name) == str]
    for column in groups.columns
]


rows = [x for y in rows for x in y]

outdata = {"Pre-assign Room Name": [], "Email Address": []}
for x,y in rows:
    outdata["Pre-assign Room Name"].append(x)
    outdata["Email Address"].append(y)


out = pd.DataFrame(outdata)
out.to_csv(sys.stdout,index=False)

