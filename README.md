# S-DES
网安小组实验

从main.py启动界面，选择解密、加密、破解、碰撞4个功能。在明文或密文中，输入以"0b"为前缀的二进制数（二进制限制8位的倍数），或ASCLL字符（任意长度）。在密钥中输入10位二进制数。

main.py调用Window类，负责初始化界面。 
s_des.py中，在SimpleDes类中实现了Simple-DES算法，分别对外提供二进制数组，二进制字符，ASCLL字符的加解密及破解。 
window.py中，Entry类调用SimpleDes类，并为界面提供3个Entry控件，方便界面操作；Window类通过Notebook和Frame创建不同功能的分页，并调用Entry类，用按钮绑定事件。
