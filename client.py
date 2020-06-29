# -*- coding:utf-8 -*-
from xmlrpc.client import ServerProxy
import xmlrpc.client
import tkinter
from tkinter import filedialog, Tk, StringVar, Label, Listbox, Button, Canvas
import os
import tkinter.messagebox
from ip_dict import ips_dict
from concurrent.futures import ThreadPoolExecutor
from threading import Lock
from functools import partial

# import traceback

pool = ThreadPoolExecutor(max_workers=10)
lock = Lock()


class Xpc:
    def __init__(self, ip, files, long_folder_path):
        self.long_folder_path = long_folder_path
        self.ip = ip
        self.files = files
        self.server = self.init_server(self.ip)

    def put_file(self):
        for file_path in self.files:
            local_file_name = os.path.basename(file_path)
            long_file_path = os.path.join(self.long_folder_path, local_file_name)

            # 调用远程服务,上传文件
            with open(file_path, 'rb') as put_handle:
                self.server.file_put(long_file_path, xmlrpc.client.Binary(put_handle.read()))

    @staticmethod
    def init_server(ip):
        server = ServerProxy(r"http://%s:8888" % ip, allow_none=True)
        return server


class Gui:
    canvas: Canvas
    get_file_start: None
    path_long: Listbox
    label_long: Label
    path_local: Listbox
    label_local: Label
    file: StringVar
    bn_jp: Button
    bn_clear: Button
    get_file_local: None
    bn_uk: Button
    long_file_path: StringVar
    bt2_all: Button
    bt1_all: Button
    bn_us: Button
    lb2_ip: Listbox
    lb1_ip: Listbox
    lb2: Label
    lb1: Label
    checked_ips: StringVar
    ip: StringVar
    tk: Tk

    def __init__(self, all_ips_dict):
        self.ips = all_ips_dict
        self.checked_ips_dict = {}
        self.checked_ips_path_dict = {}
        self.finished_task_count = 0
        self.failed_task_list = []

    # 点击按钮后,右侧服务器列表向左移动
    def left_ip(self, envent):
        checked_ip_index = self.lb2_ip.curselection()
        if not checked_ip_index:
            tkinter.messagebox.showinfo(title='卧槽', message="求求你选一个服务器吧!")
            return

        if len(checked_ip_index) > 1:
            for x in checked_ip_index[::-1]:
                checked_ip = self.lb2_ip.get(x)
                self.checked_ips_dict.pop(checked_ip)
                self.lb2_ip.delete(x)
                self.lb1_ip.insert(tkinter.END, checked_ip)
            self.bt2_all["bg"] = "white"

        else:
            checked_ip = self.lb2_ip.get(checked_ip_index)

            self.checked_ips_dict.pop(checked_ip)
            self.lb2_ip.delete(checked_ip_index)
            self.lb1_ip.insert(tkinter.END, checked_ip)
        self.lb1.configure(text="服务器:  " + str(self.lb1_ip.size()) + "\000\000\000" * 4)
        self.lb2.configure(text="选中要上传的服务器： " + str(self.lb2_ip.size()))
        self.reload_path()

    # 点击按钮后,左侧服务器列表向右移动
    def rgt_ip(self, envent):
        checked_ip_index = self.lb1_ip.curselection()
        if not checked_ip_index:
            tkinter.messagebox.showinfo(title='卧槽', message="求求你选一个服务器吧!")
            return

        if len(checked_ip_index) > 1:
            for x in checked_ip_index[::-1]:
                checked_ip = self.lb1_ip.get(x)
                self.checked_ips_dict.update({checked_ip: self.ips.get(checked_ip)})
                self.lb1_ip.delete(x)
                self.lb2_ip.insert(tkinter.ACTIVE, checked_ip)
            self.bt1_all["bg"] = "white"
        else:
            checked_ip = self.lb1_ip.get(checked_ip_index)
            self.checked_ips_dict.update({checked_ip: self.ips.get(checked_ip)})
            self.lb1_ip.delete(checked_ip_index)
            self.lb2_ip.insert(tkinter.END, checked_ip)
        self.lb1.configure(text="服务器:  " + str(self.lb1_ip.size()) + "\000\000\000" * 4)
        self.lb2.configure(text="选中要上传的服务器： " + str(self.lb2_ip.size()))
        self.reload_path()

    # 服务器列表的全选功能
    def bt_checked_all(self, button_number):
        if button_number == 1:
            lb_ip = self.lb1_ip
            bt_all = self.bt1_all
        elif button_number == 2:
            lb_ip = self.lb2_ip
            bt_all = self.bt2_all
        else:
            raise ValueError("fuck!")

        if len(lb_ip.get(0, tkinter.END)) >= 1:
            if not bt_all['bg'] == "red":
                bt_all['bg'] = "red"
                lb_ip.select_set(0, tkinter.END)
            else:
                bt_all['bg'] = "white"
                lb_ip.select_clear(0, tkinter.END)
        else:
            bt_all['bg'] = "white"

    # 点击路径按钮后,生成对应的路径
    def bn_path(self, country):

        if country == 'us':
            current_button = self.bn_us
        elif country == 'uk':
            current_button = self.bn_uk
        elif country == 'jp':
            current_button = self.bn_jp
        else:
            raise ValueError("fuck you !")

        self.bn_us["fg"] = "black"
        self.bn_uk["fg"] = "black"
        self.bn_jp["fg"] = "black"

        # 删除路径
        self.path_long.delete(0, tkinter.END)
        self.checked_ips_path_dict.clear()

        # 取消所有选择的路径
        if current_button["fg"] == "red":
            current_button["fg"] = "black"

        else:
            current_button["fg"] = "red"

            # 添加路径
            for x in self.checked_ips_dict.keys():
                self.checked_ips_path_dict.update({x: self.checked_ips_dict.get(x).get(country)})
                self.path_long.insert(tkinter.END, x + " ----> " + self.checked_ips_dict.get(x).get(country))
        self.label_long.configure(text="远程文件路径： " + str(self.path_long.size()))

    # 重新加载需要上传的文件路径列表
    def reload_path(self):
        if self.bn_uk["fg"] == "red":
            country = 'uk'
        elif self.bn_us["fg"] == "red":
            country = 'us'
        elif self.bn_jp["fg"] == "red":
            country = 'jp'
        else:
            return

        # 先删除路径
        self.path_long.delete(0, tkinter.END)
        self.checked_ips_path_dict.clear()

        # 添加路径
        for x in self.checked_ips_dict.keys():
            self.checked_ips_path_dict.update({x: self.checked_ips_dict.get(x).get(country)})
            self.path_long.insert(tkinter.END, x + " ----> " + self.checked_ips_dict.get(x).get(country))
        self.label_long.configure(text="远程文件路径： " + str(self.path_long.size()))

    # 右键删除文件时使用
    def menu_func(self):
        files = self.path_local.curselection()
        if not files:
            tkinter.messagebox.showwarning(title='卧槽', message="你TM先选中一个再删好吗!")
            return

        if len(files) > 1:
            for x in files[::-1]:
                self.path_local.delete(x)  # 删除选中数据
                self.label_local.configure(text="本地上传文件： " + str(self.path_local.size()))
        else:
            self.path_local.delete(self.path_local.curselection())  # 删除选中数据
            self.label_local.configure(text="本地上传文件： " + str(self.path_local.size()))

    # 获取本地需要上传的文件路径
    def get_file_path(self):
        file_name_local = filedialog.askopenfilenames()
        if not file_name_local:
            return

        for file in file_name_local:
            if file not in self.path_local.get(0, tkinter.END):
                self.path_local.insert(tkinter.END, file)

                self.label_local.configure(text="本地上传文件： " + str(self.path_local.size()))

    # 调用远程服务,传输文件
    def put_file_to_long(self):
        files = self.path_local.get(0, tkinter.END)

        if not self.checked_ips_dict.keys():
            tkinter.messagebox.showinfo(title='卧槽', message="你是不是没选服务器!")
            return

        if not files:
            tkinter.messagebox.showinfo(title='卧槽', message="你是不是没选文件!")
            return

        if not self.checked_ips_path_dict.keys():
            tkinter.messagebox.showinfo(title='卧槽', message="告诉我上传到哪好吗!")
            return

        for ip in self.checked_ips_dict.keys():
            long_folder_path = self.checked_ips_path_dict.get(ip)
            put_file_obj = Xpc(ip, files, long_folder_path)

            # 换成多线程
            future = pool.submit(put_file_obj.put_file)
            # 把机器的host存进去,可以在结果里取出来
            future.task_ip = ip

            future.add_done_callback(self.fill_progress_bar)

    # 填充进度条
    def fill_progress_bar(self, future):
        try:
            future.result()
        except Exception as e:
            # error_msg = traceback.format_exc()
            tmp_str = f'{future.task_ip}: {e}\n'
            self.failed_task_list.append(tmp_str)

        x = 660  # 进度条的长度

        # 进度条填满的次数 = 所有任务总数
        fill_times = len(self.checked_ips_dict.keys())

        # 每次需要填充多少
        step_len = x / fill_times

        with lock:
            self.finished_task_count += 1
            # 最后一个完成时任务,变为红色,并显示所有失败任务的上传结果
            if self.finished_task_count == fill_times:
                fill_line = self.canvas.create_rectangle(0, 0, 0, 23, width=0, fill="red")
                error_msg = "".join(self.failed_task_list)
                self.canvas.coords(fill_line, (0, 0, step_len * self.finished_task_count, 23))
                self.tk.update()
                tkinter.messagebox.showerror(title='上传失败', message=error_msg)
            else:
                fill_line = self.canvas.create_rectangle(0, 0, 0, 23, width=0, fill="green")

                self.canvas.coords(fill_line, (0, 0, step_len * self.finished_task_count, 23))
                self.tk.update()

    # 清空所有选框
    def clear_all(self):
        # 清空进度条
        fill_line = self.canvas.create_rectangle(0, 0, 0, 23, width=0, fill="white")
        x = 660
        self.canvas.coords(fill_line, (0, 0, x, 23))

        # 清空远程文件路径
        self.path_long.delete(0, tkinter.END)
        self.checked_ips_path_dict.clear()

        self.checked_ips_dict.clear()
        self.label_long.configure(text="远程文件路径： " + str(self.path_long.size()))

        # 清空要上传的文件
        self.path_local.delete(0, tkinter.END)  # 删除选中数据
        self.label_local.configure(text="本地上传文件： " + str(self.path_local.size()))

        # 清空要上传的服务器
        self.lb2_ip.delete(0, tkinter.END)
        self.lb2.configure(text="本地上传文件： " + str(self.path_local.size()))

        # 恢复所有可选服务器列表
        self.lb1_ip.delete(0, tkinter.END)
        for ip in self.ips.keys():
            self.lb1_ip.insert(tkinter.END, ip)
        self.lb1.configure(text="服务器:  " + str(self.lb1_ip.size()) + "\000\000\000" * 4)

        # 刷新window
        self.tk.update()

    def creat_gui(self):
        tk = tkinter.Tk()
        tk.title("上传文件器")
        self.tk = tk

        # 防止用户调整尺寸
        tk.resizable(False, False)

        sw = tk.winfo_screenwidth()
        sh = tk.winfo_screenheight()
        ww = 800
        wh = 500
        x = (sw - ww) / 2
        y = (sh - wh) / 2
        tk.geometry("%dx%d+%d+%d" % (ww, wh, x, y))

        frm_top1 = tkinter.Frame(tk)
        frm_top1.pack(anchor=tkinter.NW, padx=60)
        # ip-listbox
        # 左边
        self.ip = tkinter.StringVar()
        self.checked_ips = tkinter.StringVar()

        frm1 = tkinter.Frame(frm_top1)
        frm_lb1 = tkinter.Frame(frm1)
        frm_lb1.pack(side=tkinter.TOP, anchor=tkinter.W)

        self.lb1 = tkinter.Label(frm_lb1, text="服务器:")
        # self.bt1_all = tkinter.Button(frm_lb1, text="全选", command=self.bt1_checked_all, bg="white")
        self.lb1_ip = tkinter.Listbox(frm1, selectmode=tkinter.EXTENDED, listvariable=self.ip, width=25, height=8,
                                      highlightbackground="green", bd=1)

        # tmp_fun_bt_1 = partial(self.bt_checked_all, self.lb1_ip, self.bt1_all)
        tmp_fun_bt_1 = partial(self.bt_checked_all, 1)
        tmp_fun_bt_2 = partial(self.bt_checked_all, 2)

        self.bt1_all = tkinter.Button(frm_lb1, text="全选", command=tmp_fun_bt_1, bg="white")

        self.bt1_all.grid(row=0, column=1, sticky=tkinter.E, padx=10)
        self.lb1.grid(row=0, column=0, sticky=tkinter.W)

        for ip in self.ips.keys():
            self.lb1_ip.insert(tkinter.END, ip)
        self.lb1.configure(text="服务器:  " + str(self.lb1_ip.size()) + "\000\000\000" * 4)
        self.lb1_ip.pack(side=tkinter.LEFT, anchor=tkinter.NE, pady=5)

        # 滚动条
        sc = tkinter.Scrollbar(frm1)
        sc.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.lb1_ip.configure(yscrollcommand=sc.set)
        # 额外属性赋值
        sc["command"] = self.lb1_ip.yview()
        frm1.pack(side=tkinter.LEFT, anchor=tkinter.NE, padx=10, pady=10)

        # 中间操作图标
        frm3 = tkinter.Frame(frm_top1)
        image_left = tkinter.PhotoImage(file="./left.png")
        lb3_1 = tkinter.Label(frm3, image=image_left)
        lb3_1.bind("<Button-1>", self.left_ip)
        lb3_1.pack(anchor=tkinter.CENTER, side=tkinter.BOTTOM)
        image_rgt = tkinter.PhotoImage(file="./rgt.png")
        lb3_2 = tkinter.Label(frm3, image=image_rgt)
        lb3_2.bind("<Button-1>", self.rgt_ip)
        lb3_2.pack(anchor=tkinter.S, side=tkinter.BOTTOM, pady=10)
        frm3.pack(side=tkinter.LEFT, anchor=tkinter.NE, pady=60)

        # 右边
        frm2 = tkinter.Frame(frm_top1)
        frm_lb2 = tkinter.Frame(frm2)
        frm_lb2.pack(side=tkinter.TOP, anchor=tkinter.NW)
        self.lb2 = tkinter.Label(frm_lb2, text="选中要上传的服务器：")
        self.bt2_all = tkinter.Button(frm_lb2, text="全选", command=tmp_fun_bt_2, bg="white")
        self.bt2_all.grid(row=0, column=1, padx=5)
        self.lb2.grid(row=0, column=0)
        self.lb2_ip = tkinter.Listbox(frm2, selectmode=tkinter.EXTENDED, listvariable=self.checked_ips, width=25,
                                      height=8,
                                      highlightbackground="green", bd=1)
        self.lb2_ip.pack(side=tkinter.LEFT, anchor=tkinter.NE, pady=5)
        self.lb2.configure(text="选中要上传的服务器： " + str(self.lb2_ip.size()))
        # 滚动条
        sc2 = tkinter.Scrollbar(frm2)
        sc2.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.lb2_ip.configure(yscrollcommand=sc2.set)
        # 额外属性赋值
        sc2["command"] = self.lb2_ip.yview()
        frm2.pack(side=tkinter.LEFT, anchor=tkinter.NE, padx=20, pady=10)

        # 文件路径
        self.long_file_path = tkinter.StringVar()
        frm4 = tkinter.Frame(frm_top1)
        lb4 = tkinter.Label(frm4, text="选择上传服务器文件路径")
        lb4.grid(row=0, columnspan=2, padx=5, pady=0)

        bn_path_na = partial(self.bn_path, "us")
        bn_path_europe = partial(self.bn_path, "uk")
        bn_path_jp = partial(self.bn_path, "jp")

        self.bn_us = tkinter.Button(frm4, text="路径1", command=bn_path_na, font=('黑体', 15, 'bold'), fg="black")
        self.bn_us.grid(row=1, column=0, padx=5, pady=10)

        self.bn_uk = tkinter.Button(frm4, text="路径3", command=bn_path_europe, font=('黑体', 15, 'bold'), fg="black")
        self.bn_uk.grid(row=2, column=0, padx=5, pady=10)

        self.bn_clear = tkinter.Button(frm4, text="重 置", command=self.clear_all, font=('黑体', 15, 'bold'),
                                       fg="black")
        self.bn_clear.grid(row=2, column=1, padx=5, pady=10)

        self.bn_jp = tkinter.Button(frm4, text="路径2", command=bn_path_jp, font=('黑体', 15, 'bold'), fg="black")
        self.bn_jp.grid(row=1, column=1, padx=10, pady=10)
        frm4.pack(side=tkinter.RIGHT, anchor=tkinter.NE, padx=20, pady=10)

        # 本地文件选择
        frm5 = tkinter.Frame(tk)
        self.file = tkinter.StringVar()

        # 本地文件路径
        self.label_local = tkinter.Label(frm5, text="本地上传文件：")
        self.label_local.grid(column=0, row=0, sticky=tkinter.W, padx=10)
        self.path_local = tkinter.Listbox(frm5, selectmode=tkinter.EXTENDED,
                                          listvariable=self.file, width=50, height=8,
                                          highlightbackground="green", bd=1)

        self.path_local.grid(column=0, row=1, padx=10, pady=5)
        self.label_local.configure(text="本地上传文件： " + str(self.path_local.size()))

        # 滚动条
        sc3 = tkinter.Scrollbar(frm5)
        sc3.grid(column=1, row=1, sticky=tkinter.N + tkinter.S)
        self.path_local.configure(yscrollcommand=sc3.set)
        # 额外属性赋值
        sc3["command"] = self.path_local.yview("moveto", 1.0)

        # 本地路径文件添加右键删除菜单
        menu = tkinter.Menu(self.path_local, tearoff=False)
        menu.add_command(label="删除", command=self.menu_func)

        self.path_local.bind("<Button-3>", lambda event: menu.post(event.x_root, event.y_root))
        self.get_file_local = tkinter.Button(frm5, text="添加本地文件", command=self.get_file_path, font=('黑体', 10, 'bold'),
                                             fg="black").grid(column=0, row=2, padx=10, pady=20)

        # 路径文件远程
        self.label_long = tkinter.Label(frm5, text="远程文件路径：")
        self.label_long.grid(column=2, row=0, sticky=tkinter.W, padx=10)
        self.path_long = tkinter.Listbox(frm5, selectmode=tkinter.EXTENDED, listvariable=self.long_file_path, width=35,
                                         height=8, highlightbackground="green", bd=1)
        self.path_long.grid(column=2, row=1, padx=10, pady=5)
        self.label_long.configure(text="远程文件路径： " + str(self.path_long.size()))
        # 滚动条
        sc4 = tkinter.Scrollbar(frm5)
        sc4.grid(column=3, row=1, sticky=tkinter.N + tkinter.S)
        self.path_long.configure(yscrollcommand=sc4.set)
        # 额外属性赋值
        sc4["command"] = self.path_long.yview("moveto", 1.0)

        self.get_file_start = tkinter.Button(frm5, text="开始上传", command=self.put_file_to_long, font=('黑体', 10, 'bold'),
                                             fg="black").grid(column=2, row=2, padx=10, pady=20)
        frm5.pack(side=tkinter.TOP, anchor=tkinter.NW, padx=60, pady=30)
        # ##########################################

        # 设置下载进度条
        # tkinter.Label(tk, text='上传进度:', ).place(x=70, y=200)
        self.canvas = tkinter.Canvas(tk, width=650, height=22, bg="white")
        self.canvas.place(x=70, y=200)

        # ##########################################
        # 主窗口循环
        tk.mainloop()


if __name__ == '__main__':
    run = Gui(ips_dict)
    run.creat_gui()
