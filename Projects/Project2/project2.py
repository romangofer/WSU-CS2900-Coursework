import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import scipy.stats

# Data Ingestion

## Merge the Data Set

df1 = pd.read_csv("data/id-hw-exams.csv", converters={"SID": str.lower})
df2 = pd.read_csv("data/id-section.csv", converters = {"Email Address": str.lower, "NetID": str.lower} )

merged_set= pd.merge(df1, df2, left_on = 'SID', right_on = 'NetID')


cleaned_set = merged_set.drop(columns = ['NetID'])



## Drop the Timestamp Columns for Homeworks and Exams

timestamps = cleaned_set.filter(regex=r"\W*(Submission)\W*", axis=1)



cleaned_set = cleaned_set.drop(timestamps, axis = 1)

cleaned_set = cleaned_set.fillna(0)



# Data Prep

## Calculate the score each user received on each homework and store the result in a new column

for num in range (1,11):
    cleaned_set[f'hw{num}_score'] = ((cleaned_set[f'Homework {num}'] / cleaned_set[f'Homework {num} - Max Points'])*100)

for num in range (1,4):
    cleaned_set[f'exam{num}_score'] = ((cleaned_set[f'Exam {num}'] / cleaned_set[f'Exam {num} - Max Points'])*100)

homework_scores = cleaned_set.filter(regex=r"^hw", axis=1)



## Calculate the homework and exam averages for each user and store the results in new columns

cleaned_set['hw_avg'] = homework_scores.mean(axis=1)

exam_scores = cleaned_set.filter(regex=r"^ex", axis=1)

cleaned_set['ex_avg'] = exam_scores.mean(axis=1)

## Calculate each user's final grade for the class and store it in a new column

cleaned_set['final_score'] = (cleaned_set['hw_avg'] * .6) + (cleaned_set['ex_avg'] * .4)

## Filter out and remove the points awarded and max points columns
  
homework_nums = cleaned_set.filter(regex=r"(\W*Homework\W*)", axis=1)



cleaned_set = cleaned_set.drop(homework_nums, axis = 1)



exam_cols_to_drop = cleaned_set.filter(regex=r"(\W*Exam\W*)", axis=1)



cleaned_set = cleaned_set.drop(exam_cols_to_drop, axis = 1 )



# Generate a report for each homework assignment and exam

for num in range (1,11):
      print(f'Homework {num}:')
      print('Lowest Score: ', cleaned_set[f'hw{num}_score'].min())
      print('Highest Score: ', cleaned_set[f'hw{num}_score'].max())
      print('Average Score: ', cleaned_set[f'hw{num}_score'].mean())
      print('Standard Deviation from Average: ', cleaned_set[f'hw{num}_score'].std())

for num in range (1,4):
    print(f'Exam {num}:')
    print('Lowest Score:', cleaned_set[f'exam{num}_score'].min())
    print('Highest Score:', cleaned_set[f'exam{num}_score'].max())
    print('Average Score:', cleaned_set[f'exam{num}_score'].mean())
    print('Standard Deviation from Average:', cleaned_set[f'exam{num}_score'].std())

# Extra Credit 1 - Calculating Letter Grades Based on Final Grades

## Round up the final_score numbers and put them in a column called "ceiling_score"

cleaned_set["ceiling_score"] = np.ceil(cleaned_set["final_score"])

## Define the ranges of grades that go with each letter

grades = {
    90: "A",
    80: "B",
    70: "C",
    60: "D",
    0: "F",
}

## Function that takes the values in the "ceiling_score" column and compares them with the keys in the grades dictionary to determine
## which letter to assign to each ceiling grade value

def grade_mapping(value):
    for key, letter in grades.items():
        if value >= key:
            return letter

## Create a new Series called letter_grades by mapping grade_mapping() onto the "ceiling_score" column from cleaned_set

letter_grades = cleaned_set["ceiling_score"].map(grade_mapping)

## After mapping, create a categorical Pandas column

cleaned_set["final_letter_grade"] = pd.Categorical(
    letter_grades, categories=grades.values(), ordered=True
)


# Find how many students in each section who received what letter grade

grade_occurrences = cleaned_set.groupby('Section')['final_letter_grade'].value_counts()
print(grade_occurrences)


# Calculate and output the correlation between homework grades and final grades

hw_and_final_grade_corr = cleaned_set['hw_avg'].corr(cleaned_set['final_score'])
print(hw_and_final_grade_corr)

# Calculate and output the correlation between exam grades and final grades

exam_and_final_grade_corr = cleaned_set['ex_avg'].corr(cleaned_set['final_score'])
print(exam_and_final_grade_corr)

# Extra Credit 2 - Generate a visualization for the summary statistics of the data 


converted = cleaned_set["final_score"]/100

converted.plot.hist(bins=20, label="Histogram")

converted.plot.density(
    linewidth=4, label="Kernel Density Estimate"
)

final_mean = converted.mean()
final_std = converted.std()
x = np.linspace(final_mean - 5 * final_std, final_mean + 5 * final_std, 200)
normal_dist = scipy.stats.norm.pdf(x, loc=final_mean, scale=final_std)
plt.title('Final Grade Distribution')
plt.xlabel('Grade (in decimal form, so 0.9 = 90%)')
plt.plot(x, normal_dist, label="Normal Distribution", linewidth=4)
plt.legend()
plt.show()




