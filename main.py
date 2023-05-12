import sys
import hashlib
import pymysql
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QDesktopWidget


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口大小和居中
        self.resize(400, 200)
        self.center()
        # 设置窗口标题
        self.setWindowTitle('用户登录')

        # 用户名输入框
        self.user_label = QLabel('用户名:', self)
        self.user_label.move(50, 50)
        self.user_edit = QLineEdit(self)
        self.user_edit.move(110, 50)
        # 密码输入框
        self.passwd_label = QLabel('密  码:', self)
        self.passwd_label.move(50, 80)
        self.passwd_edit = QLineEdit(self)
        self.passwd_edit.setEchoMode(QLineEdit.Password)
        self.passwd_edit.move(110, 80)
        # 登录按钮
        self.login_btn = QPushButton('登录', self)
        self.login_btn.move(110, 120)
        self.login_btn.clicked.connect(self.login)
        # 退出按钮
        self.exit_btn = QPushButton('退出', self)
        self.exit_btn.move(220, 120)
        self.exit_btn.clicked.connect(self.close)

        self.show()

    def center(self):
        #将窗口居中
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def login(self):
        #用户登录
        # 获取用户输入的用户名和密码
        user_id = self.user_edit.text()
        user_passwd = self.passwd_edit.text()
        # 对密码进行MD5加密
        md5 = hashlib.md5()
        md5.update(user_passwd.encode('utf-8'))
        user_passwd = md5.hexdigest()

        # 连接数据库
        conn = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='123456',
            database='testdb',
            charset='utf8'
        )
        cursor = conn.cursor()

        # 查询用户
        sql = "SELECT user_id, user_name, user_passwd, IsAdmin FROM tbuser WHERE user_id=%s"
        cursor.execute(sql, user_id)
        user = cursor.fetchone()

        if user is None:
            QMessageBox.warning(self, '登录失败', '用户名或密码错误！')
        else:
            if user[2] == user_passwd:
                QMessageBox.information(self, '登录成功', '欢迎您，' + user[1] + '！')
                if user[3] == 1:
                    QMessageBox.information(self, '管理员登录', '您是管理员，可以进行相关操作。')
                else:
                    QMessageBox.information(self, '普通用户登录', '您是普通用户，只能进行普通操作。')
            else:
                QMessageBox.warning(self, '登录失败', '用户名或密码错误！')

        # 关闭数据库连接
        cursor.close()
        conn.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    sys.exit(app.exec_())
