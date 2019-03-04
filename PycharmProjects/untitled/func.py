import time

trace_log = True


def trace(log):
    if trace_log:
        print(log)


def checkUICTemplate(tag9F0E, tag9F0F, tag9F0D, AID):
    # 模板1--借记DDA 联机PIN，允许bypassPIN
    # '00 10 80 00 00' 十六进制(发卡行为代码 -拒绝 )
    # 'D8 68 1C F8 00' 十六进制(发卡行为代码 -联机 )
    # 'D0 60 1C A8 00' 十六进制(发卡行为代码 -缺省 )
    # 模板2 --借记DDA 联机PIN，不允许bypassPIN
    # '00 10 98 00 00' 十六进制(发卡行为代码 -拒绝 )
    # 'D8 68 04 F8 00' 十六进制(发卡行为代码 -联机 )
    # 'D0 60 04 A8 00' 十六进制(发卡行为代码 -缺省 )
    # byte3 bit5 = 要求输入PIN，但密码键盘不存在或者不工作
    # byte3 bit4 = 要求输入PIN，密码键盘存在，但是未输入PIN
    # byte3 bit3 = 输入联机PIN
    tag9F0EByte3 = tag9F0E[4:6]
    tag9F0FByte3 = tag9F0F[4:6]
    tag9F0DByte3 = tag9F0D[4:6]
    result = ''

    debitAIDs = ['A000000333010101', 'A000000333018001']
    if AID in debitAIDs:
        if int(tag9F0EByte3, 16) & int('00', 16) == int('00', 16):
            result = '模板1--借记DDA 联机PIN，允许bypassPIN'
            if (int(tag9F0FByte3, 16) & int('1C', 16) != int('1C', 16)) or \
               (int(tag9F0DByte3, 16) & int('1C', 16) != int('1C', 16)):
                result = result + "\n 9F0F, 9F0D 设置有问题"
        elif int(tag9F0EByte3, 16) & int('18', 16) == int('18', 16):
            result = '模板2--借记DDA 联机PIN，不允许bypassPIN'
            if (int(tag9F0FByte3, 16) & int('04', 16) != int('04', 16)) or \
               (int(tag9F0DByte3, 16) & int('04', 16) != int('04', 16)):
                    result = result + "\n 9F0F, 9F0D 设置有问题"
        else:
            result = "未知 IAC，请人工检查数据 "
        return result

    if AID == "A000000333010103":
        return "准贷记DDA 联机PIN，允许bypassPIN"
    if AID == 'A000000333010102':
        if int(tag9F0FByte3, 16) & int('3C', 16) == int('3C', 16):
            result = '模板6--贷记DDA 脱机PIN，允许bypassPIN'
            if (int(tag9F0DByte3, 16) & int('3C', 16) != int('3C', 16)) or \
               (int(tag9F0EByte3, 16) & int('80', 16) != int('80', 16)):
                    result = result + "\n 9F0E, 9F0D 设置有问题"
        elif int(tag9F0FByte3, 16) & int('1C', 16) == int('1C', 16):
            result = '模板3--贷记DDA 联机PIN，允许bypassPIN'
            if (int(tag9F0DByte3, 16) & int('1C', 16) != int('1C', 16)) or \
               (int(tag9F0EByte3, 16) & int('00', 16) != int('00', 16)):
                    result = result + "\n 9F0E, 9F0D 设置有问题"
        elif (int(tag9F0FByte3, 16) & int('04', 16) == int('04', 16)):
            if (int(tag9F0EByte3, 16) & int('18', 16) == int('18', 16)):
                result = '模板5--贷记DDA 联机PIN，不允许bypassPIN'
                if (int(tag9F0DByte3, 16) & int('04', 16) != int('04', 16)):
                    result = result + "\n 9F0D 设置有问题"
            elif (int(tag9F0EByte3, 16) & int('00', 16) == int('00', 16)):
                result = '模板4--贷记DDA 签名 联机控制'
                if (int(tag9F0DByte3, 16) & int('04', 16) != int('04', 16)):
                    result = result + "\n 9F0D 设置有问题"
            else:
                result = "未知 IAC，请人工检查数据 "
        else:
            result = "未知 IAC，请人工检查数据 "
        return result
    if AID == 'A000000333010106':
        return '模板11--纯电子现金DDA'
    else:
        return '未知AID'


def little_endian_ascii2hexStr(input_ascii):
    i = 0
    outputStr = ""
    while i < len(input_ascii):
        strTemp = hex(input_ascii[i])
        strTemp = strTemp.replace('0x', '')
        if(len(strTemp) == 1):
            strTemp = '0' + strTemp
        outputStr = outputStr + strTemp
        i = i + 1
    return outputStr


def big_endian_ascii2hexStr(input_ascii):
    i = 0
    outputStr = ""
    while i < len(input_ascii):
        strTemp = hex(input_ascii[i])
        strTemp = strTemp.replace('0x', '')
        if(len(strTemp) == 1):
            strTemp = '0' + strTemp
        outputStr = strTemp + outputStr
        # trace(outputStr)
        i = i + 1
    return outputStr


def get_DGIcontext(gpf_file, DGIname_list, DGIContext_hash):
    Single_ICData = ''
    with open(gpf_file, 'rb') as source_file:
        source_file.seek(8596)
        bstemp = source_file.read(4)
        DGIname_list_len = int(big_endian_ascii2hexStr(bstemp), 16)
        for i in range(0, DGIname_list_len):
            bstemp = source_file.read(2)
            bsSingleDGIname_len = int(big_endian_ascii2hexStr(bstemp), 16)
            bstemp = source_file.read(bsSingleDGIname_len)
            tag = str(bstemp).replace('b', '').replace('\'', '').upper()
            DGIname_list.append(tag)
            # trace(tag)
        source_file.read(4)
        bstemp = source_file.read(2)
        # trace(bstemp)
        ICData_len = int(big_endian_ascii2hexStr(bstemp), 16)
        # trace(ICData_len)
        bstemp = source_file.read(ICData_len)
        Single_ICData = little_endian_ascii2hexStr(bstemp)

    for DGIname in DGIname_list:
        temp_str = Single_ICData[2:4]
        if temp_str == '82':
            length = 2*int(Single_ICData[4:8], 16)
            single_DGIData = Single_ICData[8:length+8]
            next_DGI_index = 8 + length
        elif temp_str == '81':
            length = 2*int(Single_ICData[4:6], 16)
            single_DGIData = Single_ICData[6:length+6]
            next_DGI_index = 6 + length
        else:
            length = 2*int(Single_ICData[2:4], 16)
            single_DGIData = Single_ICData[4:length+4]
            next_DGI_index = 4 + length
        DGIContext_hash[DGIname] = single_DGIData.upper()
        Single_ICData = Single_ICData[next_DGI_index:]


def ToTlvFormat(DGIValue, Tag_dic, tag_list=[]):
    TagTempls = ['70', 'A5', '61']
    index = 0
    tag_Sequence = 0
    strDGI = DGIValue
    while index < len(strDGI):
        # trace('strDGI = %s' % strDGI)
        tag = strDGI[index:index + 2]
        # trace('Tag = %s' % tag)
        length = 0
        value = ''
        if tag == '' or len(tag) == 1:
            print(tag + ' :待解析的TLV结构为空或者不符合TLV！')
            raise ValueError(tag + ' :待解析的TLV结构为空或者不符合TLV！')
        # Tag first Byte
        # bit6 means if it is a complex TLV;
        # bit5-Bit1 = 1 1111 means this tag need one more byte
        # if the next byte bit8=1, it means need one more byte and so on.
        # Currently, EMV requirement is 2 bytes and no more than 4 bytes

        # ------To judge is it is a complex TLV
        if (int(tag, 16) & int('20', 16)) != int('20', 16):
            isBasicTLVstructure = True
        else:
            isBasicTLVstructure = False
        if isBasicTLVstructure and (tag not in TagTempls):
            # it means single TLV structure. 基本数据结构
            # trace('基本数据对象')
            if int(tag, 16) & int('1f', 16) == int('1f', 16):
                #  it means 多字节Tag eg: buffer[currentIndex] & 0x1f) == 0x1f
                tag = strDGI[index:index+4]
                if len(tag) % 2 != 0:
                    print('Parse %s fail at offset %d ' % (strDGI, index))
                    raise ValueError('Parse %s fail at offset %d ' % (strDGI, index))
                index += 4
            else:
                index += 2
            if len(strDGI) <= index:
                # 仅有Tag，没有Length，报错
                print('Parse %s fail at offset %d. Only Tag, no L-V ' % (strDGI, index))
                raise ValueError('Parse %s fail at offset %d. Only Tag, no L-V ' % (strDGI, index))
            strLength = strDGI[index:index+2]
            if strLength == '82':
                strLength = strDGI[index+2:index+2+4]
                index += 6
            elif strLength == '81':
                strLength = strDGI[index+2:index+2+2]
                index += 4
            else:
                strLength = strDGI[index:index+2]
                index += 2
            length = 2 * int(strLength, 16)
            if len(strDGI) <= index + length - 1:
                print('Parse %s fail at offset %d. Only Tag, no L-V ' % (strDGI, index))
                raise ValueError('Parse %s fail at offset %d. Only Tag, no L-V ' % (strDGI, index))
            value = strDGI[index:index+length]
            Tag_dic[tag] = value
            tag_list.append(tag)
            tag_Sequence += 1
            index += length
        else:  # it means complex TLV structure. 嵌套数据结构
            # trace('结构数据对象')
            if int(tag, 16) & int('1f', 16) == int('1f', 16):  # it means 多字节Tag eg: buffer[currentIndex] & 0x1f) == 0x1f
                tag = strDGI[index:index+4]
                if len(tag) % 2 != 0:
                    print('Parse %s fail at offset %d ' % (strDGI, index))
                    raise ValueError('Parse %s fail at offset %d ' % (strDGI, index))
                index += 4
            else:
                index += 2
            if len(strDGI) <= index:
                # 仅有Tag，没有Length，报错
                print('Parse %s fail at offset %d. Only Tag, no L-V ' % (strDGI, index))
                raise ValueError('Parse %s fail at offset %d. Only Tag, no L-V ' % (strDGI, index))
            strLength = strDGI[index:index+2]
            if strLength == '82':
                strLength = strDGI[index+2:index+2+4]
                index += 6
            elif strLength == '81':
                strLength = strDGI[index+2:index+2+2]
                index += 4
            else:
                strLength = strDGI[index:index+2]
                index += 2
            length = 2 * int(strLength, 16)
            if len(strDGI) <= index + length - 1:
                print('Parse %s fail at offset %d. Only Tag, no L-V ' % (strDGI, index))
                raise ValueError('Parse %s fail at offset %d. Only Tag, no L-V ' % (strDGI, index))
            value = strDGI[index:index+length]
            # Tag_dic[tag] = value
            ToTlvFormat(value, Tag_dic, tag_list)
            index += length


def _ParseAFL_to_TLV(afl, DGIContext_hash, tag_dic):
    # eg: afl = 94 10 10050701 18010100 30010100 18020300
    # eg: obtain DGI0101
    exceptDGIs = ['']
    if len(afl) % 8 != 0:
        print('Error: AFL %s  长度不是8的倍数' % afl)
        raise ValueError('AFL %s  长度不是8的倍数' % afl)
    while 0 < len(afl):
        sfi = hex(int(afl[:2], 16)//8).replace("0x", "").zfill(2).upper()
        print(afl)
        # trace(afl[:8])
        j = int(afl[2:4], 16)
        while j <= int(afl[4:6], 16):
            DGIname = 'DGI' + sfi + hex(j).replace('0x', '').zfill(2).upper()
            print(DGIname)
            if DGIname not in DGIContext_hash.keys():
                print('Error: %s not exist! Need more detail check..' % DGIname)
                raise ValueError('Error: %s not exist! Need more detail check..' % DGIname)
            if DGIname not in exceptDGIs:
                DGIValue = DGIContext_hash[DGIname]
                ToTlvFormat(DGIValue[6:], tag_dic)
            else:
                print(DGIname + '未解析')
            j = j + 1
        afl = afl[8:]
    # print(DGIContext_hash)


def date_is_effective(target, candidate, format):
    if target == 'now':
        current_time = time.localtime()
        yyyy = str(current_time.tm_year).zfill(4)
        mm = str(current_time.tm_mon).zfill(2)
        dd = str(current_time.tm_mday).zfill(2)
    # format: 20181122
    if format == 'yyyymmdd':
        target = yyyy + mm + dd
        if len(target) != 8 or len(candidate) != 8:
            raise ValueError('日期格式有误 %s' % candidate)
        if int(target[:4]) < int(candidate[:4]):
            return True
        elif int(target[4:6]) < int(candidate[4:6]):
            return True
        elif int(target[6:]) <= int(candidate[6:]):
            return True
        else:
            return False
    elif format == 'yyyymm':
        target = yyyy + mm
        if len(target) != 6 or len(candidate) != 6:
            raise ValueError('日期格式有误 %s' % candidate)
        if int(target[:4]) < int(candidate[:4]):
            return True
        elif int(target[4:6]) <= int(candidate[4:6]):
            return True
        else:
            return False
    else:
        raise ValueError("该日期格式不支持")


def GetValFromDics(hash_list, tag):
    for hash in hash_list:
        if tag in hash.keys():
            return hash[tag]
    return ''


def GetConfigInfo(config_file, ConfigDic):
    with open(config_file, 'r') as source_file:
        lines = source_file.readlines()
    temp_key = ''
    for line in lines:
        line = line.replace('\n', '')
        if len(line) == 0 or line[0] == ';':
            continue
        if line[0] == '[':
            if not line.endswith('_setup]'):
                print('Wrong config format!!! %s' % line)
                raise ValueError('Wrong config format!!! %s' % line)
            temp_key = line[1:len(line)-1].replace('\n', '').strip()
            ConfigDic[temp_key] = {}
        else:
            tem_arr = line.strip().split('=')
            if len(tem_arr) != 2:
                print('Wrong config format!!! %s' % line)
                raise ValueError('Wrong config format!!! %s' % line)
            ConfigDic[temp_key][tem_arr[0].strip()] = tem_arr[1].strip()
            # eg: ConfigDic['GPF_setup']['AFLDGI_RSA'] = 'DGI9104


def GetKeysInfo(key_file, TransactionKeysDic):
    with open(key_file, 'r') as source:
        lines = source.readlines()
    for line in lines:
        if line[0] == ';' or len(line) < 32:
            continue
        else:
            tem_arr = line.strip().replace('\n', '').split('=')
            TransactionKeysDic[tem_arr[0]] = tem_arr[1]
