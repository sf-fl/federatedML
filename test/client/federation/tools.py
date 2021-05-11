


def write_detail(id,text,mod):
    with open(r'./client/data_storage/train_detail_%s.log' % id, mod, encoding='UTF-8') as f1:
        f1.write(text)