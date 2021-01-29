#!/usr/bin/env python3

import pandas as pd
import sys
import numpy as np



if len(sys.argv) > 3:
    student_file = pd.concat([pd.read_csv(x) for x  in sys.argv[1:-1]])
    attendance = pd.read_csv(sys.argv[-1])
else:
    student_file = pd.read_csv(sys.argv[1])
    attendance = pd.read_csv(sys.argv[-1])

student_file = student_file[pd.notna(student_file["SIS User ID"])]

missing = np.setdiff1d(list(student_file["SIS Login ID"]),list( attendance["User Email"]))
student_file = student_file.set_index("SIS Login ID")
students_missing = student_file.loc[missing,"Student"]
print(f"Found {len(missing)} missing students")
for i in students_missing:
    print("  - ", i)



