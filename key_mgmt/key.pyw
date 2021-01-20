# @Time    : 2021/1/11 18:16
# @Author  : Rainbird
# @Email   : 731465297@qq.com
# @File    : key.py
# @Describe: 给我妈用来查钥匙的

import xlrd, tkinter as tk, re
FileName = 'key.xlsx'
TableName = 'key'
area = ('', 'A区', 'B区', 'C区', 'D区', 'E区', 'F区', 'G区', '移交财务')

class Key:

    def __init__(self):
        self.FileName = FileName
        self.TableName = TableName
        self.form = xlrd.open_workbook((self.FileName), encoding_override='utf-8')
        self.table = self.form.sheet_by_name(self.TableName)

    def select(self, target):
        for i in range(self.table.nrows):
            for j in range(self.table.ncols):
                if str(self.table.cell_value(i, j)).strip() == target:
                    return (
                     area[i], j)

    def count(self):
        k = 0
        for i in range(self.table.nrows):
            for j in range(self.table.ncols):
                # if not re.match('^\s*$', str(self.table.cell_value(i, j)).strip()):
                if str(self.table.cell_value(i, j)).strip() != '':
                  k += 1
        return (k -39)


class Window:

    def __init__(self):
        self.window = tk.Tk()
        self.table = Key()
        self.msg = tk.StringVar()
        self.window.title('钥匙查询系统')
        self.window.geometry('550x200')
        self.num = tk.Label((self.window), font=25, text='当前仓库钥匙数：{} 把'.format(self.table.count()))
        self.num.pack()
        self.note = tk.Label((self.window), font=25, text='请输入要查询的钥匙编号：')
        self.note.pack()
        self.entry = tk.Entry((self.window), bd=4, width=20, font=14)
        self.entry.pack()
        self.button = tk.Button((self.window), font=40, height=1, text='查询', command=(self.filter))
        self.button.pack()
        self.label = tk.Label((self.window), font=30, textvariable=(self.msg))
        self.label.pack()

    def filter(self):
        text = str(self.entry.get()).strip()
        if not re.match('^\\d{6}\\s*$', text):
            self.msg.set('钥匙号码格式错误！请检查后重新输入！')
        else:
            array = self.table.select(text)
            if array:
                self.msg.set('{} 钥匙位于 {} 第 {} 列'.format(text, array[0], array[1]))
            else:
                if not array:
                    self.msg.set('没有找到 {} 这把钥匙！请仔细核对后查询！'.format(text))


if __name__ == '__main__':
    b = Window()
    b.window.mainloop()
