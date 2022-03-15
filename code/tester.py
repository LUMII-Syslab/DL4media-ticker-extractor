from . video import Video
from . tesseract import TesseractOCR
import tsv
from . slidingreader import read_tickers
from . stringmetrics import similarity_metric, accuracy, split_words, edit_distance_with_errors
from . storyops import concatenate_news_stories
import random

def do_test(video_paths, truth_paths, **parameters):
    """
    Runs full pipeline on videos, compares them to truth.
    Returns dictionary of different metrics.
      ''
    
    videos - list of paths to videos.
    truths - list of paths to tsv files with ground truth.
    parameters - parameters of pipeline.
    """

    res = {}
    
    outputs = []
    truths = []
    
    res['outputs'] = []
    res['inputs'] = []
    
    for idx, video_path in enumerate(video_paths):
        print('Reading video ' + video_path)
        video = Video(video_path, TesseractOCR())
        output_stories = read_tickers(video, **parameters)
        truth_stories = tsv.read(truth_paths[idx])
        
        outputs.append(concatenate_news_stories(output_stories[0], char = ' '))
        name = 'random\\' + str(random.randint(0, 1000000000)) + '.txt'
        print('Output written to ' + name)
        res['outputs'].append(name)
        res['inputs'].append(video_path)
        f = open(name, 'w', encoding = 'utf8')
        f.write(outputs[-1])
        f.close()
        truths.append(concatenate_news_stories(truth_stories, char = ' '))
        #print('HZ')
        #print(outputs[-1])
        #print('RZ')
        #print(truths[-1])
        
    res['lengths'] = []
    res['length'] = 0
    res['word_lengths'] = []
    res['word_length'] = 0
    
    res['similarity_metric'] = []
    res['similarity_metric_weighted'] = 0
    res['similarity_metric_unweighted'] = 0
    
    res['character_accuracy'] = []
    res['character_accuracy_weighted'] = 0
    res['character_accuracy_unweighted'] = 0
    
    res['character_insertion'] = 0
    res['character_substitution'] = 0
    res['character_deletion'] = 0
    res['character_insertions'] = []
    res['character_substitutions'] = []
    res['character_deletions'] = []

    res['character_insertion_weighted'] = 0
    res['character_substitution_weighted'] = 0
    res['character_deletion_weighted'] = 0
    res['character_insertion_unweighted'] = 0
    res['character_substitution_unweighted'] = 0
    res['character_deletion_unweighted'] = 0
    
    res['word_accuracy'] = []
    res['word_accuracy_weighted'] = 0
    res['word_accuracy_unweighted'] = 0
    
    res['word_insertion'] = 0
    res['word_substitution'] = 0
    res['word_deletion'] = 0
    res['word_insertions'] = []
    res['word_substitutions'] = []
    res['word_deletions'] = []

    res['word_insertion_weighted'] = 0
    res['word_substitution_weighted'] = 0
    res['word_deletion_weighted'] = 0
    res['word_insertion_unweighted'] = 0
    res['word_substitution_unweighted'] = 0
    res['word_deletion_unweighted'] = 0
    
    weight = 0
    unweighted = 0
    weighted = 0
    for idx in range(len(outputs)):
        HZ = outputs[idx]
        RZ = truths[idx]
        res['lengths'].append(len(RZ))
        
        HZw = split_words(HZ)
        RZw = split_words(RZ)
        res['word_lengths'].append(len(RZw))

        m = similarity_metric(HZ, RZ)
        res['similarity_metric'].append(m)
        
        m = edit_distance_with_errors(HZ, RZ)
        #m = accuracy(HZ, RZ)
        res['character_accuracy'].append(m['accuracy'])
        
        res['character_insertions'].append(m['insertions'])
        res['character_substitutions'].append(m['substitutions'])
        res['character_deletions'].append(m['deletions'])
        
        m = edit_distance_with_errors(HZw, RZw)
        res['word_accuracy'].append(m['accuracy'])

        res['word_insertions'].append(m['insertions'])
        res['word_substitutions'].append(m['substitutions'])
        res['word_deletions'].append(m['deletions'])

    res['length'] = sum(res['lengths'])
    res['word_length'] = sum(res['word_lengths'])
    
    def average(values, weights = None):
        if weights is None:
          weights = [1 for val in values]
        cumulative = 0
        mass = 0
        for i, w in enumerate(weights):
            cumulative += values[i] * w
            mass+= w
        return cumulative / mass
            
    def normalize(values, divisors):
      return [val / divisors[i] for i, val in enumerate(values)]
            
    
    res['similarity_metric_weighted'] = average(res['similarity_metric'], res['lengths'])
    res['similarity_metric_unweighted'] = average(res['similarity_metric'])
    
    res['character_accuracy_weighted'] = average(res['character_accuracy'], res['lengths'])
    res['character_accuracy_unweighted'] = average(res['character_accuracy'])
    
    res['character_insertion'] = sum(res['character_insertions'])
    res['character_substitution'] = sum(res['character_substitutions'])
    res['character_deletion'] = sum(res['character_deletions'])
    
    res['character_insertions_norm'] = normalize(res['character_insertions'], res['lengths'])
    res['character_insertion_weighted'] = average(res['character_insertions_norm'], res['lengths'])
    res['character_insertion_unweighted'] = average(res['character_insertions_norm'])
    res['character_substitutions_norm'] = normalize(res['character_substitutions'], res['lengths'])
    res['character_substitution_weighted'] = average(res['character_substitutions_norm'], res['lengths'])
    res['character_substitution_unweighted'] = average(res['character_substitutions_norm'])
    res['character_deletions_norm'] = normalize(res['character_deletions'], res['lengths'])
    res['character_deletion_weighted'] = average(res['character_deletions_norm'], res['lengths'])
    res['character_deletion_unweighted'] = average(res['character_deletions_norm'])
    
    res['word_accuracy_weighted'] = average(res['word_accuracy'], res['word_lengths'])
    res['word_accuracy_unweighted'] = average(res['word_accuracy'])
    
    res['word_insertion'] = sum(res['word_insertions'])
    res['word_substitution'] = sum(res['word_substitutions'])
    res['word_deletion'] = sum(res['word_deletions'])
    
    res['word_insertions_norm'] = normalize(res['word_insertions'], res['word_lengths'])
    res['word_insertion_weighted'] = average(res['word_insertions_norm'], res['word_lengths'])
    res['word_insertion_unweighted'] = average(res['word_insertions_norm'])
    res['word_substitutions_norm'] = normalize(res['word_substitutions'], res['word_lengths'])
    res['word_substitution_weighted'] = average(res['word_substitutions_norm'], res['word_lengths'])
    res['word_substitution_unweighted'] = average(res['word_substitutions_norm'])
    res['word_deletions_norm'] = normalize(res['word_deletions'], res['word_lengths'])
    res['word_deletion_weighted'] = average(res['word_deletions_norm'], res['word_lengths'])
    res['word_deletion_unweighted'] = average(res['word_deletions_norm'])
    
    return res