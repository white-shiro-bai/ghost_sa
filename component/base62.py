#!/usr/bin/env python
# encoding: utf-8
# author: toddlerya
# date: 2019/03/31

import string


class Base62(object):
    """
    基于0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ共计62个ascii字符
    构建62进制编码, 实现正整形十进制数据字符编码和解码
    作者源码在这里：https://gist.github.com/toddlerya/24ff96256ae4c8df2190a443d727d4ed
    """
    def __init__(self):
        # self.BASE_STR = string.ascii_letters + string.digits
        self.BASE_STR = string.digits + string.ascii_letters # 这里相对源码做了一个修改，把0-9排到字母前面了。如果字母在前，10进制转换62进制。会存在第52，第52+64*52的时候，返回000。62进制转换10进制的时候，会出现a=0,aa=0的情况。造成判断错误。如果是吧0-9放在前面。那么0只有在0的时候出现。此外再也不会出现了。这个具体可以看下面的测试用例。
        self.BASE = len(self.BASE_STR)

    def __10to62(self, digit, value=None):
        # 小心value参数的默认传参数陷阱
        # 不应写为value=[], 这将导致只有一次初始化, 每次调用列表的值都会累加
        # 应该声明为None, 只有为None才进行初始化, 这样能保持每次调用都会初始化此参数
        # https://pythonguidecn.readthedocs.io/zh/latest/writing/gotchas.html
        if value is None:
            value = list()
        rem = int(digit % self.BASE)
        value.append(self.BASE_STR[rem])
        div = int(digit / self.BASE)
        if div > 0:
            value = self.__10to62(div, value)
        return value

    def __62to10(self, str_value):
        value_list = list(str_value)
        value_list.reverse()
        temp_list = [self.BASE_STR.index(ele) * (62 ** n) for n, ele in enumerate(value_list)]
        return sum(temp_list)

    def encode_10to62(self, digit: int) -> str:
        """
        10进制转为62进制
        """
        value = self.__10to62(digit)
        value.reverse()
        value = ''.join(value)
        return value

    def decode_62to10(self, str62: str) -> int:
        """
        62进制转为10进制
        """
        return self.__62to10(str62)        



def main():
    code = Base62()
    print(code.encode_10to62(0))
    print(code.encode_10to62(1))
    print(code.encode_10to62(10))
    print(code.encode_10to62(52))
    print(code.encode_10to62(52+62*52))
    print(code.encode_10to62(53))
    print(code.encode_10to62(54))
    print(code.encode_10to62(60))
    print(code.encode_10to62(61))
    print(code.encode_10to62(62))
    print(code.encode_10to62(63))
    print(code.encode_10to62(122262))
    print('==' * 20)
    print(code.decode_62to10('0'))
    print(code.decode_62to10('00'))
    print(code.decode_62to10('a'))
    print(code.decode_62to10('aa'))
    print(code.decode_62to10('k'))
    print(code.decode_62to10('9'))
    print(code.decode_62to10('ab'))
    print(code.decode_62to10('ba'))
    print(code.decode_62to10('FX8'))

if __name__ == "__main__":
    main()