#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Levenshtein distance 


import sys, codecs

def levenshtein(s1, s2):
	
    l1 = len(s1)+1
    l2 = len(s2)+1
    dp = []
    #print l1,l2
    dp.append([j for j in range(l2)])
    
    for i in range(1,l1):
        t = [0 for j in range(l2)]
        t[0] = i
        dp.append(t)
    #print dp
    for i in range(1,l1):
        for j in range(1,l2):
            if s1[i-1] == s2[j-1]:   dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = min(dp[i-1][j]+1, dp[i-1][j-1]+1, dp[i][j-1]+1)
            #print dp[i][j],
        #print
    ins, delt, sub = 0, 0, 0

    i,j = l1-1,l2-1
    while(i>=1 or j>=1):
        #print (i,j)
        if dp[i][j] == dp[i-1][j-1]+1:
            sub += 1
            i,j=i-1,j-1
                
        elif dp[i][j] == dp[i-1][j]+1:
            ins += 1
            i,j=i-1,j
                
        elif dp[i][j] == dp[i][j-1]+1:
            delt += 1
            i,j=i,j-1
            
        else:
            i,j = i-1,j-1
            
    return (l1-1, ins, delt, sub)


def main():
    N = S = D = I = 0
    if len(sys.argv)<2:
        print '*ERROR: not enough arguments'
        return 1
    with codecs.open(sys.argv[1], encoding='utf-8') as f:
        for line in f:
    #s = raw_input().decode('utf-8').strip().split('*')
            s = line.strip().split('*')
            s1 = s[0].split(' ')
            #for i in s1: print i,
            #print
            s2 = s[1].split(' ')
            #for i in s2: print i,
            #print
            n,i,d,s = levenshtein(s1,s2)
            S += s
            D += d
            I += i
            N += n
    #print 'N:',N, '\tS:',S,'\tD:',D,'\tI:',I
    print  (S+D+I)
    return 0

if __name__ == '__main__':
	main()
