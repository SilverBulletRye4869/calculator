#四則演算 + 括弧
import re
import math

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
    f_child = f_child.replace("PI",str(math.pi))
    f_child = f_child.replace("e",str(math.e))
    while ")" in f_child:
        kakko :int = f_child.find(")");
        for now in range(kakko,-1,-1):
            if(f_child[now] == "("):
                res: float = calcFunc(f_child[now+1:kakko])
                f_child = f_child[:now] + str(res)+f_child[kakko+1:]
                break
    return calcFunc(f_child)

#Function
def calcFunc(f_child: str) -> str:
    last : int = len(f_child)
    for now in range(len(f_child)-1,-1,-1):
        if(f_child[now].isdigit() or f_child[now]=='.'): continue;
        if((not f_child[now] in ["n","s","g"]) or (now <2)):
            if(not f_child[now-1:now+1] in ["n-","s-"]): last = now; 
            continue
        func : str = f_child[now-2:now+1]
        res:int =0;
        num: int = toFloat(f_child,now+1,last);
        if(func == "sin"): res = math.sin(num / 180.0 * math.pi);
        elif(func == "cos"): res = math.cos(num / 180.0 * math.pi);
        elif(func == "tan"): 
            if((num-90)%180 ==0): return "Err!"
            res = math.tan(num / 180.0 * math.pi);
        elif(func == "log"): 
            if(num<=0): return "Err!"
            res = math.log(num);
        res = round(res,12)
        now = now-2;
        f_child = f_child[:now] + str(res)+ f_child[last:]
    return calcEx(f_child)
#exponential
def calcEx(f_child: str) -> str:
    now = start = -1 #現在地
    place :int = 0; #項の始まり
    f_child+="\n";
    while True:
        now+=1;
        if(now >= len(f_child)): break;
        if(f_child[now].isdigit() or f_child[now]=='.'): continue;
        if (f_child[now]=="-" and re.compile(r"\s*").fullmatch(f_child[place:now])): continue
        if(start>=0):
            res: float = (toFloat(f_child,start,place-1))**(toFloat(f_child,place,now))
            f_child = f_child[:start] + str(res) + f_child[now:]
            now=start-1;
            place = start;
        if(f_child[now] == "^"): start = place;
        else: 
            start=-1; 
        place = now+1;
    return calcMD(f_child)

#乗除
def calcMD(f_child: str) -> str:
    if(f_child[-1] !='\n'): f_child +="\n";
    res :float  = 1; #現在の結果
    place :int  = 0; #見ている場所
    start = now  = -1; #剰余,現在地のスタート場所 (start:-1は無効モード)
    isMulti :bool = True; #乗算か？
    replaceMemo = []; #式の置き換えメモ
    while True:
        now+=1
        if(now>=len(f_child)): break
        if((not f_child[now].isdigit()) and (not f_child[now] in allowSymbol)): return "Err!" #変なのが来たらErr
        elif(f_child[now] == '+' or f_child[now] == '-' or f_child[now] == '\n' ): #＋、－、文末処理
            if (f_child[now]=="-" and re.compile(r"\s*").fullmatch(f_child[place:now])): continue 
            if(start>=0): #直前まで乗除であれば実行
                num = toFloat(f_child, place, now);
                if((not isMulti) and num==0): return "Err!"
                res *= num if isMulti else (1 / num); #resに対して数値を乗除
                f_child = f_child[:start] + str(res)+f_child[now:]
                now = start-1
                place=start
            res = 1; #結果を初期化
            place = now+1; #現在の位置を一つ後ろに
            start = -1; #乗除無効モードに
        elif(f_child[now] == '*' or f_child[now] == '/'): #乗除の時に実行
            if(start == -1): start = place; #現在地を掛け算のスタート位置に
            num = toFloat(f_child, place, now);
            if((not isMulti) and num==0): return "Err!"
            res *= num if isMulti else (1 / num); #resに対して数値を乗除
            isMulti = f_child[now]=="*"; #掛け算なら掛け算モードに
            place = now+1; #現在地を一つ後ろに
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
    print(calcFunc("log1"))
else:
    testFile = open("testcase.txt", "r")
    ansFile = open("anscase.txt","r")
    testCases = testFile.readlines()
    ansCases = ansFile.readlines()
    testFile.close()
    ansFile.close()
    ACCnt : int = 0
    for i in range(0,len(testCases)):
        resultStr : str =0;
        try:
            resultStr = calcMain(testCases[i])
        except:
            print(str(i+1)+f"{bc.FAIL}[RE]{bc.RESET}")
            continue

        try:
            resultFloat : float = round(float(resultStr),10)
            if(resultFloat == float(ansCases[i])):
                print(str(i+1)+f"{bc.OK}[AC]{bc.RESET}")
                ACCnt+=1
            else:
                print(str(i+1)+f"{bc.WARNING}[WA]{bc.RESET}")
                print(str(resultFloat) + "-"+ ansCases[i])
        except ValueError:
            if(resultStr == ansCases[i].replace("\n","")):
                print(str(i+1)+f"{bc.OK}[AC]{bc.RESET}")
                ACCnt+=1
            else:
                print(str(i+1)+f"{bc.WARNING}[WA]{bc.RESET}")
                print(resultStr + "-"+ ansCases[i])

    print("----- [総合結果] -----")
    if ACCnt == len(testCases):
        print(f"{bc.OK}[All-AC]{bc.RESET} (" + str(ACCnt)+"/"+str(len(testCases))+")")
    else:
        print(f"{bc.WARNING}[WA]{bc.RESET} (" + str(ACCnt)+"/"+str(len(testCases))+")")
    print("----------------------")