from models import Model
from models.mongua import Mongua


class User(Mongua):
    __fields__ = Mongua.__fields__ + [
        ('username', str, ''),
        ('password', str, ''),
        ('user_image', str, ''),
        ('role', int, -1)
    ]

    """
        User 是一个保存用户数据的 model
        现在只有两个属性 username 和 password
    """
    # def from_form(self, form):
    #     self.id = form.get('id', None)
    #     self.username = form.get('username', '')
    #     self.password = form.get('password', '')
    #     self.user_image = 'default.png'
    def __init__(self):
        self.user_image = 'default.png'
        self.role = 1

    def salted_password(self, password, salt='$!@><?>HUI&DWQa`'):
        import hashlib
        def sha256(ascii_str):
            return hashlib.sha256(ascii_str.encode('ascii')).hexdigest()

        hash1 = sha256(password)
        hash2 = sha256(hash1 + salt)
        return hash2

    def hashed_password(self, pwd):
        import hashlib
        # 用 ascii 编码转换成 bytes 对象
        p = pwd.encode('ascii')
        s = hashlib.sha256(p)
        # 返回摘要字符串
        return s.hexdigest()

    @classmethod
    def register(cls, form):
        name = form.get('username', '')
        pwd = form.get('password', '')
        if len(name) > 2 and User.find_by(username=name) is None:
            u = User().new(form)
            # u.from_form(form)
            u.password = u.salted_password(pwd)
            u.role = 11
            u.user_image = 'default.png'
            u.save()
            return u
        else:
            return None

    @classmethod
    def validate_login(cls, form):
        u = User()
        u.username = form.get("username", '')
        u.password = form.get("password", "")
        # u.from_form(form)
        user = User.find_by(username=u.username)
        if user is not None and user.password == u.salted_password(u.password):
            return user
        else:
            return None