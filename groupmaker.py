#! /usr/bin/env python3

"""
Author: Charlie Kapsiak    
Modified: 2021-01-19
Description: A simple script that takes as input a canvas grade export and makes groups of a certain size
            trying to distribute students with different profiencies across groups. 
""" 



import pandas as pd
import argparse
import re
import sys



def breakNum(num, max_size):
    approx_groups, remainder = divmod(num,max_size)
    if remainder == 0 :
        return [max_size] * approx_groups
    num_groups = approx_groups + 1
    ret = [0] * num_groups
    for x in range(num):
        ret[x % num_groups] += 1
    return ret

    


        

def removeBadRows(df, section = None):
    df = df[pd.notna(df["SIS User ID"])]
    if section:
        df = df[df["Section"].str.contains(section)]
    return df


def manualGrouping(df, disc, size):
    pref = "Group"
    counter = 1
    ret = {}
    df[disc] = df[disc].astype(float)
    df["STUDENT_RANK"] = df[disc].rank(method='first', na_option='bottom')
    for num in size:
        df["STUDENT_LOC"] =  pd.qcut(df["STUDENT_RANK"], num)
        grouped = df.groupby("STUDENT_LOC")
        samples = grouped.sample(n=1)["Student"];
        df = df.drop(samples.index)
        to_append = list(samples)
        ret[pref + str(counter)] = to_append
        counter += 1
    return pd.DataFrame({k: pd.Series(v) for k,v in ret.items()})


    

parser = argparse.ArgumentParser()
parser.add_argument("students",  type=str, nargs='+')
parser.add_argument("--section", "-c", type=str, default=None)
parser.add_argument("--discriminant", "-d", type=str, default="Current Score")
parser.add_argument("--groupsize", "-g", type=int, default=4)

args = parser.parse_args()

students = None


try:
    students = [pd.read_csv(x, sep=",") for x in args.students]
    students = pd.concat(students)
except Exception as e:
    print("Could not load file due to {}".format(e))



students = removeBadRows(students, args.section)
groups = manualGrouping(students, args.discriminant , breakNum(students.shape[0], args.groupsize))

groups.to_csv(sys.stdout,index=False)

