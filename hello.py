import requests
import json
import threading
import time

urlList = [
    # 设置要监控的url
    "https://m.poizon.com/mapi/product/detail?productId=14450&source=shareDetail&sign=08ab59f20a7c8c08b199156a863d3c52",
    "https://m.poizon.com/mapi/product/detail?productId=27050&source=shareDetail&sign=29d7ca0272239f18e230e473212b2c7d",
    "https://m.poizon.com/mapi/product/detail?productId=26715&source=shareDetail&sign=f9475e1e7c6df8fde0877186f7d4a5f8",
]

# 设置每次抓数间隔 单位：秒
interval = 5


currentTime = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
print(currentTime + " 程序启动, 迎娶白富美...  ")

dataDict = {}


def pullData():
    print(currentTime + " 抓取数据, 走向人生巅峰...")
    for url in urlList:
        response = requests.get(url)
        res = response.json()
        data = res['data']
        title = data['detail']['title']
        productId = str(data['detail']['productId'])
        sizeList = data['sizeList']
        prodDict = {}
        for item in sizeList:
            prodDict[item['size']] = (
                item['item']['price'] / 100) if item['item'] else 0

        oldProdDict = dataDict.get(title)
        if(oldProdDict is None):
            dataDict[title] = prodDict
            prodDict = json.dumps(prodDict)
            rowData = currentTime + " 发现新数据：" + title + " - " + str(prodDict)
            print(rowData)
            with open(r'.\\' + productId + '.txt', 'a') as file:
                file.write('\r\n' + rowData)
        else:
            oldProdDictJson = json.dumps(oldProdDict)
            prodDictJson = json.dumps(prodDict)
            if(oldProdDictJson != prodDictJson):
                rowData1 = currentTime + " 请注意以下数据有变化: " + title + " ！！！"
                rowData2 = currentTime + " 旧数据: " + oldProdDictJson
                rowData3 = currentTime + " 新数据: " + prodDictJson

                newData = {}
                removeData = {}
                diffData = {}
                oldKeys = oldProdDict.keys()
                for key in oldKeys:
                    oldData = oldProdDict.get(key)
                    currData = prodDict.get(key)
                    if(currData is None):
                        removeData[key] = oldData
                    elif(oldData != currData):
                        diffData[key] = str(oldData) + '->' + str(currData)
                newKeys = prodDict.keys()
                for key in newKeys:
                    if(not key in oldProdDict):
                        currData = prodDict.get(key)
                        newData[key] = currData

                rowDataNew = {}
                rowDataRemove = {}
                rowDataDiff = {}
                if(len(newData) > 0):
                    rowDataNew = currentTime + " 新增码数：" + str(newData)
                if(len(removeData) > 0):
                    rowDataRemove = currentTime + " 减少码数：" + str(removeData)
                if(len(diffData) > 0):
                    rowDataDiff = currentTime + " 价格变化：" + str(diffData)

                print(rowData1)
                print(rowData2)
                print(rowData3)
                if(len(rowDataNew) > 0):
                    print(rowDataNew)
                if(len(rowDataRemove) > 0):
                    print(rowDataRemove)
                if(len(rowDataDiff) > 0):
                    print(rowDataDiff)

                with open(r'.\\' + productId + '.txt', 'a') as file:
                    file.write('\r\n' + rowData1)
                    file.write('\n' + rowData2)
                    file.write('\n' + rowData3)
                    if(len(rowDataNew) > 0):
                        file.write('\n' + rowDataNew)
                    if(len(rowDataRemove) > 0):
                        file.write('\n' + rowDataRemove)
                    if(len(rowDataDiff) > 0):
                        file.write('\n' + rowDataDiff)

                dataDict[title] = prodDict

    global timer
    timer = threading.Timer(interval, pullData)
    timer.start()


timer = threading.Timer(1, pullData)
timer.start()
