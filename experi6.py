#四則演算 + 括弧
import re

class bc:
    OK = '\033[92m' #GREEN
    WARNING = '\033[93m' #YELLOW
    FAIL = '\033[91m' #RED
    RESET = '\033[0m' #RESET COLOR

allowSymbol = ("+","-","*","/"," ","\n",".");
def toFloat(target: str, start: int, end: int) -> float:
    if(start >= end): return 0;
    return float(target[start:end].replace(" ",""));


def calcMain(f_child: str) -> str:
    while ")" in f_child:
        kakko = now =-1;
        while True:
            now+=1;
            if (now>=len(f_child)): break
            if(f_child[now] == "("):
                kakko=now;
            elif(f_child[now]==")"):
                if(kakko==-1): return "Err"
                res: float = calcMD(f_child[kakko+1:now])
                f_child = f_child[:kakko] + str(res)+f_child[now+1:]
                break
    return calcMD(f_child)

#乗除
def calcMD(f_child: str) -> str:
    f_child+="\n";
    res :float  = 1; #現在の結果
    place :int  = 0; #見ている場所
    start :int  = -1; #剰余のスタート場所 (-1は無効モード)
    isMulti :bool = True; #乗算か？
    replaceMemo = []; #式の置き換えメモ
    
    now : int= -1;
    while True:
        now+=1
        if(now>=len(f_child)): break
        if((not f_child[now].isdigit()) and (not f_child[now] in allowSymbol)): return "Err!" #変なのが来たらErr
        elif(f_child[now] == '+' or f_child[now] == '-' or f_child[now] == '\n' ): #＋、－、文末処理
            if (f_child[now]=="-" and re.compile(r"\s*").fullmatch(f_child[place:now])): continue 
            if(start>=0): #直前まで乗除であれば実行
                res *= toFloat(f_child, place, now) if isMulti else (1 / toFloat(f_child, place, now)); #resに対して数値を乗除
                replaceMemo.append(start); #乗除算の開始位置をメモ
                replaceMemo.append(now); #乗除算の終了位置をメモ
                replaceMemo.append(res); #乗除算の結果をメモ
            res = 1; #結果を初期化
            place = now+1; #現在の位置を一つ後ろに
            start = -1; #乗除無効モードに
        elif(f_child[now] == '*' or f_child[now] == '/'): #乗除の時に実行
            if(start == -1): start = place; #現在地を掛け算のスタート位置に
            res *= toFloat(f_child, place, now) if isMulti else (1 / toFloat(f_child, place, now)); #resに対して数値を乗除
            isMulti = f_child[now]=="*"; #掛け算なら掛け算モードに
            place = now+1; #現在地を一つ後ろに
        
    for i in range(len(replaceMemo)-1,-1,-3): #掛け算を計算済み値に置換
        f_child = f_child[0:replaceMemo[i-2]] + str(replaceMemo[i]) + f_child[replaceMemo[i-1]:len(f_child)]

    return calcAS(f_child)

def calcAS(f_child: str) -> str:
    f_length = len(f_child);
    res :float  = 0; #現在の結果
    place :int  = 0; #見ている場所
    isPlus :bool = True; #加算か？
    
    now : int= -1
    while True:
        now+=1
        if(now >= len(f_child)): break
        if((not f_child[now].isdigit()) and (not f_child[now] in allowSymbol)): return "Err"
        if(f_child[now] == '+' or f_child[now] == '-'):
            if (f_child[now]=="-" and re.compile(r"\s*").fullmatch(f_child[place:now])): continue 
            res += toFloat(f_child, place, now) if isPlus else -toFloat(f_child, place, now) #前回の記号の次から今の一個手前までを数値に変換して加算か減算
            isPlus= f_child[now]=='+'; #足し算なら足し算モードに！
            place = now+1; #一個後を次の開始位置に
    res += toFloat(f_child, place, len(f_child)) if isPlus else -toFloat(f_child, place,len(f_child))
    return str(res);


singleDebug : bool = False
if singleDebug: 
    print(calcMain("(((3))*(3+2))"))
else:
    testFile = open("testcase.txt", "r")
    ansFile = open("anscase.txt","r")
    testCases = testFile.readlines()
    ansCases = ansFile.readlines()
    testFile.close()
    ansFile.close()
    ACCnt : int = 0
    for i in range(0,len(testCases)):
        result : int =0;
        try:
            result = float(calcMain(testCases[i]));
        except:
            print(f"{bc.FAIL}[RE]{bc.RESET}")
            continue
        if(result == float(ansCases[i])):
            print(f"{bc.OK}[AC]{bc.RESET}")
            ACCnt+=1
        else:
            print(f"{bc.WARNING}[WA]{bc.RESET}")
            print(str(result) + "-"+ ansCases[i])

    print("----- [総合結果] -----")
    if ACCnt == len(testCases):
        print(f"{bc.OK}[All-AC]{bc.RESET} (" + str(ACCnt)+"/"+str(len(testCases))+")")
    else:
        print(f"{bc.WARNING}[WA]{bc.RESET} (" + str(ACCnt)+"/"+str(len(testCases))+")")
    print("----------------------")
