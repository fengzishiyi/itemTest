import os

class Paths:
    base = os.path.dirname(__file__) # 返回父目录
    icons = os.path.join(base,'icons')

    @classmethod
    def icon(cls,filename):
        return os.path.join(cls.icons,filename) # 类属性 cls.a