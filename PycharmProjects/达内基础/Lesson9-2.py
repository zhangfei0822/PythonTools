# 模拟cp 操作
# 创建 cp.py 文件
# 将 /bin/ls “拷贝” 到 /root/目录下
# 要求读取 /bin/ls 后， 每次读取4096 字节， 依次写入到新文件
# 不要修改原始文件
def copy(src_fname, dst_fname):
    src_fobj = open(src_fname, 'rb')
    dst_fobj = open(dst_fname, 'wb')
    while True:
        data = src_fobj.read(4096)  # 防止内存溢出
        # if data == '':  # python2
        # if len(data) == 0:
        if not data:
            break
        dst_fobj.write(data)

    src_fobj.close()
    dst_fobj.close()


src_fname = 'lesson8.log'
dst_fname = 'lesson8-2.txt'
copy(src_fname, dst_fname)
# copy(sys.argv[1], sys.argv[2]) # obtain Linux cmd position arguments
