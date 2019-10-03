import json
from datetime import date
import requests

import sys
import argparse

def fetchAbi(name,address):

    ABI_ENDPOINT = 'https://api.etherscan.io/api?module=contract&action=getabi&address='
    response = requests.get('%s%s'%(ABI_ENDPOINT, address))
    response_json = response.json()
    abi_json = json.loads(response_json['result'])
    result = json.dumps({"abi":abi_json}, indent=4, sort_keys=True)

    open(name, 'w').write(result)

def load_json(file_path):
    # open JSON file and parse contents
    fh = open(file_path,'r')
    data = json.load(fh)
    fh.close()

    return data


#used to fill in empty values for inexistant keys
def fillIn(dictionary,element,dictName):
    if element not in dictionary:
        dictionary[element] = ''
#         print(dictName+' is missing a '+element+' quality')
    return dictionary[element]

def addMessage(messageList, counter, message):
    messageList.append("\n"+str(counter)+" : "+message)
    counter = counter + 1
    return (messageList, counter)

def errorBundle(messageList, counter, key, fileA, fileB, dictA,dictB):
    messageList, counter = addMessage(messageList, counter, "Same ABI object name of ("+dictA["name"]+") and type ("+dictA["type"]+") - wrong "+key+" attribute")
    messageList, counter = addMessage(messageList, counter-1, "   Type in "+fileA+"= "+str(dictA[key]))
    messageList, counter = addMessage(messageList, counter-1, "   Type in "+fileB+"= "+str(dictB[key]))
    return (messageList, counter)


def compare_abi_data(A,fileA,B,fileB):

    errorMessage = []
    successMessage =[]
    errorCounter = 1
    successCounter = 1

    abiA = A['abi']
    abiB = B['abi']

#     if len(abiA)<len(abiB):
#         errorMessage.append('Please run compare_abi_data with flipped arguments')
#         return errorMessage
#     if len(abiA)>len(abiB):
#         print("Placeholder list elements added to abiB")
#         abiB.append({'Placeholder for comparison':'' for i in range(len(abiA)-len(abiB))})

    #keys that will be checked in each ABI obejct
    keys2check = ['name', 'type', 'inputs', 'outputs', 'constant', 'payable']

#fill in all keys that will be checked
    for i in range(len(abiB)):
        for k in range(len(keys2check)):
            abiB[i][keys2check[k]]=fillIn(abiB[i],keys2check[k],'abiB')


    for i in range(len(abiA)):

#         abiA[i]["name"]=fillIn(abiA[i],'name','abiA')
#         abiA[i]["type"]=fillIn(abiA[i],'type','abiA')

        for k in range(len(keys2check)):
            abiA[i][keys2check[k]]=fillIn(abiA[i],keys2check[k],'abiA')

        conditionName = 1
        conditionAttr = 1


        for k in range(len(abiB)):

            if abiA[i][keys2check[0]] == abiB[k][keys2check[0]]:
                conditionName = 0

                if abiA[i][keys2check[1]] == abiB[k][keys2check[1]]:

                    for u in range(2,4):

                        for j in range(len(abiA[i][keys2check[u]])):

                            for t in range(len(abiB[k][keys2check[u]])):


                                if not abiA[i][keys2check[u]][j]['name'] == abiB[k][keys2check[u]][t]['name']:
                                    conditionAttr = 0
                                    stateList = [errorMessage, errorCounter, 'name', fileA, fileB, abiA[i][keys2check[u]][j],abiB[k][keys2check[u]][t]]
                                    errorMessage, errorCounter = errorBundle(*stateList)

                                if not abiA[i][keys2check[u]][j]['type'] == abiB[k][keys2check[u]][t]['type']:
                                    conditionAttr = 0
                                    stateList = [errorMessage, errorCounter, 'type', fileA, fileB, abiA[i][keys2check[u]][j],abiB[k][keys2check[u]][t]]
                                    errorMessage, errorCounter = errorBundle(*stateList)


                    for n in range(4,len(keys2check)):

                        if not abiA[i][keys2check[n]] == abiB[k][keys2check[n]]:
                            conditionAttr = 0
                            stateList = [errorMessage, errorCounter, keys2check[n], fileA, fileB, abiA[i],abiB[k]]
                            errorMessage, errorCounter = errorBundle(*stateList)


                    if conditionAttr == 1:
                        successMessage, successCounter = addMessage(successMessage, successCounter, f'({abiA[i][keys2check[0]]}) \U00002705')

                    abiB.pop(k)
                    break


                else:
                    errorMessage, errorCounter = addMessage(errorMessage, errorCounter, "Same ABI object name of ("+abiA[i]["name"]+") in both but wrong type! ")
                    errorMessage, errorCounter = addMessage(errorMessage, errorCounter-1, "   Type in "+fileA+" = "+abiA[i]["type"])
                    errorMessage, errorCounter = addMessage(errorMessage, errorCounter-1, "   Type in "+fileB+" = "+abiB[k]["type"])

        if conditionName == 1:
            errorMessage, errorCounter = addMessage(errorMessage, errorCounter, "No ABI object named ("+abiA[i]["name"]+") in "+fileB)




    for k in range(len(abiB)):
        errorMessage, errorCounter = addMessage(errorMessage, errorCounter, fileB+" contains an additional ABI object named ("+abiB[k]["name"]+") of ("+abiB[k]["type"]+") type")


    if not errorMessage:
        errorMessage.append('Great! No errors')

    return errorMessage, successMessage



def main(args):
    parser = argparse.ArgumentParser("abi-compare")

    parser.add_argument("--fileA-name", type=str, required=True,
                            help="Name of base ABI file (e.g. weth.json)")

    parser.add_argument("--fileB-name", type=str, required=True,
                            help="Name of target ABI file (e.g. weth.json)")

    parser.add_argument("--contractA-address", type=str, required=True,
                            help="Ethereum address of the base token contract on mainnet")

    parser.add_argument("--contractB-address", type=str, required=True,
                            help="Ethereum address of the base token contract on mainnet")

    arguments = parser.parse_args(args)

    fileA = arguments.fileA_path
    fileB = arguments.fileB_path
    contractA = arguments.contractA_address
    contractB = arguments.contractB_address

    # fileA = 'weth.json'
    # fileB = 'BAT.json'
    # contractA = '0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2'
    # contractB = '0x0D8775F648430679A709E98d2b0Cb6250d2887EF'

    fetchAbi(fileA,contractA)
    fetchAbi(fileB,contractB)

    binance_json=load_json(fileA)
    weth_json=load_json(fileB)


    errorResult, matchResult = compare_abi_data(binance_json, fileA, weth_json, fileB)

    ## TODO, add more object attributes to check
    ## TODO, add the results of each check, list out which objects overlap in select area
    print("-----Results-----")
    print("Time: "+str(date.today()))
    print("Basis: "+fileA+" located at address "+ contractA)
    print("Checking: "+fileB+" located at address "+ contractB)



    print("\n-----Matches-----")
    print('Covers following attributes: name, type, inputs, outputs, constant, and payable')
    print("\n".join(matchResult))



    print("\n-----ERRORS-----")
    print("\n".join(errorResult))


if __name__== "__main__":
  main(sys.argv)
