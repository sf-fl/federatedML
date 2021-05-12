


def write_detail(id,text,mod):
    with open(r'./client/data_storage/train_detail_%s.log' % id, mod, encoding='UTF-8') as f:
        if mod != 'r+':
            f.write(text)
        else:
            old = f.read()
            f.seek(0)
            f.write(text)
            f.write(old)
