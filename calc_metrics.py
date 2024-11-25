
# compute corresponding metrics to each task type

from rouge_score import rouge_scorer
# ref: https://thepythoncode.com/article/calculate-rouge-score-in-python#rouge-l

import pandas as pd

data = pd.read_csv('FinLaw_Evaluations.csv')

scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)

metric_df = pd.DataFrame({
    'Task:' : data['Task:'], # Use the first column of the original DataFrame
})
# copy the LLM columns with values 0
for i in range(len(data.columns)-4): # 4 is the number of columns left to LLM columns
    col_name = data.columns[i]
    metric_df[col_name] = 0

for i in range(len(data)): # iterate over rows
    
    # check the task type
    task_type = data.loc[i, 'Task:']
    # .loc[] accesses by label (first index can be an integer if the index is default)

    reference = data.loc[i, 'Golden Answer:']

    if "1-1" in task_type: # task 1-1 uses Rouge-L
        for j in range(4, len(data.columns)): # iterate each LLM output
            score = scorer.scorer(reference, data.iloc[i, j])
            # score is a dictionary {'rougeL' : Score(precision=0.625, recall=0.555, fmeasure=0.583)}
            
            metric_df.iloc[i,j-4+1] = score['rougeL'].precision
            # store the precision

    elif "1-2" in task_type: # task 1-2 uses accuracy
        # accuracy is an exact match. e.g. answer 'B', prediction 'B'
        for j in range(4, len(data.columns)): # iterate each LLM output
            if reference == data.iloc[i, j]:
                metric_df.iloc[im j-4+1] = 1
            else:
                metric_df.iloc[im j-4+1] = 0

    elif "2-1" in task_type: # task 2-1 uses F0.5
        for j in range(4, len(data.columns)): # iterate each LLM output
