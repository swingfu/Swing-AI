from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks

input = 'I like movies, but I think this one is just so-so.'
semantic_fun = pipeline(Tasks.text_classification,'damo/nlp_bert_sentiment-analysis_english-base')
result = semantic_fun(input)

print(result)
