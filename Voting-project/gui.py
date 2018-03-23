import tkinter as tk
window = tk.Tk()
window.title("Voter Modeling")
window.geometry('500x500')


def hit_me():
    global on_hit
    if on_hit == False:  # 从 False 状态变成 True 状态
        on_hit = True
        var.set('you hit me')  # 设置标签的文字为 'you hit me'
    else:  # 从 True 状态变成 False 状态
        on_hit = False
        var.set('')  # 设置 文字为空


def insert_point():
    var = e.get()
    t.insert('insert', var)


def insert_end():
    var = e.get()
    t.insert('end', var)


l = tk.Label(
    window,
    text='OMG! this is TK!',  # 标签的文字
    bg='green',  # 背景颜色
    font=('Arial', 12),  # 字体和字体大小
    width=15,
    height=2  # 标签长宽
)
l.pack()  # 固定窗口位置

var = tk.StringVar()  # 这时文字变量储存器
l = tk.Label(
    window,
    textvariable=var,  # 使用 textvariable 替换 text, 因为这个可以变化
    bg='green',
    font=('Arial', 12),
    width=15,
    height=2)
l.pack()

on_hit = False  # 默认初始状态为 False
b = tk.Button(
    window,
    text='hit me',  # 显示在按钮上的文字
    width=15,
    height=2,
    command=hit_me)  # 点击按钮式执行的命令
b.pack()  # 按钮位置
#Enter and Exit text
b1 = tk.Button(
    window, text="insert point", width=15, height=2, command=insert_point)
b1.pack()

b2 = tk.Button(window, text="insert end", command=insert_end)
b2.pack()

e = tk.Entry(window, show='*')
e.pack()

t = tk.Text(window, height=2)
t.pack()
window.mainloop()