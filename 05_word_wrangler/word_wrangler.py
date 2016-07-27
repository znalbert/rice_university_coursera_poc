"""
Student code for Word Wrangler game
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    uniques = []

    for dummy_idx in list1:
        if dummy_idx not in uniques:
            uniques.append(dummy_idx)

    return uniques

def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    intersection = []

    for dummy_idx in list1:
        if dummy_idx in list2 and dummy_idx not in intersection:
            intersection.append(dummy_idx)

    return intersection

# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing those elements that are in
    either list1 or list2.

    This function can be iterative.
    """
    merged = []
    l1_copy = list(list1)
    l2_copy = list(list2)

    if len(list1) == 0 or len(list2) == 0:
        return list1 + list2

    while len(l1_copy) > 0 and len(l2_copy) > 0:
        if l1_copy[0] == l2_copy[0]:
            merged.append(l1_copy.pop(0))
            merged.append(l2_copy.pop(0))
        elif l1_copy[0] < l2_copy[0]:
            merged.append(l1_copy.pop(0))
        else:
            merged.append(l2_copy.pop(0))

    merged = merged + l1_copy + l2_copy

    return merged

def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """

    half = len(list1)/2

    if len(list1) == 0 or len(list1) == 1:
        return list1
    else:
        return merge(merge_sort(list1[0: half]), merge_sort(list1[half:]))


# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    if len(word) == 0:
        return [""]

    # step 1
    first = word[0]
    rest = word[1:]

    # step 2
    rest_strings = gen_all_strings(rest)

    # step 3
    strings = list(rest_strings)

    for string in strings:
        for position in range(len(string)):
            new_string = string[:position] + first + string[position:]
            rest_strings.append(new_string)
        rest_strings.append(string + first)
    return rest_strings


# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    return []

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates,
                                     intersect, merge_sort,
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
# run()


    
