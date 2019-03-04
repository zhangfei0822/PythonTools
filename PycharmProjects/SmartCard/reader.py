# encoding=utf-8

"""Reader connection

    This module has realized the communication between program and readers by using PySmartCard module.
    The protocol is PCSC, and others will be supported later.
"""
from PySmartCard.CpuCard import PcscReader
import time


def send_apdu(reader, apdu, recv_list, readertype=None):
    """Send apdu to cpu card by reader with input str type
    arguments:
    readr: PcscReader() , class type
    apdu:  string type
    recv_list: list which has two element and one is return value and the other is SW
    """
    # Clear list
    recv_list[:] = []
    apdu = apdu.replace(" ", "")
    time1 = time.strftime("%Y_%m_%d %H:%M:%S", time.localtime(time.time()))
    showlog = "{} {} {}".format(time1, " Send: ", apdu)
    # print(time1, " Send: ", apdu)
    print(showlog)
    result = reader.send_apdu(apdu, readertype)
    print('\n' * 3 + 'reader.send_apdu(apdu, readertype) returns: ')
    print(type(result))
    print(result)
    time2 = time.strftime("%Y_%m_%d %H:%M:%S", time.localtime(time.time()))
    showlog = "{} {} {}".format(time2, " Recv: ", result)
    print(showlog)
    # print(time2, " Recv: ", result)
    # recv values
    recv_list.append(result[:-4])
    # SW
    recv_list.append(result[-4:])
    print(recv_list)


def send_apducommand(reader, apdu, recv_list, readertype=None):
    send_apdu(reader, apdu, recv_list, readertype)
    if recv_list[1][0:2] == "61":
        apdu = "00C00000" + recv_list[1][2:4]
        send_apdu(reader, apdu, recv_list, readertype)
    elif recv_list[1][0:2] == "6C":
        apdu = apdu[0:8] + recv_list[1][2:4]
        send_apdu(reader, apdu, recv_list, readertype)


def PersoSingleCard():
    print("Test PcscReader...")
    pcsc = PcscReader()
    result = pcsc.get_pcsc_readerlist()
    readerNameList = result.split(";")
    for iname in range(len(readerNameList) - 1):
        showlog = "{} {} : {}".format("reader", iname, readerNameList[iname])
        print(showlog)

    # Identive CLOUD 4700 F Contact Reader 0
    # Identive CLOUD 4700 F Contactless Reader 1

    # linux readername
    # Contact Reader: Identive Identive CLOUD 4500 F Dual Interface Reader
    #                 [CLOUD 4700 F Contact Reader] (53201441201079) 00 00
    # Ctless Reader:Identive Identive CLOUD 4500 F Dual Interface Reader
    #               [CLOUD4700 F Contactless Reader] (53201441201079) 01 00
    # Test PcscReader...
    # reader 0 : NetOp Virtual Smart Card Reader 0
    # reader 1 : OMNIKEY CardMan 5x21 0
    # reader 2 : OMNIKEY CardMan 5x21-CL 0

    readername = "Identive CLOUD 4700 F Contact Reader 0"
    # readername = "Identive CLOUD 4700 F Contactless Reader 1 "
    for iname in range(len(readerNameList) - 1):
        readername = readerNameList[iname]
        result = pcsc.connect_device(readername)
        if len(result) == 0:
            showlog = "{} {} : {}  does not has a smart card here ".format("reader", iname, readerNameList[iname])
            print(showlog)
        else:
            print("{} ConnectDevice Success...".format(readerNameList[iname]))
            print("ATR: ", result)

    # 1-contact reader 2-contactless reader
    readertype = 2

    result = pcsc.power_on(readertype)
    if result != 0:
        pcsc.disconnect_device()
        print("Device PowerOn Failed!")
        return -1
    else:
        print("Device PowerOn Success...")

    apdu = "0084000008"
    apdu = "00A4040008 A000000632010105"
    apdu = "00A4040008 A000000333010102"
    revc_info = []
    send_apducommand(pcsc, apdu, revc_info, readertype)
    if revc_info[1] != "9000":
        pcsc.disconnect_device()
        print("Send Apdu Failed!")
        return -1

    apdu = "00B2010C00"
    icount = 1
    while (1):
        send_apducommand(pcsc, apdu, revc_info, readertype)
        if revc_info[1] != "9000":
            print("Send Apdu Failed!")
            return -1
        icount = icount + 1
        if icount > 50:
            break

    pcsc.disconnect_device()
    return 0


if __name__ == '__main__':
    if PersoSingleCard() == 0:
        print("Test OK...")
    else:
        print("Test Failed!")