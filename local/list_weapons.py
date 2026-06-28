import os
p='local/weapons_db'
for fn in sorted(os.listdir(p)):
    if 'レ' in fn or 'レー' in fn or 'ヴ' in fn:
        print(repr(fn))
print('--- total files:', len(os.listdir(p)))
