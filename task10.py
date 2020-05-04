import re
import json
import copy

valueRe = re.compile('value (\d+) goes to bot (\d+)')
jobRe = re.compile('bot (\d+) gives low to (bot|output) (\d+) and high to (bot|output) (\d+)')


def emptyBot():
    return {
        "low": None, 
        "high": None, 
        "value1": None, 
        "value2": None,
    }

def setVal(dct, key, val):
    if "bot" in key:
        dstVal1 = dct[key].get("value1", None)

        if dstVal1 is None:
            dct[key]["value1"] = val
        else:
            dct[key]["value2"] = val
    else:
        dstVal1 = dct[key].get("value1", None)
        if dstVal1 is None:
            dct[key]["value1"] = val
        else:
            dct[key]["value1"] = dct[key]["value1"] + val


def  printVals(dct, key):
    print("{}: ({}, {})".format(key, dct[key].get("value1", None), dct[key].get("value2", None)))

def loadInitialState(fileName="", state={}):
    with open(fileName) as f:
        for line in f:
            m = valueRe.match(line)
            if m:
                key="bot-{}".format(m.group(2))
                val=int(m.group(1))
                if state.get(key, None) is not None:
                    prevVal = state[key].get("value1", None)
                    if prevVal is not None:
                        state[key]["value2"] = val
                    else:
                        state[key]["value1"] = val
                else:
                    state[key] = emptyBot()
                    state[key]["value1"] =  val

            m = jobRe.match(line)

            if m:
                key="{}-{}".format("bot", m.group(1))
                if state.get(key, None) is None:
                    state[key] = emptyBot()

                keyLow="{}-{}".format(m.group(2), m.group(3))
                if state.get(keyLow, None) is None:
                    state[keyLow] = emptyBot()

                keyHight="{}-{}".format(m.group(4), m.group(5))
                if state.get(keyHight, None) is None:
                    state[keyHight] = emptyBot()

                state[key]["low"] = keyLow
                state[key]["high"] = keyHight


def makeMoves(state={}, exitCallBackFn="", debug=False):
    currentState = copy.deepcopy(state)
    newState = copy.deepcopy(state)

    movement = True
    while movement:
        movement = False
        for key in sorted(list(currentState.keys())):
            originVal1 = currentState[key].get("value1", None)
            originVal2 = currentState[key].get("value2", None)

            if debug:
                printVals(newState, key)

            if "bot" in key and originVal1 and originVal2:
                movement = True

                if callable(exitCallBackFn):
                    ret = exitCallBackFn(originVal1, originVal2)
                    if ret:
                        return key, currentState

                dstKeyLow=newState[key]["low"]
                dstKeyHigh=newState[key]["high"]

                if newState.get(dstKeyLow, None) is None:
                    newState[dstKeyLow] = emptyBot()

                if newState.get(dstKeyHigh, None) is None:
                    newState[dstKeyHigh] = emptyBot()


                dstLowVal1 = newState[dstKeyLow].get("value1", None)
                dstLowVal2 = newState[dstKeyLow].get("value2", None)

                dstHighVal1 = newState[dstKeyHigh].get("value1", None)
                dstHighVal2 = newState[dstKeyHigh].get("value2", None)

                # originVal1 - hight
                if originVal1 > originVal2:
                    setVal(newState, dstKeyHigh, originVal1)
                    setVal(newState, dstKeyLow, originVal2)
                else:
                    setVal(newState, dstKeyHigh, originVal2)
                    setVal(newState, dstKeyLow, originVal1)

                newState[key]["value1"] = None
                newState[key]["value2"] = None
        
        currentState = copy.deepcopy(newState)

    return None, state


if __name__ == '__main__':
    def breakAt61(val1, val2):
        if val1==61 and val2==17:
            return True
        if val1==17 and val2==61:
            return True
        return False

    st={}
    loadInitialState(fileName="task10.in.txt", state=st)
    bot, afterstate = makeMoves(state=st, exitCallBackFn=breakAt61)
    print("Answer ==>", bot)
