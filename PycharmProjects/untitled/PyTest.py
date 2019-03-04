import xlwings as xw
import func
import time
import os
import tkinter.messagebox
import sys

gpf_file = ''
key_file = 'task\\ServerConfig.ini'
CAPP_file = 'task\\append_record_for_bctest.js'
config_file = 'BCTC_UICS.ini'
log_file = 'log.txt'
template_xlsm = '.\\BCTC_template\\PBOCUICS应用个人化信息表3.2.4 2018-10-15.xlsm'

ConfigDic = {}
DGINameList = []
DGIValDic = {}
TransactionKeysDic = {}
LAP_list = []

gpf_tags_RSA = {'DC': {}, 'ECC': {}, 'Q_UICS': {}}
gpf_tags_SM4 = {'DC': {}, 'ECC': {}, 'Q_UICS': {}}
ShareTags = {}
ShareTagsDC_ECC = {}
ShareTags_Q = {}
Tag9F45 = ''

try:
    log_writer = open(log_file, 'w')
    app = xw.App(visible=True, add_book=False)

    path = os.getcwd()
    key_file = path + "\\" + key_file
    CAPP_file = path + "\\" + CAPP_file
    config_file = path + "\\" + config_file
    log_file = path + "\\" + log_file

    gpf_file_count = 0
    for root, sub_dirs, files in os.walk('.\\task\\'):
        for single_file in files:
            if (single_file.endswith('.GPF') or single_file.endswith('.gpf')):
                gpf_file_count = gpf_file_count + 1
                gpf_file = os.path.join(root, single_file)
    if (gpf_file_count != 1):
        log_writer.write('NO GPF or more then one: %d \n' % gpf_file_count)
        tkinter.messagebox.showwarning('', 'GPF 数量: %d 不等于 1\n' % gpf_file_count)
        sys.exit()

    log_writer.write('Load transaction keys(AC, MAC, DEK) info......\n')
    func.GetKeysInfo(key_file, TransactionKeysDic)

    log_writer.write('Load config info......\n')
    func.GetConfigInfo(config_file, ConfigDic)

    log_writer.write('Load GPF info....%s ..\n' % gpf_file)
    func.get_DGIcontext(gpf_file, DGINameList, DGIValDic)

    AID = ''
    isSM4Data = False
    for DGIname in DGINameList:
        log_writer.write(DGIname + ':' + DGIValDic[DGIname] + '\n')
        index = DGIValDic[DGIname].find('4F08A000000333')
        AIDStart = index + 4
        if index > 0:
            AID = DGIValDic[DGIname][AIDStart:(AIDStart + 16)]

        index = DGIValDic[DGIname].find('DF6901')
        if index > 0:
            isSM4Data = True

    afl_list_rsa = []
    afl_list_sm4 = []
    if ('AFLDGI_RSA' not in ConfigDic['GPF_setup'].keys()) or \
            (len(ConfigDic['GPF_setup']['AFLDGI_RSA']) == 0):
        decision = tkinter.messagebox.askquestion("RSA AFL setup", \
                                                  'defalut: (DC,ECC,Q) DGI9104,DGI9203,DGI9207\n\n\n继续处理点击“确定”\n终止程序点击“取消”')
        if decision == 'no':
            tkinter.messagebox.showinfo('', '请在BCTC_UICS.ini中配置AFLDGI_RSA')
            sys.exit()
        else:
            ConfigDic['GPF_setup']['AFLDGI_RSA'] = 'DGI9104,DGI9203,DGI9207'
    log_writer.write('RSA AFL: ' + ConfigDic['GPF_setup']['AFLDGI_RSA'] + '\n')
    afl_list_rsa = ConfigDic['GPF_setup']['AFLDGI_RSA'].split(',')

    if isSM4Data:
        if ('AFLDGI_SM4' not in ConfigDic['GPF_setup'].keys()) or \
                (len(ConfigDic['GPF_setup']['AFLDGI_SM4']) == 0):
            decision = tkinter.messagebox.askquestion("SM4 AFL setup", \
                                                      'defalut: (DC,ECC,Q) DGI9114,DGI9213,DGI9217\n\n\n继续处理点击“确定”\n终止程序点击“取消”')
            if decision == 'no':
                tkinter.messagebox.showinfo('', '请在BCTC_UICS.ini中配置AFLDGI_SM4')
                sys.exit()
            else:
                ConfigDic['GPF_setup']['AFLDGI_SM4'] = 'DGI9114,DGI9213,DGI9217'
        log_writer.write('SM4 AFL = ' + ConfigDic['GPF_setup']['AFLDGI_SM4'] + '\n')
        afl_list_sm4 = ConfigDic['GPF_setup']['AFLDGI_SM4'].split(',')

        # RSA record data tags-----------
    # AFLDGI sequence should be DC,ECC,Q

    tansaction_hash = ['DC', 'ECC', 'Q_UICS']
    log_writer.write('afl_list_rsa start...' + '\n')
    for i in range(0, len(afl_list_rsa)):
        DGIValue = DGIValDic[afl_list_rsa[i]][6:]
        tag_dic = gpf_tags_RSA[tansaction_hash[i]]
        func.ToTlvFormat(DGIValue, tag_dic)
        afl = gpf_tags_RSA[tansaction_hash[i]]['94']
        func._ParseAFL_to_TLV(afl, DGIValDic, tag_dic)
    log_writer.write('afl_list_rsa end...' + '\n')
    if isSM4Data:
        log_writer.write('afl_list_sm4 start...' + '\n')
        for i in range(0, len(afl_list_sm4)):
            # print('debug-- %d' % i)
            DGIValue = DGIValDic[afl_list_sm4[i]][6:]
            # print('debug--2--')
            tag_dic = gpf_tags_SM4[tansaction_hash[i]]
            # print('debug--3--')
            func.ToTlvFormat(DGIValue, tag_dic)
            # print('debug--4--')
            afl = gpf_tags_SM4[tansaction_hash[i]]['94']
            # print('debug--5--')
            # afl = 'A80E0F00'
            func._ParseAFL_to_TLV(afl, DGIValDic, tag_dic)
        log_writer.write('afl_list_sm4 end...' + '\n')
    # private data tags
    log_writer.write('解析DGI0D01, DGI0E01.......' + '\n')
    tag_list = []
    func.ToTlvFormat(DGIValDic['DGI0D01'][6:], ShareTags)
    func.ToTlvFormat(DGIValDic['DGI0E01'][6:], ShareTags)
    # share DC&ECC tags
    log_writer.write('解析DGI9200, DGI9102.......' + '\n')
    tag_list = []
    func.ToTlvFormat(DGIValDic['DGI9200'][6:], ShareTagsDC_ECC)
    func.ToTlvFormat(DGIValDic['DGI9102'][6:], ShareTagsDC_ECC)
    # share Q tags
    log_writer.write('解析DGI9103.......' + '\n')
    func.ToTlvFormat(DGIValDic['DGI9103'][6:], ShareTags_Q)

    log_writer.write('对国密数据和国际数据中的9F10 进行补充.....')
    gpf_tags_RSA['DC']['9F10'] = ShareTagsDC_ECC['9F10']
    gpf_tags_RSA['ECC']['9F10'] = ShareTagsDC_ECC['9F10']
    if '9F10' not in gpf_tags_RSA['Q_UICS']:
        gpf_tags_RSA['Q_UICS']['9F10'] = ShareTagsDC_ECC['9F10']
    if isSM4Data:
        gpf_tags_SM4['DC']['9F10'] = gpf_tags_SM4['Q_UICS']['9F10']
        gpf_tags_SM4['ECC']['9F10'] = gpf_tags_SM4['Q_UICS']['9F10']
        for dic in gpf_tags_SM4:
            log_writer.write('******SM4_' + dic + '_记录数据tags\n')
            for tag in gpf_tags_SM4[dic]:
                log_writer.write(tag + ':' + gpf_tags_SM4[dic][tag] + '\n')
    log_writer.write('对国密数据和国际数据中的9F45 进行补充.....')
    gpf_tags_RSA['DC']['9F45'] = ConfigDic['Head_setup']['DC9F45']
    gpf_tags_RSA['ECC']['9F45'] = ConfigDic['Head_setup']['ECC9F45']
    gpf_tags_RSA['Q_UICS']['9F45'] = ConfigDic['Head_setup']['qUICS9F45']

    for dic in gpf_tags_RSA:
        log_writer.write('******RSA_' + dic + '_记录数据tags\n')
        for tag in gpf_tags_RSA[dic]:
            log_writer.write(tag + ':' + gpf_tags_RSA[dic][tag] + '\n')

    # check BCTC UICS LAP if is effective
    log_writer.write('......检查UICS证书是否过期.......' + '\n')
    current_time = time.localtime()
    # today = str(current_time.tm_year).zfill(4) + str(current_time.tm_mon).zfill(2) + str(current_time.tm_mday).zfill(2)
    chip = ConfigDic['Head_setup']['芯片商及型号']
    tem_arr = ConfigDic['UICS_LAP_setup'][chip].split(',')
    for temp in tem_arr:
        if func.date_is_effective('now', temp.split('|')[1], 'yyyymmdd'):
            LAP_list.append(temp.split('|')[0])
        else:
            raise ValueError(chip + 'BCTC 证书 失效！')
    # raise ValueError()
    # ---------------fix Excel----------------------
    log_writer.write('........打开BCTC表格，开始填写.......' + '\n')
    is_CAPP_data = False
    if ConfigDic['CAPP_setup']['appendCAPP'] == 'Y':
        is_CAPP_data = True
        template_xlsm = template_xlsm.replace('.xlsm', '_CAPP.xlsm')

    wb = app.books.open(template_xlsm)
    sheet = wb.sheets[0]  # 选择第0个表单
    log_writer.write('......开始填写表头.......' + '\n')
    BIN_row = ConfigDic['Ranges_setup']['BIN_row']
    row = int(BIN_row)
    sheet.range('B' + str(row)).value = ConfigDic['Head_setup']["BIN号"]

    tem_arr = ConfigDic['Ranges_setup']['CardInfo_range'].split('-')
    row = int(tem_arr[0])
    while row <= int(tem_arr[1]):
        # 注意 range （a, b）函数中的取值范围为a, a+1,..., b-1
        if sheet.range('A' + str(row)).value:
            item = sheet.range('A' + str(row)).value.strip()
            sheet.range('B' + str(row)).value = ConfigDic['Head_setup'][item]
        else:
            log_writer.write('Row: A' + str(row) + ' can not read ')
        row = row + 1

    tem_arr = ConfigDic['Ranges_setup']['UICSLAP_range'].split('-')
    row = int(tem_arr[0])
    i = 0
    while i < (int(tem_arr[1]) - int(tem_arr[0]) + 1):
        sheet.range('F' + str(row + i)).value = LAP_list[i]
        i = i + 1

    log_writer.write('......开始填写1公共部分.......' + '\n')
    tem_arr = ConfigDic['Ranges_setup']['pub1.1_range'].split('-')

    row = int(tem_arr[0])
    while row <= int(tem_arr[1]):
        log_writer.write('row %s start---\n' % str(row))
        if sheet.range('B' + str(row)).value:
            item = sheet.range('B' + str(row)).value.strip()
            hash_list = [gpf_tags_RSA['DC'], gpf_tags_RSA['ECC'], ShareTags, ShareTagsDC_ECC]
            tagValue = func.GetValFromDics(hash_list, item)
            if tagValue == '':
                log_writer.write('%s did not find any value\n' % item)
            else:
                sheet.range('E' + str(row)).value = tagValue
        else:
            log_writer.write('RowB%s can not read \n' % str(row))
        row = row + 1

    tem_arr = ConfigDic['Ranges_setup']['pub1.2_range'].split('-')
    for row in range(int(tem_arr[0]), int(tem_arr[1]) + 1):
        if (sheet.range('B' + str(row)).value):
            item = sheet.range('B' + str(row)).value.strip()
            hash_list = [gpf_tags_RSA['Q_UICS'], ShareTags, ShareTags_Q]
            tagValue = func.GetValFromDics(hash_list, item)
            if tagValue == '':
                log_writer.write('%s did not find any value\n' % item)
            else:
                sheet.range('E' + str(row)).value = tagValue
        else:
            log_writer.write('RowB%s can not read \n' % str(row))

    tem_arr = ConfigDic['Ranges_setup']['pub1.3_range'].split('-')
    row = int(tem_arr[0])
    sheet.range('F' + str(row)).value = TransactionKeysDic['MdkAc_3DES']
    sheet.range('F' + str(row + 2)).value = TransactionKeysDic['MdkMac_3DES']
    sheet.range('F' + str(row + 4)).value = TransactionKeysDic['MdkDek_3DES']
    if isSM4Data:
        sheet.range('F' + str(row + 1)).value = TransactionKeysDic['MdkAc_SM4']
        sheet.range('F' + str(row + 3)).value = TransactionKeysDic['MdkMac_SM4']
        sheet.range('F' + str(row + 5)).value = TransactionKeysDic['MdkDek_SM4']

    log_writer.write('......开始填写2借贷部分DC.......' + '\n')
    tem_arr1 = ConfigDic['Ranges_setup']['DC_range'].split(',')
    for temp in tem_arr1:
        tem_arr = temp.split('-')
        tag_cache = ''
        for row in range(int(tem_arr[0]), int(tem_arr[1]) + 1):
            log_writer.write('row %s start---\n' % str(row))
            if sheet.range('E' + str(row)).value:
                log_writer.write(sheet.range('E' + str(row)).value)
                if sheet.range('E' + str(row)).value.strip() == '国际':
                    item = sheet.range('B' + str(row)).value.strip()
                    hash_list = [gpf_tags_RSA['DC'], ShareTags, ShareTagsDC_ECC]
                    tagValue = func.GetValFromDics(hash_list, item)
                    if tagValue == '':
                        log_writer.write('%s did not find any value\n' % item)
                    else:
                        sheet.range('F' + str(row)).value = tagValue
                    tag_cache = item
                    log_writer.write('RSA tag %s fixed\n' % item)
                elif sheet.range('E' + str(row)).value.strip() == '国密':
                    if isSM4Data:
                        hash_list = [gpf_tags_SM4['DC']]
                        tagValue = func.GetValFromDics(hash_list, tag_cache)
                        if tagValue == '':
                            log_writer.write('%s did not find any value\n' % tag_cache)
                        else:
                            sheet.range('F' + str(row)).value = tagValue
                        log_writer.write('SM4 tag %s fixed\n' % tag_cache)
                    else:
                        continue
                else:
                    raise ValueError('E 列 数值 异常 %s' % str(row))
                log_writer.write(tag_cache + '\n')
            elif sheet.range('B' + str(row)).value:
                item = sheet.range('B' + str(row)).value.strip()
                hash_list = [gpf_tags_RSA['DC'], ShareTags, ShareTagsDC_ECC]
                tagValue = func.GetValFromDics(hash_list, item)
                if tagValue == '':
                    log_writer.write('%s did not find any value\n' % item)
                else:
                    sheet.range('E' + str(row)).value = tagValue
            else:
                continue
            log_writer.write('row' + str(row) + '---OK' + '\n')

    log_writer.write('......开始填写3小额支付部分ECC.......' + '\n')
    tem_arr1 = ConfigDic['Ranges_setup']['ECC_range'].split(',')
    for temp in tem_arr1:
        tem_arr = temp.split('-')
        tag_cache = ''
        for row in range(int(tem_arr[0]), int(tem_arr[1]) + 1):
            log_writer.write('row %s start---\n' % str(row))
            if sheet.range('E' + str(row)).value:
                if sheet.range('E' + str(row)).value.strip() == '国际':
                    item = sheet.range('B' + str(row)).value.strip()
                    print('fix item: %s' % item)
                    hash_list = [gpf_tags_RSA['ECC'], ShareTags, ShareTagsDC_ECC]
                    tagValue = func.GetValFromDics(hash_list, item)
                    if tagValue == '':
                        log_writer.write('%s did not find any value\n' % item)
                    else:
                        sheet.range('F' + str(row)).value = tagValue
                    tag_cache = item
                    log_writer.write('RSA tag: %s has been fixed\n' % item)
                elif sheet.range('E' + str(row)).value.strip() == '国密':
                    if isSM4Data:
                        hash_list = [gpf_tags_SM4['ECC']]
                        tagValue = func.GetValFromDics(hash_list, tag_cache)
                        if tagValue == '':
                            log_writer.write('%s did not find any value\n' % tag_cache)
                        else:
                            sheet.range('F' + str(row)).value = tagValue
                        log_writer.write('SM tag: %s has been fixed\n' % tag_cache)
                    else:
                        continue
                else:
                    log_writer.write('E 列 数值 异常 %s\n' % str(row))
                    print('E 列 数值 异常 %s' % str(row))
                    raise ValueError('E 列 数值 异常 %s' % str(row))
                log_writer.write(tag_cache + 'fixed\n')
            elif sheet.range('B' + str(row)).value:
                item = sheet.range('B' + str(row)).value.strip()
                print('fix item: %s' % item)
                hash_list = [gpf_tags_RSA['ECC'], ShareTags, ShareTagsDC_ECC]
                tagValue = func.GetValFromDics(hash_list, item)
                if tagValue == '':
                    log_writer.write('%s did not find any value\n' % item)
                else:
                    sheet.range('E' + str(row)).value = tagValue
                log_writer.write('%s fixed\n' % item)
            else:
                continue

    log_writer.write('......开始填写4快速借贷记部分qUICS/PBOC.......' + '\n')
    tem_arr1 = ConfigDic['Ranges_setup']['Q_range'].split(',')
    for temp in tem_arr1:
        tem_arr = temp.split('-')
        tag_cache = ''
        for row in range(int(tem_arr[0]), int(tem_arr[1]) + 1):
            log_writer.write('%s start-----\n' % str(row))
            if sheet.range('E' + str(row)).value:
                if sheet.range('E' + str(row)).value.strip() == '国际':
                    item = sheet.range('B' + str(row)).value.strip()
                    hash_list = [gpf_tags_RSA['Q_UICS'], ShareTags, ShareTags_Q]
                    tagValue = func.GetValFromDics(hash_list, item)
                    if tagValue == '':
                        log_writer.write('%s did not find any value\n' % item)
                    else:
                        sheet.range('F' + str(row)).value = tagValue
                    tag_cache = item
                    log_writer.write('RSA tag: %s has been fixed\n' % item)
                elif sheet.range('E' + str(row)).value.strip() == '国密':
                    if isSM4Data:
                        hash_list = [gpf_tags_SM4['Q_UICS']]
                        tagValue = func.GetValFromDics(hash_list, tag_cache)
                        if tagValue == '':
                            log_writer.write('%s did not find any value\n' % tag_cache)
                        else:
                            sheet.range('F' + str(row)).value = tagValue
                        log_writer.write('SM tag: %s has been fixed\n' % tag_cache)
                    else:
                        continue
                else:
                    raise ValueError('E 列 数值 异常 %s' % str(row))
                log_writer.write(tag_cache + '\n')
            elif sheet.range('B' + str(row)).value:
                item = sheet.range('B' + str(row)).value.strip()
                hash_list = [gpf_tags_RSA['Q_UICS'], ShareTags, ShareTags_Q]
                tagValue = func.GetValFromDics(hash_list, item)
                if tagValue == '':
                    log_writer.write('%s did not find any value\n' % item)
                else:
                    sheet.range('E' + str(row)).value = tagValue
                log_writer.write('%s fixed\n' % item)
            else:
                continue
            log_writer.write('row' + str(row) + '---OK' + '\n')

    if is_CAPP_data:
        log_writer.write('......获取CAPP数据.......' + '\n')
        appendKey = {}
        fileLenDic = {}
        CAPP_SFI = []
        initialData1E = ''
        initialData = ''
        managerKey = ''
        with open(CAPP_file, 'r') as source_file:
            lines = source_file.readlines()
        CAPPLineStart = False
        for line in lines:
            if 'var bsInitKeyArr = new Array();' in line:
                CAPPLineStart = True
                continue

            if 'var atc = card.sendApdu(0x80, 0xCA, 0x9F, 0X36,0x00, swok);' in line:
                CAPPLineStart = False
                continue

            if CAPPLineStart:
                # print(line)
                if line.find('bsInitKeyArr["') > 0:
                    # print('CAPP append Key')
                    line = line.replace('bsInitKeyArr["', '')
                    line = line.replace('\n', '').strip()
                    indexStart = line.find('("') + 2
                    appendKey[line[:2]] = line[indexStart:(indexStart + 32)]
                elif line.find('//sfi_list') > 0:
                    # print('//sfi_list' + line)
                    continue
                elif line.find('sfi_list') > 0:
                    # print('sfi_list' + line)
                    temp = line.split('"')[1]
                    print(temp)
                    tem_arr = temp.split(' ')
                    for sfi in tem_arr:
                        CAPP_SFI.append(sfi.strip())
                else:
                    print(line + 'continue')
                    continue

            if 'var bsManageKey = new ByteString("' in line:
                indexStart = line.find('("') + 2
                managerKey = line[indexStart:(indexStart + 32)]

            if 'var record_data = new ByteString("' in line:
                indexStart = line.find('("') + 2
                indexEnd = line.find('",HEX);')
                initialData = line[indexStart:indexEnd]

            if 'record_data = new ByteString("' in line:
                indexStart = line.find('("') + 2
                indexEnd = line.find('",HEX);')
                initialData1E = line[indexStart:indexEnd]

        log_writer.write('......开始填写5快速借贷记部分扩展应用CAPP.......' + '\n')
        # format check
        if len(initialData) != 44:
            raise ValueError('initialData length Err!')
        if len(initialData1E) != 128:
            raise ValueError('1E record len Err!')
        if len(managerKey) != 32:
            raise ValueError('managerKey length error! ')

        hash_list = [gpf_tags_RSA['Q_UICS'], ShareTags, ShareTags_Q]
        tem_arr = ConfigDic['Ranges_setup']['DF62_row'].split('-')
        row = tem_arr[0]
        sheet.range('E' + row).value = func.GetValFromDics(hash_list, 'DF62')
        # prepare CAPP file length from DGIB001-D3
        B001Dic = {}
        if 'DGIB001' in DGIValDic.keys():
            log_writer.write('解析B001.......' + '\n')
            # B001 tags
            func.ToTlvFormat(DGIValDic['DGIB001'][6:], B001Dic)
            if 'D3' in B001Dic.keys():
                temp = B001Dic['D3']
                if len(temp) % 10 != 0:
                    log_writer.write('D3 = ' + temp)
                    raise ValueError('B001 length error ')
                log_writer.write('...解析D3中的 文件长度' + '\n')
                i = 0
                while i < len(temp):
                    CAPPFileLen = hex(int(temp[6:10], 16)).replace('0x', '').upper()
                    # log_writer.write(temp[:2])
                    # log_writer.write(CAPPFileLen)
                    fileLenDic[temp[:2]] = CAPPFileLen
                    temp = temp[10:]
            else:
                print('B001 中不含D3，请手动填写CAPP file length')
        else:
            print('B001 不存在，请手动填写CAPP file length')

        if '1E' not in CAPP_SFI:
            CAPP_SFI.append('1E')
        print('需要填充的CAPP SFI：')
        print(CAPP_SFI)
        tem_arr = ConfigDic['Ranges_setup']['CAPP_range'].split('-')
        index = int(tem_arr[0])
        while index < (int(tem_arr[1]) - 1):
            if sheet.range('A' + str(index)).value:
                sfi = sheet.range('A' + str(index)).value.strip()
                log_writer.write(sfi + '\n')
                sfi = sfi[len(sfi) - 2:]
                if sfi in CAPP_SFI:
                    print('开始填充 %s \n' % sfi)
                    if sfi in appendKey.keys():
                        if len(appendKey[sfi]) != 32:
                            raise ValueError('append Key len error! ')
                        sheet.range('E' + str(index)).value = appendKey[sfi]
                    # print('CAPP debug 1')
                    # print(fileLenDic.keys())
                    if sfi in fileLenDic.keys():
                        sheet.range('E' + str(index + 1)).value = fileLenDic[sfi]
                    # print('CAPP debug 2')
                    if sfi != '1E':
                        sheet.range('E' + str(index + 2)).value = initialData
                    else:
                        sheet.range('E' + str(index + 2)).value = initialData1E
                    sheet.range('E' + str(index + 3)).value = managerKey
                    log_writer.write('row: ' + str(index) + '  sfi = ' + sfi + ' OK' + '\n')
                else:
                    print(' %s did not append' % sfi)
                index = index + 4
            else:
                log_writer.write('Excel 表格读取 CAPP 信息错误！ \n')
                raise ValueError('Excel 表格读取 CAPP 信息错误！')

        if "1E" in fileLenDic.keys():
            sheet.range('E' + tem_arr[1]).value = str(int(fileLenDic['1E'], 16) // 64)
        else:
            log_writer.write('1E file lenght missing \n')

    finalxlsm = 'PBOCUICS应用个人化信息表_GD'
    finalxlsm = finalxlsm + '_' + ConfigDic['Head_setup']['卡片名称'].replace('卡', '')
    finalxlsm = finalxlsm + '_' + ConfigDic['Head_setup']['芯片商及型号']
    finalxlsm = finalxlsm + '_' + ConfigDic['Head_setup']['BIN号']

    wb.save(finalxlsm)
    wb.close()
    app.quit()

    Tag9F0E = gpf_tags_RSA['DC']['9F0E']  # IAC 拒绝
    Tag9F0F = gpf_tags_RSA['DC']['9F0F']  # IAC 联机
    Tag9F0D = gpf_tags_RSA['DC']['9F0D']  # IAC 缺省
    log_writer.write('AID = %s \n' % AID)
    log_writer.write('Tag9F0E = %s \n' % Tag9F0E)
    log_writer.write('Tag9F0F = %s \n' % Tag9F0F)
    log_writer.write('Tag9F0D = %s \n' % Tag9F0D)
    UICStemplate = func.checkUICTemplate(Tag9F0E, Tag9F0F, Tag9F0D, AID)
    log_writer.write('个人化模板X编号为 = %s \n' % UICStemplate)
    log_writer.write('处理结束，生成的xlsm为： %s \n' % finalxlsm)
    log_writer.close()
    tkinter.messagebox.showinfo('', '%s \n请继续补充其他内容，并检查保存！' % UICStemplate)
# except:
#    log_writer.write('处理失败！')
finally:
    if log_writer:
        log_writer.close()
    if app:
        app.quit()
    # user = input("press any key to exit: ")
    sys.exit()
