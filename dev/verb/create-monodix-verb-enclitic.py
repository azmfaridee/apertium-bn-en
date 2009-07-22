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

V = u'[অআইঈউঊঋএঐওঔ]'
C = u'[কখগঘঙচছজঝঞটঠডঢণতথদধনপফবভমযরলশষসহৎড়ঢ়য়]'
K = u'[ািীুূৃেৈোৌ]'
N = u'[০১২৩৪৫৬৭৮৯]'
M = u'[ঁংঃ]'
H = u'[্]'

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
for form in forms:
    symbol_tags = ""
    for s in form.split('_'):
	symbol_tags +=  '<n s=\"' + s + '\"/>'
    tags[form] = symbol_tags
    
    
speling_tags = {}
for form in forms:
    symbol_tags = form.replace('_', '.')
    speling_tags[form] = symbol_tags

    
#pprint(tags)

DEBUG = False

def dprint(str):
    if DEBUG == True:
	print "DEBUG: " + str

animacy_table = {'0': 'nn', '1': 'aa', '2': 'hu', '3': 'el'}
gender_table = {'0': 'mf', '1': 'm', '2': 'f', '3': 'nt'}

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
    
def append_real_verbs(cursor, sql, single_word_verbs):
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
	verb, = row
	real_verb = verb.split(' ')[-1]
	if real_verb != None and real_verb != '\n' and real_verb not in single_word_verbs:
	    single_word_verbs.append(real_verb)

def string_length_compare(a, b): 
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
    
    inflections = ( verb + "তে",
		    verb + "নোর",
		    verb + "নো",
		    verb + "ই",  verb + "ন", verb + "ও", verb + "স",  verb + "ন", verb + "য়",  verb + "য়",
		    verb + "চ্ছি",  verb + "চ্ছেন", verb + "চ্ছ", verb + "চ্ছিস",  verb + "চ্ছেন", verb + "চ্ছে",  verb + "চ্ছে",
		    verb + "লাম",  verb + "লেন", verb + "লে", verb + "লি",  verb + "লেন", verb + "ল",  verb + "ল",
		    verb + "চ্ছিলাম",  verb + "চ্ছিলেন", verb + "চ্ছিলে", verb + "চ্ছিলি",  verb + "চ্ছিলেন", verb + "চ্ছিল",  verb + "চ্ছিল",
		    verb + "তাম",  verb + "তেন", verb + "তে", verb + "তি",  verb + "তেন", verb + "ত",  verb + "ত",
		    verb + "ব",  verb + "বেন", verb + "বে", verb + "বি",  verb + "বেন", verb + "বে",  verb + "বে",
		    verb + "তে থাকব",  verb + "তে থাকবেন", verb + "তে থাকবে", verb + "তে থাকবি",  verb + "তে থাকবেন", verb + "তে থাকবে",  verb + "তে থাকবে",
		    umlaut + "য়েছি",  umlaut + "য়েছেন", umlaut + "য়েছ", umlaut + "য়েছিস",  umlaut + "য়েছেন", umlaut + "য়েছে",  umlaut + "য়েছে",
		    umlaut + "য়েছিলাম",  umlaut + "য়েছিলেন", umlaut + "য়েছিলে", umlaut + "য়েছিলি",  umlaut + "য়েছিলেন", umlaut + "য়েছিল",  umlaut + "য়েছিল",		    
		    umlaut + "য়ে",
		    verb + "লে",		    
		    verb + "ন", verb + "ও", verb, verb + "ন", verb + "ক", verb + "ক",
		    verb + "বেন", verb + "বে", verb + "বি",  verb + "বে", verb + "বি", verb + "বি" 
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
    
    inflections = ( umlaut + "তে",
		    verb + "ার",
		    verb + "া",
		    umlaut + "ি",  verb + "েন", verb, umlaut + "িস",  verb + "েন", verb + "ে",  verb + "ে",
		    umlaut + "ছি",  umlaut + "ছেন", umlaut + "ছ", umlaut + "ছিস",  umlaut + "ছেন", umlaut + "ছে",  umlaut + "ছে",
		    umlaut + "লাম",  umlaut + "লেন", umlaut + "লে", umlaut + "লি",  umlaut + "লেন", umlaut + "ল",  umlaut + "ল",
		    umlaut + "ছিলাম",  umlaut + "ছিলেন", umlaut + "ছিলে", umlaut + "ছিলি",  umlaut + "ছিলেন", umlaut + "ছিল",  umlaut + "ছিল",
		    umlaut + "তাম",  umlaut + "তেন", umlaut + "তে", umlaut + "তি",  umlaut + "তেন", umlaut + "ত",  umlaut + "ত",
		    umlaut + "ব",  umlaut + "বেন", umlaut + "বে", umlaut + "বি",  umlaut + "বেন", umlaut + "বে",  umlaut + "বে",
		    umlaut + "তে থাকব",  umlaut + "তে থাকবেন", umlaut + "তে থাকবে", umlaut + "তে থাকবি",  umlaut + "তে থাকবেন", umlaut + "তে থাকবে",  umlaut + "তে থাকবে",
		    umlaut + "েছি",  umlaut + "েছেন", umlaut + "েছ", umlaut + "েছিস",  umlaut + "েছেন", umlaut + "েছে",  umlaut + "েছে",
		    umlaut + "েছিলাম",  umlaut + "েছিলেন", umlaut + "েছিলে", umlaut + "েছিলি",  umlaut + "েছিলেন", umlaut + "েছিল", umlaut + "েছিল",  umlaut + "েছিল",					
		    umlaut + "ে",
		    umlaut + "লে",		    
		    umlaut + "ুন", verb, umlaut,  umlaut + "ুন", umlaut + "ুক", umlaut + "ুক",
		    umlaut + "বেন", verb + "ো", umlaut + "িস",  umlaut + "বেন", umlaut + "বে", umlaut + "বে"
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
    inflections = ( verb + "তে",
		    verb + "ার",
		    verb + "া",
		    verb + "ি", verb + "েন", verb, verb + "িস", verb + "েন", verb + "ে", verb + "ে",
		    verb + "ছি", verb + "ছেন", verb + "ছ", verb + "ছিস", verb + "ছেন", verb + "ছে", verb + "ছে", 
		    verb + "লাম",  verb + "লেন", verb + "লে", verb + "লি",  verb + "লেন", verb + "ল",  verb + "ল",
		    verb + "ছিলাম", verb + "ছিলেন", verb + "ছিলে", verb + "ছিলি", verb + "ছিলেন", verb + "ছিল", verb + "ছিল",
		    verb + "তাম", verb + "তেন", verb + "তে", verb + "তি", verb + "তেন", verb + "ত", verb + "ত",
		    verb + "ব", verb + "বেন", verb + "বে", verb + "বি", verb + "বেন", verb + "বে", verb + "বে",
		    verb + "তে থাকব", verb + "তে থাকবেন", verb + "তে থাকবে", verb + "তে থাকবি", verb + "তে থাকবেন", verb + "তে থাকবে", verb + "তে থাকবে",
		    umlaut + "েছি", umlaut + "েছেন", umlaut + "েছ", umlaut + "েছিস", umlaut + "েছেন", umlaut + "েছে", umlaut + "েছে",
		    umlaut + "েছিলাম", umlaut + "েছিলেন", umlaut + "েছিলে", umlaut + "েছিলি", umlaut + "েছিলেন", umlaut + "েছিল", umlaut + "েছিল", umlaut + "েছিল",
		    umlaut + "ে",
		    verb + "লে",		    
		    verb + "ুন", verb, verb, verb + "ুন", verb + "ুক", verb + "ুক",
		    verb + "বেন", umlaut + "ো", verb + "িস", verb + "বেন", verb + "বে", verb + "বে"
		   )
    inflections = dict(zip(forms, inflections))
    
    return inflections

def get_inflection_be(verb, length):
    # special inflection case for verb আছ - be
    umlaut = 'থাক'
    umlaut2 = 'রই'
    
    inflections = {}
    if DEBUG == True:
	print verb
    
    inflections = ( umlaut + "তে",
		    umlaut + "ার",
		    umlaut + "া",
		    verb + "ি",  verb + "েন", verb, verb + "িস",  verb + "েন", verb + "ে",  verb + "ে",
		    umlaut + "ছি",  umlaut + "ছেন", umlaut + "ছ", umlaut + "ছিস",  umlaut + "ছেন", umlaut + "ছে",  umlaut + "ছে",
		    umlaut + "লাম",  umlaut + "লেন", umlaut + "লে", umlaut + "লি",  umlaut + "লেন", umlaut + "ল",  umlaut + "ল",
		    umlaut + "ছিলাম",  umlaut + "ছিলেন", umlaut + "ছিলে", umlaut + "ছিলি",  umlaut + "ছিলেন", umlaut + "ছিল",  umlaut + "ছিল",
		    umlaut + "তাম",  umlaut + "তেন", umlaut + "তে", umlaut + "তি",  umlaut + "তেন", umlaut + "ত",  umlaut + "ত",
		    umlaut + "ব",  umlaut + "বেন", umlaut + "বে", umlaut + "বি",  umlaut + "বেন", umlaut + "বে",  umlaut + "বে",
		    umlaut2 + "তে থাকব",  umlaut2 + "তে থাকবেন", umlaut2 + "তে থাকবে", umlaut2 + "তে থাকবি",  umlaut2 + "তে থাকবেন", umlaut2 + "তে থাকবে",  umlaut2 + "তে থাকবে",
		    verb + "ি",  verb + "েন", verb, verb + "িস",  verb + "েন", verb + "ে",  verb + "ে",
		    "ছিলাম",  "ছিলেন", "ছিলে", "ছিলি", "ছিলেন", "ছিল", "ছিল",
		    "থেকে",
		    umlaut + "লে",		    
		    umlaut + "ুন", umlaut, umlaut, umlaut + "ুন", umlaut + "ুক", umlaut + "ুক",
		    umlaut + "বেন", "থেকো", "থাকিস",  umlaut + "বেন", umlaut + "বে", umlaut + "বে" 		    
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
    
    inflections = ( umlaut + "তে",
		    verb + "ার",
		    verb + "ওয়া",
		    verb + "ই",  verb + "ন", verb + "ও", verb + "স",  verb + "ন", verb + "য়",  verb + "য়",
		    verb + "চ্ছি",  verb + "চ্ছেন", verb + "চ্ছ", verb + "চ্ছিস",  verb + "চ্ছেন", verb + "চ্ছে",  verb + "চ্ছে",
		    umlaut + "লাম",  umlaut + "লেন", umlaut + "লে", umlaut + "লি",  umlaut + "লেন", umlaut + "ল",  umlaut + "ল",
		    verb + "চ্ছিলাম",  verb + "চ্ছিলেন", verb + "চ্ছিলে", verb + "চ্ছিলি",  verb + "চ্ছিলেন", verb + "চ্ছিল",  verb + "চ্ছিল",
		    umlaut + "তাম" ,  umlaut + "তেন", umlaut + "তে", umlaut + "তি",  umlaut + "তেন", umlaut + "ত",  umlaut + "ত",
		    verb + "ব",  verb + "বেন", verb + "বে", verb + "বি",  verb + "বেন", verb + "বে",  verb + "বে",
		    umlaut + "তে থাকব",  umlaut + "তে থাকবেন", umlaut + "তে থাকবে", umlaut + "তে থাকবি",  umlaut + "তে থাকবেন", umlaut + "তে থাকবে",  umlaut + "তে থাকবে",
		    umlaut + "য়েছি",  umlaut + "য়েছেন", umlaut + "য়েছ", umlaut + "য়েছিস",  umlaut + "য়েছেন", umlaut + "য়েছে",  umlaut + "য়েছে",
		    umlaut + "য়েছিলাম",  umlaut + "য়েছিলেন", umlaut + "য়েছিলে", umlaut + "য়েছিলি",  umlaut + "য়েছিলেন", umlaut + "য়েছিল",  umlaut + "য়েছিল",		    
		    umlaut + "য়ে",
		    umlaut + "লে",		    
		    verb + "ন", verb + "ও", verb, verb + "ন", verb + "ক", verb + "ক",
		    verb + "বেন", umlaut + "ও", verb + "স",  verb + "বেন", verb + "বে", verb + "বে"
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
        
    inflections = ( umlaut + "তে",
		    verb + "বার",
		    verb + "ওয়া",
		    verb + "ই",  verb + "ন", verb + "ও", verb + "স",  verb + "ন", verb + "য়",  verb + "য়",
		    verb + "চ্ছি",  verb + "চ্ছেন", verb + "চ্ছ", verb + "চ্ছিস",  verb + "চ্ছেন", verb + "চ্ছে",  verb + "চ্ছে",
		    umlaut2 + "লাম",  umlaut2 + "লেন", umlaut2 + "লে", umlaut2 + "লি",  umlaut2 + "লেন", umlaut2 + "ল",  umlaut2 + "ল",
		    verb + "চ্ছিলাম",  verb + "চ্ছিলেন", verb + "চ্ছিলে", verb + "চ্ছিলি",  verb + "চ্ছিলেন", verb + "চ্ছিল",  verb + "চ্ছিল",
		    umlaut + "তাম",  umlaut + "তেন", umlaut + "তে", umlaut + "তি",  umlaut + "তেন", umlaut + "ত",  umlaut + "ত",
		    verb + "ব",  verb + "বেন", verb + "বে", verb + "বি",  verb + "বেন", verb + "বে",  verb + "বে",
		    umlaut + "তে থাকব",  umlaut + "তে থাকবেন", umlaut + "তে থাকবে", umlaut + "তে থাকবি",  umlaut + "তে থাকবেন", umlaut + "তে থাকবে",  umlaut + "তে থাকবে",
		    umlaut3 + "য়েছি",  umlaut3 + "য়েছেন", umlaut3 + "য়েছ", umlaut3 + "য়েছিস",  umlaut3 + "য়েছেন", umlaut3 + "য়েছে",  umlaut3 + "য়েছে",
		    umlaut3 + "য়েছিলাম",  umlaut3 + "য়েছিলেন", umlaut3 + "য়েছিলে", umlaut3 + "য়েছিলি",  umlaut3 + "য়েছিলেন", umlaut3 + "য়েছিল",  umlaut3 + "য়েছিল",
		    umlaut3 + "য়ে",
		    umlaut2 + "লে",		    
		    verb + "ন", verb + "ও", verb, verb + "ন", verb + "ক", verb + "ক",
		    verb + "বেন", verb + "বে", verb + "বি",  verb + "বেন", verb + "বে", verb + "বে" 		    
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
    umlaut = re.sub(u'(' + BnChars['consonant_real'] +  u')(ো)(ঁ?)$', u'\g<1>ু\g<3>', verb)
    
    if DEBUG == True:    
	print verb, umlaut, umlaut2
        
    #inflections = {}

    inflections = ( umlaut + "তে",
		    verb + "বার",
		    verb + "ওয়া",
		    verb + "ই",  verb + "ন", umlaut2 + "ও", umlaut + "স",  verb + "ন", verb + "য়",  verb + "য়",
		    umlaut + "চ্ছি",  umlaut + "চ্ছেন", umlaut + "চ্ছ", umlaut + "চ্ছিস",  umlaut + "চ্ছেন", umlaut + "চ্ছে",  umlaut + "চ্ছে",
		    umlaut + "লাম",  umlaut + "লেন", umlaut + "লে", umlaut + "লি",  umlaut + "লেন", umlaut + "ল",  umlaut + "ল",
		    umlaut + "চ্ছিলাম",  umlaut + "চ্ছিলেন", umlaut + "চ্ছিলে", umlaut + "চ্ছিলি",  umlaut + "চ্ছিলেন", umlaut + "চ্ছিল",  umlaut + "চ্ছিল",
		    umlaut + "তাম",  umlaut + "তেন", umlaut + "তে", umlaut + "তি",  umlaut + "তেন", umlaut + "ত",  umlaut + "ত",
		    verb + "ব",  verb + "বেন", verb + "বে", umlaut + "বি",  verb + "বেন", verb + "বে",  verb + "বে",
		    umlaut + "তে থাকব",  umlaut + "তে থাকবেন", umlaut + "তে থাকবে", umlaut + "তে থাকবি",  umlaut + "তে থাকবেন", umlaut + "তে থাকবে",  umlaut + "তে থাকবে",
		    umlaut + "য়েছি",  umlaut + "য়েছেন", umlaut + "য়েছ", umlaut + "য়েছিস",  umlaut + "য়েছেন", umlaut + "য়েছে",  umlaut + "য়েছে",
		    umlaut + "য়েছিলাম",  umlaut + "য়েছিলেন", umlaut + "য়েছিলে", umlaut + "য়েছিলি",  umlaut + "য়েছিলেন", umlaut + "য়েছিল",  umlaut + "য়েছিল",
		    umlaut + "য়ে",
		    umlaut + "লে",		    
		    verb + "ন", umlaut2 + "ও", verb,  verb + "ন", umlaut + "ক", umlaut + "ক",
		    verb + "বেন", umlaut + "ও", umlaut + "স",  verb + "বেন", verb + "বে", verb + "বে"
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
    sql_select = ''' SELECT lemma FROM verb_stems '''
    
    single_word_verbs = []
    
    if cursor.execute(sql_select):
	result = cursor.fetchall()
	
	for row in result:
	    verb, = row
	    single_word_verbs.append(verb)
	    
    return single_word_verbs


def print_speling():
    for lemma, v in inflection.iteritems():
	for tense, exapand in v.iteritems():
	    print lemma + "; " + exapand + "; " +  speling_tags[tense] + "; vblex"
    
try:
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
    
    # use this segment to get the prepared verbs from the verb_stems table
    single_word_verbs = get_prepared_list_from_database(cursor)
    process_verbs(single_word_verbs)
    
    #pprint(inflection)
    print_speling()
    """
    for row in rows:
	db_lemma, db_animacy, db_gender = row
	#pprint(row)
	
	lemma = db_lemma
	gender = gender_table[db_gender]
	animacy = animacy_table[db_animacy]
	entries[lemma] = {'pos' : 'n', 'gender': gender, 'animacy': animacy, 'inflections': {}}
	
	#print lemma
	entries[lemma]['inflections']['nom'], entries[lemma]['inflections']['obj'], entries[lemma]['inflections']['gen'], entries[lemma]['inflections']['loc'] = get_inflection(lemma = lemma, animacy = animacy)
    
    #pprint(entries)
    
    print '<dictionary>';
    print '  <pardefs>';
    
    print enclitic
    
    for lemma, properties in entries.iteritems():
	#pprint(lemma)
	#pprint(properties)
	pos = properties['pos']
	gender = properties['gender']
	animacy = properties['animacy']
	print '    <pardef n=\"' + lemma + '__' + pos + '_' + gender +'\">'     
        
	for case, details in properties['inflections'].iteritems():
	    #print case, details
	    for type, details2 in details.iteritems():
		#print case, type, details2
		if details2 == None:
		    continue
		for number, affix in details2.iteritems():
		    #print case, type, number, affix
		    print '      <e>'
		    print '        <p>'
		    print '          <l>' + affix + '</l>'
		    r = get_sym([pos, gender, animacy])
		    number_symbol, def_symbol = get_num(number)
		    r = r + number_symbol + get_sym([case])
		    if def_symbol != None:
			r = r + def_symbol
		    print '          <r>' + r +'</r>'
		    print '        </p>'
		    print '        <par n=\"enclitic\"/>'
		    print '      </e>'
		    
		    # add enclitic e
		    
		    # add enclitic o
		    
	print '    </pardef>'
	    
    print '  </pardefs>';
    print '  <section id="main" type="standard">'
    for lemma, properties in entries.iteritems():
        print '    <e lm=\"' + lemma + '\"><i>' + lemma.replace(' ', '<b/>') +'</i><par n=\"' + lemma + '__' + properties['pos'] + '_' + properties['gender'] + '\"/></e>'
    print '  </section>'
    print '</dictionary>'
    """
    
    cursor.close()
    conn.close()
except MySQLdb.Error, e:
	print "Error %d: %s" % (e.args[0], e.args[1])
	sys.exit (1)



