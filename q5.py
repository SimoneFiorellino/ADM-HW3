#Question 5


def subsequence(st):
    if len(st) == 1:
        return list(st)
    else:
        subs = subsequence(st[:len(st)-1])
        for element in subs:
            if element[-1] < st[-1]:
                subs += [element + st[-1]]
        subs += [st[-1]]
        return subs


def long_com_seq(s1 , s2): 
    x = len(s1) 
    y = len(s2) 
    val = list(["empty"]*(y+1) for i in range(x+1))
    for i in range(x+1): 
        for j in range(y+1): 
            if i == 0: 
                val[i][j] = 0
            elif j == 0:
                val[i][j] = 0
            elif s1[i-1] == s2[j-1]: 
                val[i][j] = val[i-1][j-1]+1
            else: 
                val[i][j] = max(val[i-1][j] , val[i][j-1])   
    return val[x][y]