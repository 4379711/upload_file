# -*- coding:utf-8 -*-
from xmlrpc.client import ServerProxy
import xmlrpc.client
import tkinter
from tkinter import filedialog
import os
import tkinter.messagebox
from ip_dict import ips_dict


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

            # 上传文件
            with open(file_path, 'rb') as put_handle:
                self.server.file_put(long_file_path, xmlrpc.client.Binary(put_handle.read()))

    @staticmethod
    def init_server(ip):
        server = ServerProxy(r"http://%s:8888" % ip, allow_none=True)
        return server


class Gui:
    def __init__(self, all_ips_dict):
        self.ips = all_ips_dict
        self.checked_ips_dict = {}
        self.checked_ips_path_dict = {}

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
            self.lb1.configure(text="服务器:  " + str(self.lb1_ip.size()) + "\000\000\000" * 4)
            self.lb2.configure(text="选中要上传的服务器： " + str(self.lb2_ip.size()))

        else:
            checked_ip = self.lb2_ip.get(checked_ip_index)
            del self.checked_ips_dict[checked_ip]
            self.lb2_ip.delete(checked_ip_index)
            self.lb1_ip.insert(tkinter.END, checked_ip)
            self.lb1.configure(text="服务器:  " + str(self.lb1_ip.size()) + "\000\000\000" * 4)
            self.lb2.configure(text="选中要上传的服务器： " + str(self.lb2_ip.size()))

    def bt1_checked_all(self):
        if len(self.lb1_ip.get(0, tkinter.END)) >= 1:
            if not self.bt1_all['bg'] == "red":
                self.bt1_all['bg'] = "red"
                self.lb1_ip.select_set(0, tkinter.END)
            else:
                self.bt1_all['bg'] = "white"
                self.lb1_ip.select_clear(0, tkinter.END)
        else:
            self.bt1_all['bg'] = "white"

    def bt2_checked_all(self):
        if len(self.lb2_ip.get(0, tkinter.END)) >= 1:
            if not self.bt2_all['bg'] == "red":
                self.bt2_all['bg'] = "red"
                self.lb2_ip.select_set(0, tkinter.END)
            else:
                self.bt2_all['bg'] = "white"
                self.lb2_ip.select_clear(0, tkinter.END)
        else:
            self.bt2_all['bg'] = "white"

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
            self.lb1.configure(text="服务器:  " + str(self.lb1_ip.size()) + "\000\000\000" * 4)
            self.lb2.configure(text="选中要上传的服务器： " + str(self.lb2_ip.size()))
        else:
            checked_ip = self.lb1_ip.get(checked_ip_index)
            self.checked_ips_dict.update({checked_ip: self.ips.get(checked_ip)})
            self.lb1_ip.delete(checked_ip_index)
            self.lb2_ip.insert(tkinter.END, checked_ip)
            self.lb1.configure(text="服务器:  " + str(self.lb1_ip.size()) + "\000\000\000" * 4)
            self.lb2.configure(text="选中要上传的服务器： " + str(self.lb2_ip.size()))

    def bn_path_na(self):
        if self.bn_us["fg"] == "red":
            # 前景色处理
            self.bn_us["fg"] = "black"
            self.bn_uk["fg"] = "black"
            self.bn_jp["fg"] = "black"
            # 删除路径
            self.path_long.delete(0, tkinter.END)
            self.checked_ips_path_dict.clear()
            self.label_long.configure(text="远程文件路径： " + str(self.path_long.size()))
        else:
            # 删除路径
            self.path_long.delete(0, tkinter.END)
            self.checked_ips_path_dict.clear()
            self.bn_us["fg"] = "red"
            self.bn_uk["fg"] = "black"
            self.bn_jp["fg"] = "black"
            # 添加路径
            for x in self.checked_ips_dict.keys():
                self.checked_ips_path_dict.update({x: self.checked_ips_dict.get(x).get("us")})
                self.path_long.insert(tkinter.END, x + "\000\000\000\000" + self.checked_ips_dict.get(x).get("us"))
            self.label_long.configure(text="远程文件路径： " + str(self.path_long.size()))

    def bn_path_jp(self):
        if self.bn_jp["fg"] == "red":
            self.bn_us["fg"] = "black"
            self.bn_uk["fg"] = "black"
            self.bn_jp["fg"] = "black"
            # 删除路径
            self.path_long.delete(0, tkinter.END)
            self.checked_ips_path_dict.clear()
            self.label_long.configure(text="远程文件路径： " + str(self.path_long.size()))
        else:
            # 删除路径
            self.path_long.delete(0, tkinter.END)
            self.checked_ips_path_dict.clear()
            self.bn_jp["fg"] = "red"
            self.bn_uk["fg"] = "black"
            self.bn_us["fg"] = "black"
            # 添加路径
            for x in self.checked_ips_dict.keys():
                self.checked_ips_path_dict.update({x: self.checked_ips_dict.get(x).get("jp")})
                self.path_long.insert(tkinter.END, x + "\000\000\000\000" + self.checked_ips_dict.get(x).get("jp"))
            self.label_long.configure(text="远程文件路径： " + str(self.path_long.size()))

    def bn_path_europe(self):
        if self.bn_uk["fg"] == "red":
            self.bn_us["fg"] = "black"
            self.bn_uk["fg"] = "black"
            self.bn_jp["fg"] = "black"
            # 删除路径
            self.path_long.delete(0, tkinter.END)
            self.checked_ips_path_dict.clear()
            self.label_long.configure(text="远程文件路径： " + str(self.path_long.size()))
        else:
            # 删除路径
            self.path_long.delete(0, tkinter.END)
            self.checked_ips_path_dict.clear()
            self.bn_uk["fg"] = "red"
            self.bn_us["fg"] = "black"
            self.bn_jp["fg"] = "black"
            # 添加路径
            for x in self.checked_ips_dict.keys():
                self.checked_ips_path_dict.update({x: self.checked_ips_dict.get(x).get("uk")})
                self.path_long.insert(tkinter.END, x + "\000\000\000\000" + self.checked_ips_dict.get(x).get("uk"))
            self.label_long.configure(text="远程文件路径： " + str(self.path_long.size()))

    def menu_func(self):
        files = self.path_local.curselection()
        if not files:
            tkinter.messagebox.showinfo(title='卧槽', message="你TM先选中一个再删好吗!")
            return

        if len(files) > 1:
            for x in files[::-1]:
                self.path_local.delete(x)  # 删除选中数据
                self.label_local.configure(text="本地上传文件： " + str(self.path_local.size()))
        else:
            self.path_local.delete(self.path_local.curselection())  # 删除选中数据
            self.label_local.configure(text="本地上传文件： " + str(self.path_local.size()))

    def get_file_path(self):
        file_name_local = filedialog.askopenfilenames()
        if not file_name_local:
            return

        for file in file_name_local:
            if file not in self.path_local.get(0, tkinter.END):
                self.path_local.insert(tkinter.END, file)

                self.label_local.configure(text="本地上传文件： " + str(self.path_local.size()))

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

        fail_ips = []

        for ip in self.checked_ips_dict.keys():
            try:
                long_folder_path = self.checked_ips_path_dict.get(ip)
                put_file_obj = Xpc(ip, files, long_folder_path)
                put_file_obj.put_file()
            except Exception:
                import traceback
                erro_msg = traceback.format_exc()
                print(erro_msg)
                fail_ips.append(ip)

        message = "上传失败\n" + ' \n'.join(fail_ips) if fail_ips else "恭喜上传成功"
        tkinter.messagebox.showinfo(title='上传结果', message=message)

    def creat_gui(self):
        tk = tkinter.Tk()
        tk.title("上传文件器")

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
        self.bt1_all = tkinter.Button(frm_lb1, text="全选", command=self.bt1_checked_all, bg="white")
        self.bt1_all.grid(row=0, column=1, sticky=tkinter.E, padx=10)
        self.lb1.grid(row=0, column=0, sticky=tkinter.W)
        self.lb1_ip = tkinter.Listbox(frm1, selectmode=tkinter.EXTENDED, listvariable=self.ip, width=25, height=8,
                                      highlightbackground="green", bd=1)
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
        self.bt2_all = tkinter.Button(frm_lb2, text="全选", command=self.bt2_checked_all, bg="white")
        self.bt2_all.grid(row=0, column=1, padx=5)
        self.lb2.grid(row=0, column=0)
        # self.lb2 = tkinter.Label(frm2, text="选中要上传的服务器：")
        # self.lb2.pack(side=tkinter.TOP, anchor=tkinter.SW)
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
        # 地区按钮选择
        self.long_file_path = tkinter.StringVar()
        frm4 = tkinter.Frame(frm_top1)
        lb4 = tkinter.Label(frm4, text="选择上传服务器文件路径")
        lb4.grid(row=0, columnspan=2, padx=20, pady=0)
        self.bn_us = tkinter.Button(frm4, text="北美", command=self.bn_path_na, font=('黑体', 15, 'bold'), fg="black")
        self.bn_us.grid(row=1, column=0, padx=20, pady=10)

        self.bn_uk = tkinter.Button(frm4, text="欧洲", command=self.bn_path_europe, font=('黑体', 15, 'bold'), fg="black")
        self.bn_uk.grid(row=2, column=0, padx=20, pady=10)

        self.bn_jp = tkinter.Button(frm4, text="日本", command=self.bn_path_jp, font=('黑体', 15, 'bold'), fg="black")
        self.bn_jp.grid(row=1, column=1, padx=10, pady=10)
        frm4.pack(side=tkinter.RIGHT, anchor=tkinter.NE, padx=20, pady=10)

        # 本地文件选择
        frm5 = tkinter.Frame(tk)
        self.file = tkinter.StringVar()

        # 路径文件本地
        self.label_local = tkinter.Label(frm5, text="本地上传文件：")
        self.label_local.grid(column=0, row=0, sticky=tkinter.W, padx=10)
        self.path_local = tkinter.Listbox(frm5, selectmode=tkinter.EXTENDED,
                                          listvariable=self.file, width=30, height=8,
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

        def showMenu(event):
            menu.post(event.x_root, event.y_root)

        self.path_local.bind("<Button-3>", showMenu)
        self.get_file_local = tkinter.Button(frm5, text="添加本地文件", command=self.get_file_path, font=('黑体', 10, 'bold'),
                                             fg="black").grid(column=0, row=2, padx=10, pady=20)

        # 路径文件远程
        self.label_long = tkinter.Label(frm5, text="远程文件路径：")
        self.label_long.grid(column=2, row=0, sticky=tkinter.W, padx=10)
        self.path_long = tkinter.Listbox(frm5, selectmode=tkinter.EXTENDED, listvariable=self.long_file_path, width=50,
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
        tk.mainloop()


if __name__ == '__main__':
    run = Gui(ips_dict)
    run.creat_gui()
