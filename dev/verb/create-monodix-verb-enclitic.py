#!/usr/bin/python2.6
# coding=utf-8
# -*- encoding: utf-8 -*-

import os
import sys
import MySQLdb
import re
import pdb
import codecs
from pprint import pprint

# these are kept here for comatibility, will remove that soon, please try to use BnChars dictionary
V = u'[অআইঈউঊঋএঐওঔ]'
C = u'[কখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহৎড়ঢ়য়]'
K = u'[ািীুূৃেৈোৌ]'
N = u'[০১২৩৪৫৬৭৮৯]'
M = u'[ঁংঃ]'
H = u'[্]'

animacy_table = {'0': 'nn', '1': 'aa', '2': 'hu', '3': 'el'}
gender_table = {'0': 'mf', '1': 'm', '2': 'f', '3': 'nt'}

BnChars = {'vowel': u'[অআইঈউঊঋএঐওঔ]',
	   'consonant_real': u'[কখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহৎড়ঢ়য়]',
	   'marker': u'[ািীুূৃেৈোৌ]',
	   'number': u'[০১২৩৪৫৬৭৮৯]',
	   'misc': u'[ঁংঃ]',
	   
	   'hasant': u'[্]',
	   'anusvara': u'[ং]',
	   'chandrabindu': u'[ঁ]',
	   'visarga': u'[ঃ]',
	   
	   'consonant': u'[কখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহৎড়ঢ়য়' + u'ংঃ' + u'্]'}

# be careful here, the ordering is really very important, we'll use this tuple in the zip fuction to
# create a dictionary
forms = ('inf',
	 'gen',
	 'ger',
	 
	 'pres_smpl_p1',
	 'pres_smpl_p2_pol', 'pres_smpl_p2_fam', 'pres_smpl_p2_infml',
	 'pres_smpl_p3_pol', 'pres_smpl_p3_infml',
	 'pres_smpl_impers',
	 
	 'pres_cnt_p1',
	 'pres_cnt_p2_pol', 'pres_cnt_p2_fam', 'pres_cnt_p2_infml',
	 'pres_cnt_p3_pol', 'pres_cnt_p3_infml',
	 'pres_cnt_impers',
	 
	 'past_smpl_p1',
	 'past_smpl_p2_pol', 'past_smpl_p2_fam', 'past_smpl_p2_infml',
	 'past_smpl_p3_pol', 'past_smpl_p3_infml',
	 'past_smpl_impers',
	 
	 'past_cnt_p1',
	 'past_cnt_p2_pol', 'past_cnt_p2_fam', 'past_cnt_p2_infml',
	 'past_cnt_p3_pol', 'past_cnt_p3_infml',
	 'past_cnt_impers',
	 
	 'past_hbtl_p1',
	 'past_hbtl_p2_pol', 'past_hbtl_p2_fam', 'past_hbtl_p2_infml',
	 'past_hbtl_p3_pol', 'past_hbtl_p3_infml',
	 'past_hbtl_impers',
	 
	 'ft_smpl_p1',
	 'ft_smpl_p2_pol', 'ft_smpl_p2_fam', 'ft_smpl_p2_infml',
	 'ft_smpl_p3_pol', 'ft_smpl_p3_infml',
	 'ft_smpl_impers',
	 
	 'ft_cnt_p1',
	 'ft_cnt_p2_pol', 'ft_cnt_p2_fam', 'ft_cnt_p2_infml',
	 'ft_cnt_p3_pol', 'ft_cnt_p3_infml',
	 'ft_cnt_impers',
	 
	 'prft_p1',
	 'prft_p2_pol', 'prft_p2_fam', 'prft_p2_infml',
	 'prft_p3_pol', 'prft_p3_infml',
	 'prft_impers',
	 
	 'plprft_p1',
	 'plprft_p2_pol', 'plprft_p2_fam', 'plprft_p2_infml',
	 'plprft_p3_pol', 'plprft_p3_infml',
	 'plprft_impers',
	 
	 'ppst',
	 'pcnd',
	 
	 'pres_imp_p2_pol', 'pres_imp_p2_fam', 'pres_imp_p2_infml',
	 'pres_imp_p3_pol', 'pres_imp_p3_infml',
	 'pres_imp_impers',
	 
	 'ft_imp_p2_pol', 'ft_imp_p2_fam', 'ft_imp_p2_infml',
	 'ft_imp_p3_pol', 'ft_imp_p3_infml',
	 'ft_imp_impers',
	 )

tags = {}
''' create tags for the xml '''
for form in forms:
    symbol_tags = '<s n=\"vblex\"/>'
    for s in form.split('_'):
        symbol_tags +=  '<s n=\"' + s + '\"/>'
    tags[form] = symbol_tags
    
    
speling_tags = {}
''' create tag for the speling format '''
for form in forms:
    symbol_tags = form.replace('_', '.')
    speling_tags[form] = symbol_tags

    
#pprint(tags)

DEBUG = False

def dprint(str):
    if DEBUG == True:
	print "DEBUG: " + str
	
def get_sym(list):
    sym = ''
    for e in list:
        sym = sym + '<s n=\"' + e + '\"/>'
    return sym

def get_num(data):
    if data == 'sd': return "<s n=\"sg\"/>", "<s n=\"def\"/>"
    else: return "<s n=\"" + data + "\"/>", None
    
enclitic = """    <pardef n="enclitic">
      <!-- passthrough -->
      <e>
        <p>
          <l></l>
          <r></r>
        </p>
      </e>
      <!-- ই -->
      <e>
        <p>
          <l>ই</l>
          <r><j/>ই<s n="adv"/></r>
        </p>
      </e>
      <!-- ও -->
      <e>
        <p>
          <l>ও</l>
          <r><j/>ও<s n="adv"/></r>
        </p>
      </e>
    </pardef>"""
    
def find_longest_common_substring(a, b):
    candidate = ''
    length = len(a.decode('utf-8'))
    for char in a.decode('utf-8'):
        candidate = candidate + char
        if b.find(candidate.encode('utf-8')) == -1:
            return candidate[0:len(candidate)-1]
    return candidate

def find_longest_common_substring_from_list(list):
    ''' Longest common substring for a given list '''
    a = list[0]
    for b in list[1:]:
        a = find_longest_common_substring(a, b)
    return a
    
def append_real_verbs(cursor, sql, single_word_verbs):
    ''' Splits the REAL verbs from the compund verbs and adds them to the single_word_verbs list '''
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
	verb, = row
	real_verb = verb.split(' ')[-1]
	if real_verb != None and real_verb != '\n' and real_verb not in single_word_verbs:
	    single_word_verbs.append(real_verb)

def string_length_compare(a, b):
    ''' comparison function that can be fed to a sort function '''
    if len(a) == len(b): 
        return 0;
    if len(a) > len(b): 
	return 1;
    return -1;

def get_inflection_do(verb, effective_length):
    ''' XCK as in করা/পড়া/নাড়া
	Note: 1. we need to decive some rule for verbs like ওলটা  that is a derived form of উলটা, or ঝোলা - ঝুলা, গোছা - গুছা
	we'll do this in deeper steps of pipeline
	
	only perfect, pluperfect and past participle will need an alternate umlut,
	So, করা - করিয়ে, ঝোলা - ঝুলিয়ে, ফেরা - ফিরিয়ে, ওলটা - উলটিয়ে but বেড়া - বেড়িয়ে because বেড়া is not a derived verb, so we need a fiter for that
    '''
    special = False
    special_verbs = ('বেরা', 'বেড়া', 'দেখা', 'চেঁচা')
    length = effective_length
    #length = len(verb.replace(u'ঁ', u'').replace(u'্', u'').decode('utf-8'))
	
    # create the basic umlaut
    # replace the ending 'া ' with a 'ি', there will no chnadrabindu in the end, surely
    umlaut = re.sub(u'া$', 'ি', verb)
    
    # check if the verb is reagular i.e. not a derived verb, if so, we'll have no special umlaut calculated
    if verb not in special_verbs:
	# verb is a derived one, so further proces the umlaut
	if length < 5:
	    # to make sure we are not stepping into the wrong syllable :)
	    
	    # ওঠা - উঠা, ওলটা - উলটা
	    umlaut = re.sub(u'^ও', u'উ', umlaut)
	    
	# ঝোলা - ঝুলা, গোছা - গুছা, there could be chandrabindu, so be careful
	p = re.compile(u'(ো)(ঁ?' + BnChars['consonant_real'] + BnChars['marker'] + ')$')
	#p = re.compile(u'(ো)(\w{2})$', re.UNICODE | re.LOCALE)
	umlaut = p.sub(u'ু\g<2>', umlaut)
	
	# ফেরা - ফিরা, there could be chandrabindu, so be careful
	p = re.compile(u'(ে)(ঁ?' + BnChars['consonant_real'] + BnChars['marker'] + ')$')
	umlaut = p.sub(u'ি\g<2>', umlaut)
	
    # here in this stage we have a working verb stem and an alternate umlaut, lets go down to bussiness
    if DEBUG == True:
	print verb, umlaut
    
    inflections = ( verb + u'তে',
		    verb + u'নোর',
		    verb + u'নো',
		    verb + u'ই',  verb + u'ন', verb + u'ও', verb + u'স',  verb + u'ন', verb + u'য়',  verb + u'য়',
		    verb + u'চ্ছি',  verb + u'চ্ছেন', verb + u'চ্ছ', verb + u'চ্ছিস',  verb + u'চ্ছেন', verb + u'চ্ছে',  verb + u'চ্ছে',
		    verb + u'লাম',  verb + u'লেন', verb + u'লে', verb + u'লি',  verb + u'লেন', verb + u'ল',  verb + u'ল',
		    verb + u'চ্ছিলাম',  verb + u'চ্ছিলেন', verb + u'চ্ছিলে', verb + u'চ্ছিলি',  verb + u'চ্ছিলেন', verb + u'চ্ছিল',  verb + u'চ্ছিল',
		    verb + u'তাম',  verb + u'তেন', verb + u'তে', verb + u'তি',  verb + u'তেন', verb + u'ত',  verb + u'ত',
		    verb + u'ব',  verb + u'বেন', verb + u'বে', verb + u'বি',  verb + u'বেন', verb + u'বে',  verb + u'বে',
		    verb + u'তে থাকব',  verb + u'তে থাকবেন', verb + u'তে থাকবে', verb + u'তে থাকবি',  verb + u'তে থাকবেন', verb + u'তে থাকবে',  verb + u'তে থাকবে',
		    umlaut + u'য়েছি',  umlaut + u'য়েছেন', umlaut + u'য়েছ', umlaut + u'য়েছিস',  umlaut + u'য়েছেন', umlaut + u'য়েছে',  umlaut + u'য়েছে',
		    umlaut + u'য়েছিলাম',  umlaut + u'য়েছিলেন', umlaut + u'য়েছিলে', umlaut + u'য়েছিলি',  umlaut + u'য়েছিলেন', umlaut + u'য়েছিল',  umlaut + u'য়েছিল',		    
		    umlaut + u'য়ে',
		    verb + u'লে',		    
		    verb + u'ন', verb + u'ও', verb, verb + u'ন', verb + u'ক', verb + u'ক',
		    verb + u'বেন', verb + u'বে', verb + u'বি',  verb + u'বে', verb + u'বি', verb + u'বি' 
		   )
    inflections = dict(zip(forms, inflections))
    
    return inflections

def get_inflection_write(verb, effective_length):
    ''' েK as in লেখ, NOTE: some of these verbs has an internal umlaut like লেখ -> লিখ while others have no
	such umlaut such as খেল, ফেল  we need to process them as regular verbs, so a further pipeline is needed
    '''
    special = False
    
    # There should be two types groups, one is for ে based special verbs and the other
    # for ো based special verbs, just append those here in this list, we'll try to
    # keep them and mark them in database later, right now this will suffice
    special_verbs = ('ফেল', 'খেল', 'দেখ')
    
    umlaut = verb
    
    # creation of umlaut for verbs like শোন, চেন than are not flagged as special
    if verb not in special_verbs:
	# verb is a derived one, so further proces the umlaut
	
	# শোন - শুন
	# notice in the regex that its consonant NOT consonant_real because there is no marker afterwards
	p = re.compile(u'(ো)(ঁ?' + BnChars['consonant'] + ')$')
	# this does not work, unfortunatly, otherwise things could have been a lot easier
	# p = re.compile(u'(ো)(\w{2})$', re.UNICODE | re.LOCALE)
	umlaut = p.sub(u'ু\g<2>', umlaut)
	
	# চেন - চিন
	p = re.compile(u'(ে)(ঁ?' + BnChars['consonant'] + ')$')
	umlaut = p.sub(u'ি\g<2>', umlaut)
	
	# ওঠ - উঠে
	p = re.compile(u'(ও)(ঁ?' + BnChars['consonant'] + ')$')
	umlaut = p.sub(u'উ\g<2>', umlaut)
	
	# we don not have any two letter verbs starting with এ right now, if we get to see one
	# we'll insert the rule here
	

    # creation of basic umlaut for inflection like কাট - কেটে, ফাট - ফেটে, সাঁট - সেঁটে
    # I dont think this is needed here, however i'm not sure, as i have a very bad headache :(
    # umlaut = re.sub(u'(া)(ঁ?' + BnChars['consonant'] + ')$', u'ে\g<2>', umlaut)
    
    #inflections ={}
    
    inflections = ( umlaut + u'তে',
		    verb + u'ার',
		    verb + u'া',
		    umlaut + u'ি',  verb + u'েন', verb, umlaut + u'িস',  verb + u'েন', verb + u'ে',  verb + u'ে',
		    umlaut + u'ছি',  umlaut + u'ছেন', umlaut + u'ছ', umlaut + u'ছিস',  umlaut + u'ছেন', umlaut + u'ছে',  umlaut + u'ছে',
		    umlaut + u'লাম',  umlaut + u'লেন', umlaut + u'লে', umlaut + u'লি',  umlaut + u'লেন', umlaut + u'ল',  umlaut + u'ল',
		    umlaut + u'ছিলাম',  umlaut + u'ছিলেন', umlaut + u'ছিলে', umlaut + u'ছিলি',  umlaut + u'ছিলেন', umlaut + u'ছিল',  umlaut + u'ছিল',
		    umlaut + u'তাম',  umlaut + u'তেন', umlaut + u'তে', umlaut + u'তি',  umlaut + u'তেন', umlaut + u'ত',  umlaut + u'ত',
		    umlaut + u'ব',  umlaut + u'বেন', umlaut + u'বে', umlaut + u'বি',  umlaut + u'বেন', umlaut + u'বে',  umlaut + u'বে',
		    umlaut + u'তে থাকব',  umlaut + u'তে থাকবেন', umlaut + u'তে থাকবে', umlaut + u'তে থাকবি',  umlaut + u'তে থাকবেন', umlaut + u'তে থাকবে',  umlaut + u'তে থাকবে',
		    umlaut + u'েছি',  umlaut + u'েছেন', umlaut + u'েছ', umlaut + u'েছিস',  umlaut + u'েছেন', umlaut + u'েছে',  umlaut + u'েছে',
		    umlaut + u'েছিলাম',  umlaut + u'েছিলেন', umlaut + u'েছিলে', umlaut + u'েছিলি',  umlaut + u'েছিলেন', umlaut + u'েছিল', umlaut + u'েছিল',  umlaut + u'েছিল',					
		    umlaut + u'ে',
		    umlaut + u'লে',		    
		    umlaut + u'ুন', verb, umlaut,  umlaut + u'ুন', umlaut + u'ুক', umlaut + u'ুক',
		    umlaut + u'বেন', verb + u'ো', umlaut + u'িস',  umlaut + u'বেন', umlaut + u'বে', umlaut + u'বে'
		   )
    inflections = dict(zip(forms, inflections))
    
    if DEBUG == True:
	print verb, umlaut   
    
    return inflections

def get_inflection_shake(verb, effective_length):
    '''
	পাড় - পেড়ে, নাড়  - নেড়ে
    '''
    
    # special handling for verb আছ
    
    if verb == 'আছ':
	return get_inflection_be(verb, effective_length)
    
    special = False
    
    special_verbs = ('আছ', )
    
    umlaut = verb
    
    if verb not in special_verbs:
	# verb is a derived one, so further proces the umlaut
	
        # creation of basic umlaut for inflection like কাট - কেটে, ফাট - ফেটে, সাঁট - সেঁটে
	umlaut = re.sub(u'(া)(ঁ?' + BnChars['consonant'] + ')$', u'ে\g<2>', umlaut)
	
	# আস - এসে
	# notice in the regex that its consonant NOT consonant_real because there is no marker afterwards
	p = re.compile(u'(আ)(ঁ?' + BnChars['consonant'] + ')$')
	umlaut = p.sub(u'এ\g<2>', umlaut)
	    
    if DEBUG == True:    	
	print verb, umlaut
    
    # here comes the actual calculation for the forms
    inflections = ( verb + u'তে',
		    verb + u'ার',
		    verb + u'া',
		    verb + u'ি', verb + u'েন', verb, verb + u'িস', verb + u'েন', verb + u'ে', verb + u'ে',
		    verb + u'ছি', verb + u'ছেন', verb + u'ছ', verb + u'ছিস', verb + u'ছেন', verb + u'ছে', verb + u'ছে', 
		    verb + u'লাম',  verb + u'লেন', verb + u'লে', verb + u'লি',  verb + u'লেন', verb + u'ল',  verb + u'ল',
		    verb + u'ছিলাম', verb + u'ছিলেন', verb + u'ছিলে', verb + u'ছিলি', verb + u'ছিলেন', verb + u'ছিল', verb + u'ছিল',
		    verb + u'তাম', verb + u'তেন', verb + u'তে', verb + u'তি', verb + u'তেন', verb + u'ত', verb + u'ত',
		    verb + u'ব', verb + u'বেন', verb + u'বে', verb + u'বি', verb + u'বেন', verb + u'বে', verb + u'বে',
		    verb + u'তে থাকব', verb + u'তে থাকবেন', verb + u'তে থাকবে', verb + u'তে থাকবি', verb + u'তে থাকবেন', verb + u'তে থাকবে', verb + u'তে থাকবে',
		    umlaut + u'েছি', umlaut + u'েছেন', umlaut + u'েছ', umlaut + u'েছিস', umlaut + u'েছেন', umlaut + u'েছে', umlaut + u'েছে',
		    umlaut + u'েছিলাম', umlaut + u'েছিলেন', umlaut + u'েছিলে', umlaut + u'েছিলি', umlaut + u'েছিলেন', umlaut + u'েছিল', umlaut + u'েছিল', umlaut + u'েছিল',
		    umlaut + u'ে',
		    verb + u'লে',		    
		    verb + u'ুন', verb, verb, verb + u'ুন', verb + u'ুক', verb + u'ুক',
		    verb + u'বেন', umlaut + u'ো', verb + u'িস', verb + u'বেন', verb + u'বে', verb + u'বে'
		   )
    inflections = dict(zip(forms, inflections))
    
    return inflections

def get_inflection_be(verb, length):
    # special inflection case for verb আছ - be
    umlaut = u'থাক'
    umlaut2 = u'রই'
    
    inflections = {}
    if DEBUG == True:
	print verb
    
    inflections = ( umlaut + u'তে',
		    umlaut + u'ার',
		    umlaut + u'া',
		    verb + u'ি',  verb + u'েন', verb, verb + u'িস',  verb + u'েন', verb + u'ে',  verb + u'ে',
		    umlaut + u'ছি',  umlaut + u'ছেন', umlaut + u'ছ', umlaut + u'ছিস',  umlaut + u'ছেন', umlaut + u'ছে',  umlaut + u'ছে',
		    umlaut + u'লাম',  umlaut + u'লেন', umlaut + u'লে', umlaut + u'লি',  umlaut + u'লেন', umlaut + u'ল',  umlaut + u'ল',
		    umlaut + u'ছিলাম',  umlaut + u'ছিলেন', umlaut + u'ছিলে', umlaut + u'ছিলি',  umlaut + u'ছিলেন', umlaut + u'ছিল',  umlaut + u'ছিল',
		    umlaut + u'তাম',  umlaut + u'তেন', umlaut + u'তে', umlaut + u'তি',  umlaut + u'তেন', umlaut + u'ত',  umlaut + u'ত',
		    umlaut + u'ব',  umlaut + u'বেন', umlaut + u'বে', umlaut + u'বি',  umlaut + u'বেন', umlaut + u'বে',  umlaut + u'বে',
		    umlaut2 + u'তে থাকব',  umlaut2 + u'তে থাকবেন', umlaut2 + u'তে থাকবে', umlaut2 + u'তে থাকবি',  umlaut2 + u'তে থাকবেন', umlaut2 + u'তে থাকবে',  umlaut2 + u'তে থাকবে',
		    verb + u'ি',  verb + u'েন', verb, verb + u'িস',  verb + u'েন', verb + u'ে',  verb + u'ে',
		    u'ছিলাম',  u'ছিলেন', u'ছিলে', u'ছিলি', u'ছিলেন', u'ছিল', u'ছিল',
		    u'থেকে',
		    umlaut + u'লে',		    
		    umlaut + u'ুন', umlaut, umlaut, umlaut + u'ুন', umlaut + u'ুক', umlaut + u'ুক',
		    umlaut + u'বেন', u'থেকো', u'থাকিস',  umlaut + u'বেন', umlaut + u'বে', umlaut + u'বে' 		    
		   )
    inflections = dict(zip(forms, inflections))
    
    return inflections

def get_inflection_eat(verb, length):
    # খা - পা - শু, চি and ক, হ
    
    # this type of verbs will have an umlaut like খা - খেতে, পা - পেতে, while verbs
    # like শু - চি will remain the same
    umlaut = re.sub(u'(' + BnChars['consonant_real'] +  u')(া)(ঁ?)$', u'\g<1>ে\g<3>', verb)

    if DEBUG == True:
        print verb, umlaut
    
    inflections = {}
    
    # verb + u'বার'> verb + u'ওয়ার'
    inflections = ( umlaut + u'তে',
		    verb + u'ওয়ার',
		    verb + u'ওয়া',
		    verb + u'ই',  verb + u'ন', verb + u'ও', verb + u'স',  verb + u'ন', verb + u'য়',  verb + u'য়',
		    verb + u'চ্ছি',  verb + u'চ্ছেন', verb + u'চ্ছ', verb + u'চ্ছিস',  verb + u'চ্ছেন', verb + u'চ্ছে',  verb + u'চ্ছে',
		    umlaut + u'লাম',  umlaut + u'লেন', umlaut + u'লে', umlaut + u'লি',  umlaut + u'লেন', umlaut + u'ল',  umlaut + u'ল',
		    verb + u'চ্ছিলাম',  verb + u'চ্ছিলেন', verb + u'চ্ছিলে', verb + u'চ্ছিলি',  verb + u'চ্ছিলেন', verb + u'চ্ছিল',  verb + u'চ্ছিল',
		    umlaut + u'তাম' ,  umlaut + u'তেন', umlaut + u'তে', umlaut + u'তি',  umlaut + u'তেন', umlaut + u'ত',  umlaut + u'ত',
		    verb + u'ব',  verb + u'বেন', verb + u'বে', verb + u'বি',  verb + u'বেন', verb + u'বে',  verb + u'বে',
		    umlaut + u'তে থাকব',  umlaut + u'তে থাকবেন', umlaut + u'তে থাকবে', umlaut + u'তে থাকবি',  umlaut + u'তে থাকবেন', umlaut + u'তে থাকবে',  umlaut + u'তে থাকবে',
		    umlaut + u'য়েছি',  umlaut + u'য়েছেন', umlaut + u'য়েছ', umlaut + u'য়েছিস',  umlaut + u'য়েছেন', umlaut + u'য়েছে',  umlaut + u'য়েছে',
		    umlaut + u'য়েছিলাম',  umlaut + u'য়েছিলেন', umlaut + u'য়েছিলে', umlaut + u'য়েছিলি',  umlaut + u'য়েছিলেন', umlaut + u'য়েছিল',  umlaut + u'য়েছিল',		    
		    umlaut + u'য়ে',
		    umlaut + u'লে',		    
		    verb + u'ন', verb + u'ও', verb, verb + u'ন', verb + u'ক', verb + u'ক',
		    verb + u'বেন', umlaut + u'ও', verb + u'স',  verb + u'বেন', verb + u'বে', verb + u'বে'
		   )
    inflections = dict(zip(forms, inflections))
    
    
    return inflections
		
def get_inflection_go(verb, length):
    # special case for verb যা
    
    umlaut = 'যে'
    umlaut2 = 'গে'
    umlaut3 = 'গি'

    if DEBUG == True:    
	print verb, umlaut, umlaut2, umlaut3
    
    inflections = {}
    
    # need to add this alternate form or replace it
    # verb + u'বার'> verb + u'ওয়ার'
    # umlaut3 + u'য়েছি',  umlaut3 + u'য়েছেন', umlaut3 + u'য়েছ', umlaut3 + u'য়েছিস',  umlaut3 + u'য়েছেন', umlaut3 + u'য়েছে',  umlaut3 + u'য়েছে'
    # >>
    # umlaut2 + u'ছি',  umlaut2 + u'ছেন', umlaut2 + u'ছ', umlaut2 + u'ছিস',  umlaut2 + u'ছেন', umlaut2 + u'ছে',  umlaut2 + u'ছে'
    inflections = ( umlaut + u'তে',
		    verb + u'ওয়ার',
		    verb + u'ওয়া',
		    verb + u'ই',  verb + u'ন', verb + u'ও', verb + u'স',  verb + u'ন', verb + u'য়',  verb + u'য়',
		    verb + u'চ্ছি',  verb + u'চ্ছেন', verb + u'চ্ছ', verb + u'চ্ছিস',  verb + u'চ্ছেন', verb + u'চ্ছে',  verb + u'চ্ছে',
		    umlaut2 + u'লাম',  umlaut2 + u'লেন', umlaut2 + u'লে', umlaut2 + u'লি',  umlaut2 + u'লেন', umlaut2 + u'ল',  umlaut2 + u'ল',
		    verb + u'চ্ছিলাম',  verb + u'চ্ছিলেন', verb + u'চ্ছিলে', verb + u'চ্ছিলি',  verb + u'চ্ছিলেন', verb + u'চ্ছিল',  verb + u'চ্ছিল',
		    umlaut + u'তাম',  umlaut + u'তেন', umlaut + u'তে', umlaut + u'তি',  umlaut + u'তেন', umlaut + u'ত',  umlaut + u'ত',
		    verb + u'ব',  verb + u'বেন', verb + u'বে', verb + u'বি',  verb + u'বেন', verb + u'বে',  verb + u'বে',
		    umlaut + u'তে থাকব',  umlaut + u'তে থাকবেন', umlaut + u'তে থাকবে', umlaut + u'তে থাকবি',  umlaut + u'তে থাকবেন', umlaut + u'তে থাকবে',  umlaut + u'তে থাকবে',
		    umlaut2 + u'ছি',  umlaut2 + u'ছেন', umlaut2 + u'ছ', umlaut2 + u'ছিস',  umlaut2 + u'ছেন', umlaut2 + u'ছে',  umlaut2 + u'ছে',
		    umlaut3 + u'য়েছিলাম',  umlaut3 + u'য়েছিলেন', umlaut3 + u'য়েছিলে', umlaut3 + u'য়েছিলি',  umlaut3 + u'য়েছিলেন', umlaut3 + u'য়েছিল',  umlaut3 + u'য়েছিল',
		    umlaut3 + u'য়ে',
		    umlaut2 + u'লে',		    
		    verb + u'ন', verb + u'ও', verb, verb + u'ন', verb + u'ক', verb + u'ক',
		    verb + u'বেন', verb + u'বে', verb + u'বি',  verb + u'বেন', verb + u'বে', verb + u'বে' 		    
		   )
    inflections = dict(zip(forms, inflections))
        
    return inflections

def get_inflection_take(verb, length):
    # two type of verbs,
    # 1. নে - নিতে, দে - দিতে
    # 2. শো - শুতে, 
    
    # নে -নিতে
    umlaut = re.sub(u'(' + BnChars['consonant_real'] +  u')(ে)(ঁ?)$', u'\g<1>ি\g<3>', verb)
    # নে - নাও
    umlaut2 = re.sub(u'(' + BnChars['consonant_real'] +  u')(ে)(ঁ?)$', u'\g<1>া\g<3>', verb)
    
    # শো - শুতে
    # the source is here the previous umlaut, be careful to remember that :)
    umlaut = re.sub(u'(' + BnChars['consonant_real'] +  u')(ো)(ঁ?)$', u'\g<1>ু\g<3>', umlaut)
    
    if DEBUG == True:    
	print verb, umlaut, umlaut2
        
    #inflections = {}

    inflections = ( umlaut + u'তে',
		    verb + u'বার',
		    verb + u'ওয়া',
		    verb + u'ই',  verb + u'ন', umlaut2 + u'ও', umlaut + u'স',  verb + u'ন', verb + u'য়',  verb + u'য়',
		    umlaut + u'চ্ছি',  umlaut + u'চ্ছেন', umlaut + u'চ্ছ', umlaut + u'চ্ছিস',  umlaut + u'চ্ছেন', umlaut + u'চ্ছে',  umlaut + u'চ্ছে',
		    umlaut + u'লাম',  umlaut + u'লেন', umlaut + u'লে', umlaut + u'লি',  umlaut + u'লেন', umlaut + u'ল',  umlaut + u'ল',
		    umlaut + u'চ্ছিলাম',  umlaut + u'চ্ছিলেন', umlaut + u'চ্ছিলে', umlaut + u'চ্ছিলি',  umlaut + u'চ্ছিলেন', umlaut + u'চ্ছিল',  umlaut + u'চ্ছিল',
		    umlaut + u'তাম',  umlaut + u'তেন', umlaut + u'তে', umlaut + u'তি',  umlaut + u'তেন', umlaut + u'ত',  umlaut + u'ত',
		    verb + u'ব',  verb + u'বেন', verb + u'বে', umlaut + u'বি',  verb + u'বেন', verb + u'বে',  verb + u'বে',
		    umlaut + u'তে থাকব',  umlaut + u'তে থাকবেন', umlaut + u'তে থাকবে', umlaut + u'তে থাকবি',  umlaut + u'তে থাকবেন', umlaut + u'তে থাকবে',  umlaut + u'তে থাকবে',
		    umlaut + u'য়েছি',  umlaut + u'য়েছেন', umlaut + u'য়েছ', umlaut + u'য়েছিস',  umlaut + u'য়েছেন', umlaut + u'য়েছে',  umlaut + u'য়েছে',
		    umlaut + u'য়েছিলাম',  umlaut + u'য়েছিলেন', umlaut + u'য়েছিলে', umlaut + u'য়েছিলি',  umlaut + u'য়েছিলেন', umlaut + u'য়েছিল',  umlaut + u'য়েছিল',
		    umlaut + u'য়ে',
		    umlaut + u'লে',		    
		    verb + u'ন', umlaut2 + u'ও', verb,  verb + u'ন', umlaut + u'ক', umlaut + u'ক',
		    verb + u'বেন', umlaut + u'ও', umlaut + u'স',  verb + u'বেন', verb + u'বে', verb + u'বে'
		   )
    inflections = dict(zip(forms, inflections))
    
    return inflections


def process_verbs(list):
    # list is supposed to contain one word verbs, make sure the list is created that way
    for index, verb in enumerate(list):
	
	# when calculating length, we do not take chandrabindu and hasant into account
	length = len(verb.replace(u'ঁ', u'').replace(u'্', u'').decode('utf-8'))
	decoded_verb = verb.decode()
	
	if DEBUG == True:
	    print '[' + str(index) + ']', length, verb, " ",
	    pprint(decoded_verb)
	
	if length > 2:    
	    ''' XCK as in করা/পড়া/নাড়া
		Note: 1. we need to decive some rule for verbs like ওলটা  that is a derived form of উলটা, or ঝোলা - ঝুলা, গোছা - গুছা
			we'll do this in deeper steps of pipeline
	    '''
	    regex = BnChars['consonant_real'] + BnChars['marker'] + '(ঁ?)$'
	    p = re.compile(regex)
	    m = p.search(decoded_verb)
	    if m:
		if DEBUG == True:
		    print 'Matched', verb, 'XCK'
		inflection[decoded_verb] = get_inflection_do(decoded_verb, length)
		continue
	
	    
	    # TODO: intoduce another pipeline for filtering out regular and irregulars
	    # STATUS: DONE
	    
	    # The follwing two rules to do the same thing actually they could be done in a single regex
	    #but we are using three different filter for the clarity 
	    ''' েK as in লেখ, NOTE: some of these verbs has an internal umlaut like লেখ -> লিখ while others have no
		such umlaut such as খেল, ফেল  we need to process them as regular verbs, so a further pipeline is needed
	    '''
	    regex = u'ে(ঁ?)' + BnChars['consonant_real'] + '$'
	    p = re.compile(regex)
	    m = p.search(verb.decode())
	    if m:
		if DEBUG == True:
		    print 'Matched', verb, 'েC'
		inflection[decoded_verb] = get_inflection_write(decoded_verb, length)
		continue
	    
	    ''' োK as in খোল, these verbs have an internal umlaut like খোল -> খুল, শোন -> শুন '''	
	    regex = u'ো(ঁ?)' + BnChars['consonant_real'] + '$'
	    p = re.compile(regex)
	    m = p.search(verb.decode())
	    if m:
		if DEBUG == True:
		    print 'Matched', verb, 'োC'
		inflection[decoded_verb] = get_inflection_write(decoded_verb, length)
		continue
	    
	    ''' CKC as in পাড়, নাড়, ছুট '''	
	    regex = BnChars['consonant_real'] + BnChars['marker'] + u'(ঁ?)' + BnChars['consonant'] + '$'
	    p = re.compile(regex)
	    m = p.search(verb.decode())
	    if m:
		if DEBUG == True:
		    print 'Matched', verb, 'CKC'
		inflection[decoded_verb] = get_inflection_shake(decoded_verb, length)
		continue
	    
	# two letter verb
	elif length == 2:
	    # the regex is for constant NOT constant_real because there will not be a following marker
	    # we'll need a ওঠ - উঠ umlaut here
	    regex = u'ও(ঁ?)' + BnChars['consonant']
	    p = re.compile(regex)
	    m = p.search(verb.decode())
	    if m:
		if DEBUG == True:
		    print 'Matched', verb, 'ওK'
		inflection[decoded_verb] = get_inflection_write(decoded_verb, length)
		continue	    
	    
	    
	    ''' আঁক, আস - VK
		NOTE: আস - এসে, আন - এনে, this type of umlaut is common, so we'll need to process them later
	    '''
	    # the regex is for constant NOT constant_real because there will not be a following marker
	    regex = BnChars['vowel'] + u'(ঁ?)' + BnChars['consonant']
	    p = re.compile(regex)
	    m = p.search(verb.decode())
	    if m:
		if DEBUG == True:
		    print 'Matched', verb, 'VK'
		inflection[decoded_verb] = get_inflection_shake(decoded_verb, length)
		continue	    
	    
	    ''' যা - this is one of the special verbs '''	
	    regex = u'যা$'
	    p = re.compile(regex)
	    m = p.search(verb.decode())
	    if m:
		if DEBUG == True:
		    print 'Matched', verb, 'যা'
		inflection[decoded_verb] = get_inflection_go(decoded_verb, length)
		continue
	    
	    ''' Cে as in নে/দে '''	
	    regex = BnChars['consonant_real'] + 'ে(ঁ?)$'
	    p = re.compile(regex)
	    m = p.search(verb.decode())
	    if m:
		if DEBUG == True:
		    print 'Matched', verb, 'Cে'
		inflection[decoded_verb] = get_inflection_take(decoded_verb, length)
		continue
	    
	    ''' Cো as in শো '''	
	    regex = BnChars['consonant_real'] + 'ো(ঁ?)$'
	    p = re.compile(regex)
	    m = p.search(verb.decode())
	    if m:
		if DEBUG == True:
		    print 'Matched', verb, 'Cো'
		inflection[decoded_verb] = get_inflection_take(decoded_verb, length)
		continue	
		    
	    ''' CK as in খা/পা/শু/নি
		Note: There are internal umlaut like খা -> খে, পা -> পে, But শু, নি Does not
		have this kind of inflection, we'll just do a replace('া', 'ে') to get
		the umlaut
	    '''	
	    regex = BnChars['consonant_real'] + BnChars['marker'] + '(ঁ?)$'
	    p = re.compile(regex)
	    m = p.search(verb.decode())
	    if m:
		if DEBUG == True:
		    print 'Matched', verb, 'CK'
		inflection[decoded_verb] = get_inflection_eat(decoded_verb, length)	
		continue
	    
	    ''' CC as in কর, বল '''	
	    regex = BnChars['consonant'] + BnChars['consonant_real'] + '$'
	    p = re.compile(regex)
	    m = p.search(verb.decode())
	    if m:
		if DEBUG == True:
		    print 'Matched', verb, 'CC'
		# we could use another rule here, but this won't hurt either, becase the further
		# regex in the pipeline won't match and this is what we want in this case, as there
		# is no umlaut in this case
		inflection[decoded_verb] = get_inflection_shake(decoded_verb, length)
		continue
	    
	# one letter verb
	else:
	    ''' C as in ক, হ '''	
	    regex = BnChars['consonant_real'] + '$'
	    p = re.compile(regex)
	    m = p.search(verb.decode())
	    if m:
		if DEBUG == True:
		    print 'Matched', verb, 'C'
		inflection[decoded_verb] = get_inflection_eat(decoded_verb, length)
		continue
    
def normalize(list):
    ''' this function replaces any compound form with a single code point, for eg য় = য + ়(Nukta),
	but য় can be described with single code point \u09df, so if we get, \u09af (য) followed by a \u09bc (Nukta)
	we replace that with \u09df (য়)
    '''
    normalized_list = []
    for verb in list:
	normalized_list.append(verb.replace(u'\u09a1\u09bc', u'\u09dc').replace(u'\u09a2\u09bc', u'\u09dd').replace(u'\u09af\u09bc', u'\u09df'))
    
    return normalized_list

def insert_into_database(list, cursor):
    ''' update the verb_stems table in the datebase '''
    for verb in list:
	sql_check = ''' select count(*) from verb_stems where lemma = '%s' ''' % (verb.encode('utf-8'))
	#print sql_check
	cursor.execute(sql_check)
	
	result = cursor.fetchone()
	count, = result
	
	# if does not exist then insert
	if count == 0:
	    sql_insert = ''' insert into verb_stems(lemma) values('%s') ''' % (verb.encode('utf-8'))
	    print sql_insert
	    cursor.execute(sql_insert)

def get_list_from_database(cursor):
    single_word_verbs = []
    
    # verb from anubadok dix
    sql = ''' SELECT distinct word FROM meaning where pos = 'VV' '''
    append_real_verbs(cursor, sql, single_word_verbs)
    
    # verbs from unknown list
    sql = ''' SELECT distinct word FROM unknown_words u where pos = '2' ''' 
    append_real_verbs(cursor, sql, single_word_verbs)
    
    '''for verb in single_word_verbs:
	print verb
    '''
    single_word_verbs.append('খোল')
    
    return single_word_verbs


def get_prepared_list_from_database(cursor):
    ''' get single word verbs from the database '''
    sql_select = ''' SELECT lemma FROM verb_stems '''
    
    single_word_verbs = []
    
    if cursor.execute(sql_select):
	result = cursor.fetchall()
	
	for row in result:
	    verb, = row
	    single_word_verbs.append(verb)
	    
    return single_word_verbs


def print_speling():
    ''' create the speling format '''
    for lemma, v in inflection.iteritems():
	for tense, exapand in v.iteritems():
	    print lemma + "; " + exapand + "; " +  speling_tags[tense] + "; vblex"
	    
def preprocess_dix_format():
    for lemma, details in inflection.iteritems():
	
	# we need to find the longest common substring from the inflectoion list
	tense_list, inflection_list = zip(*details.items())
	common = find_longest_common_substring_from_list(inflection_list)
	
	# create the pardef name
	pardef_name =  common + '/' +  lemma.replace(common, '', 1) + '__vblex'
	#print pardef_name
	
	dix_inflection_list = []
	
	for e in inflection_list:
	    # make sure we don't replace the lemma more than once of it's also occurs inside as a part 
	    dix_inflection_list.append(e.replace(common, '', 1))
	
	# now update the dix format
	dix_format[pardef_name] = {'suffixes': dict(zip(tense_list, dix_inflection_list)),
				   'lemma_end': lemma.replace(common, '', 1),
				   'lemma_start': common}
	
def print_dix():
    print '<dictionary>';
    print '  <pardefs>';
    
    print enclitic
    
    for pardef, properties in dix_format.iteritems():
	print '    <pardef n=\"' + pardef + '\">'     
	
	lemma_start = properties['lemma_start']
	lemma_end = properties['lemma_end']
	
	for tense, suffix in properties['suffixes'].iteritems():
	    l = suffix
	    r = lemma_end + tags[tense]
	    #print '          <!-- %s; %s -->' % (lemma_start+lemma_end, lemma_start)
	    print '      <e>'
	    print '        <p>'
	    print '          <l>' + l + '</l>'
	    print '          <r>' + r + '</r>'
	    print '        </p>'
	    print '        <par n=\"enclitic\"/>'
	    print '      </e>'
	print '    </pardef>'
	    
    print '  </pardefs>';
    
    print '  <section id="main" type="standard">'
    for pardef, properties in dix_format.iteritems():
	lemma_start = properties['lemma_start']
	lemma_end = properties['lemma_end']
	# this lemma does not contain any blank space, otherwise we'll need to take care of them too
        print '    <e lm=\"' + lemma_start + lemma_end + '\"><i>' + lemma_start +'</i><par n=\"'  + pardef + '\"/></e>'
    print '  </section>'
    print '</dictionary>'
    
def get_prepared_list_from_file():
    single_word_verbs = []
    f = open('verb.bn.list')
    for line in f:
        single_word_verbs.append(line.strip())
    return single_word_verbs
    
try:
    print >> sys.stderr, "STARTING"
    
    conn = MySQLdb.connect(host = "localhost", user = "root", passwd = "root", db = "bengali_conjugator")
    
    cursor = conn.cursor()
    cursor.execute('SET CHARACTER SET utf8')
    
    # use this segment to create the verb_stems table
    '''
    single_word_verbs = get_list_from_database(cursor)
    single_word_verbs = normalize(single_word_verbs)
    insert_into_database(single_word_verbs, cursor)
    '''
    inflection = {}
    dix_format = {}
    
    # use this segment to get the prepared verbs from the verb_stems table
    #single_word_verbs = get_prepared_list_from_database(cursor)
    
    # use the file for now
    single_word_verbs = get_prepared_list_from_file()
    
    process_verbs(single_word_verbs)
    
    #pprint(inflection)
    
    #print_speling()
    
    preprocess_dix_format()
    #pprint(dix_format)
    print_dix()
    
    cursor.close()
    conn.close()
    
    print >> sys.stderr, "DONE"
except MySQLdb.Error, e:
	print "Error %d: %s" % (e.args[0], e.args[1])
	sys.exit (1)