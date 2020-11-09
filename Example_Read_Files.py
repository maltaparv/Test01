# Read Files
# sys.stdin
# sys.stdin
# sys.stderr

# f = open("D:\\TempData\data01.txt", 'w')
# f.write("test line 1\n")
# f.write("test line 2\n")
# f.close()
#
# f = open("D:\\TempData\data02.txt", 'a')
# try:
#     f.write("- line 1\n")
#     f.write("- line 2\n")
# finally:
#     f.close()
#
# with open("D:\\TempData\data03.txt", 'a') as f:  # менеджер контекста
#     f.write("line - 1\n")
#     f.write('line - 2\n')
#
# f1 = open("D:\\TempData\data04.txt", 'a')
# f1.writelines(["111\n", "2222\n"])
# f1.close()

f1 = open('D:\\TempData\data04.txt', 'r')
print(f1.read())   # читать всё
# print(f1.read(1))   # читать первый символ
# print(f1.readline())  # читать построчно
# f1.seek(8)  # позиция чтения файла
# print(f1.readlines())  # читать целиком ['111\n', '2222\n', '111\n', '2222\n']
# for line in f1:
#     print(line, end='')

# for line in open('D:\\TempData\data01.txt'):
#     print(line, end='')  # после выполнения кода этот временный файл автоматически закрывается

# fin = open('D:\\TempData\data01.txt')
# buf = fin.readlines()
# fin.close()
# buf.sort()
# fout=open('D:\\TempData\data_sort.txt', 'w')
# for line in buf:
#     fout.write(line)
#     print(line, end='')
# fout.close()

f = open('D:\\TempData\\data_words.txt')
content = f.read()
f.close()
words = content.split()
print(words, end='\n')
print('Количество слов в файле: {0}.'.format(len(words)))
