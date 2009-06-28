#!/usr/bin/python

''' 
    This is an experimental script to generate speling format from paradef and 
    source xml
'''

import os
import sys
from xml.etree import ElementTree

def get_paradefs(paradef_root_elem): #{
    for element in paradef_root_elem: #{
        current_key = element.attrib['n']
        entries = []
        for e in element: #{
            if e.tag == 'e': #{
                for p in e: #{
                    if p.tag == 'p': #{
                        for node in p: #{
                            #print 'Debug', node.tag, node.text, node.tail, node.getchildren()                            
                            if node.tag == 'l': #{
                                for p in node: #{
                                    if p.tag == 'b': #{
                                        #print 'DEBUG: found'
                                        #node.remove(p)
                                        #ElementTree.dump(node)
                                        pass
                                    #}
                                #}
                                #print 'DEBUG: ', node.getchildren()
                                left = node.text
                            #}
                            if node.tag ==  'r': #{
                                right = node.text
                                tags = []
                                for s in node: #{
                                    if s.tag == 's': #{
                                        tags.append(s.attrib['n'])
                                    #}
                                #}
                            #}
                        #}
                    entry = left, right, tags
                    entries.append(entry)
                    #}
                #}
            #}
        #}
        paradefs[current_key] = entries
    #}
    return paradefs
#}

try:
    if len(sys.argv) < 3: #{
        print 'Usage: create-speling-from-paradef.py source.xml paradef.xml'
        sys.exit(1)
    #}    
    
    
    ''' construct paradefs '''
    paradefs = {}    
    paradef_file = os.path.dirname(__file__) + '/' + sys.argv[2]
    paradef_doc = ElementTree.parse(paradef_file)    
    paradef_root_elem = paradef_doc.getroot()
    
    ''' do the cleaning '''
    '''x = paradef_root_elem.getiterator('b')
    for y in x:
        paradef_root_elem.remove(y)    
    ElementTree.dump(paradef_root_elem)'''
    
    paradefs = get_paradefs(paradef_root_elem)
    
    
    
    ''' parse the input xml file '''    
    words = {}
    word = None
    rule =  None
    xml_file = os.path.dirname(__file__) + '/' + sys.argv[1]
    xml_doc = ElementTree.parse(xml_file)
    
    root_element = xml_doc.getroot()
    for element in root_element: #{
        if element.tag == 'e': #{
            ''' right now we are ignoring LR rules '''
            if 'r' not in element.keys(): #{
                for node in element: #{
                    if node.tag == 'i': #{
                        word =  node.text
                    #}
    	            if node.tag == 'par': #{
                        rule = node.attrib['n']
                    #}
                #}
                words[word] = rule
            #}
        #}
    #}
    
    ''' Do the bases conversion conversion '''
    for k, v in words.iteritems(): #{
        if k != None and v != None: #{
            for rule in paradefs[v]: #{
                #print k, rule
                surface = lemma = k
                if rule[0] != None: #{
                    surface += rule[0]
                #}
                if rule[1] != None: #{
                    lemma += rule[1]
                #}
                pos = rule[2][0]
                tag_str = ''
                for tag in rule[2][1:-1]: #{
                    tag_str += tag + "."
                #}
                tag_str += rule[2][-1]
                print surface + "; " + lemma + "; " + tag_str + "; " + pos
            #}
        #}        
    #}
    
    
except Exception, what:
    print """Exception "%s" occurred""" % (what)    
    

