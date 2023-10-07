import re


class SimpleDes:
    def __init__(self):
        self.ip_box = [2, 6, 3, 1, 4, 8, 5, 7]
        self.p_box_4 = [2, 4, 3, 1]
        self.p_box_8 = [6, 3, 7, 4, 8, 5, 10, 9]
        self.p_box_10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
        self.e_p_box = [4, 1, 2, 3, 2, 3, 4, 1]
        self.s_box_1 = [[[0, 1], [0, 0], [1, 1], [1, 0]],
                        [[1, 1], [1, 0], [0, 1], [0, 0]],
                        [[0, 0], [1, 0], [0, 1], [1, 1]],
                        [[1, 1], [0, 1], [0, 0], [1, 0]]]
        self.s_box_2 = [[[0, 0], [0, 1], [1, 0], [1, 1]],
                        [[1, 0], [1, 1], [0, 1], [0, 0]],
                        [[1, 1], [0, 0], [0, 1], [1, 0]],
                        [[1, 0], [0, 1], [0, 0], [1, 1]]]

        self.message = [None] * 8
        self.cipher = [None] * 8
        self.key = [None] * 10

    def set_message(self, message):
        self.message = message

    def set_key(self, key):
        self.key = key

    def set_key_b(self, key):
        if re.match("^[01]+$", key):
            if len(key) != 10:
                return "密钥位数不为10位"
        else:
            return "密钥二进制格式错误"

        list_b = [int(char) for char in key]
        self.key = list_b
        return "密钥设置成功"

    def set_cipher(self, cipher):
        self.cipher = cipher

    @staticmethod
    def permute(message, key):
        m = [message[k - 1] for k in key]
        return m

    @staticmethod
    def inverse(key):
        k = [key.index(i+1)+1 for i in range(len(key))]
        return k

    @staticmethod
    def left_shift(message, key):
        k = key % len(message)
        m = message[k:] + message[:k]
        return m

    @staticmethod
    def s_4_2(message, key):
        h = message[0] * 2 + message[3]
        v = message[1] * 2 + message[2]
        return key[h][v]

    @staticmethod
    def xor(arr_1, arr_2):
        result = [a ^ b for a, b in zip(arr_1, arr_2)]
        return result

    def creat_sub_key(self):
        k = self.permute(self.key, self.p_box_10)
        left = k[:5]
        right = k[5:]

        left = self.left_shift(left, 1)
        right = self.left_shift(right, 1)
        k_1 = self.permute(left+right, self.p_box_8)

        left = self.left_shift(left, 1)
        right = self.left_shift(right, 1)
        k_2 = self.permute(left + right, self.p_box_8)

        return k_1, k_2

    def f(self, message, key):
        m = self.permute(message, self.e_p_box)
        s = self.xor(m, key)
        left = s[:4]
        right = s[4:]
        left = self.s_4_2(left, self.s_box_1)
        right = self.s_4_2(right, self.s_box_2)
        return self.permute(left+right, self.p_box_4)

    def swap(self, m, k_1, k_2):
        left_1 = m[:4]
        left_2 = m[4:]

        right_1 = self.f(left_2, k_1)
        right_3 = self.xor(left_1, right_1)

        right_2 = self.f(right_3, k_2)
        left_3 = self.xor(left_2, right_2)

        i_ip_box = self.inverse(self.ip_box)

        return left_3+right_3, i_ip_box

    def encrypt(self):
        m = self.permute(self.message, self.ip_box)
        k_1, k_2 = self.creat_sub_key()

        c, i_ip_box = self.swap(m, k_1, k_2)

        self.cipher = self.permute(c, i_ip_box)
        return self.cipher

    def decrypt(self):
        m = self.permute(self.cipher, self.ip_box)
        k_2, k_1 = self.creat_sub_key()

        c, i_ip_box = self.swap(m, k_1, k_2)

        self.message = self.permute(c, i_ip_box)
        return self.message

    def crack(self, message, cipher):
        self.message = message
        for i in range(2 ** 10):
            string_b = bin(i)[2:]
            list_b = [int(char) for char in string_b]
            self.key = [0]*(10-len(list_b)) + list_b
            self.encrypt()
            if cipher == self.cipher:
                print(self.key)

    def encrypt_a(self, message):
        cipher = str()
        for string in message:
            string_b = bin(ord(string))[2:]
            list_b = [int(char) for char in string_b]
            self.message = [0]*(8-len(list_b)) + list_b

            self.encrypt()

            int_b = int(''.join(map(str, self.cipher)), 2)
            char = chr(int_b)
            cipher += char
        return cipher

    def decrypt_a(self, cipher):
        message = str()
        for string in cipher:
            string_b = bin(ord(string))[2:]
            list_b = [int(char) for char in string_b]
            self.cipher = [0]*(8-len(list_b)) + list_b

            self.decrypt()

            int_b = int(''.join(map(str, self.message)), 2)
            char = chr(int_b)
            message += char
        return message

    def crack_a(self, message, cipher):
        keys = str()
        times = 0

        for i in range(2 ** 10):
            string_b = bin(i)[2:]
            list_b = [int(char) for char in string_b]
            self.key = [0]*(10-len(list_b)) + list_b
            if cipher == self.encrypt_a(message):
                string_k = ''.join(map(str, self.key))
                times += 1
                keys += string_k + ";"
        if times == 0:
            keys = "无密钥"
        return keys, times

    def encrypt_b(self, message):
        message = message[2:]
        if re.match("^[01]+$", message):
            if len(message) % 8 != 0:
                return "明文位数不为8的倍数"
        else:
            return "明文二进制格式错误"

        cipher = str()
        for i in range(0, len(message), 8):
            string_b = message[i:i + 8]
            list_b = [int(char) for char in string_b]
            self.message = list_b

            self.encrypt()

            char = ''.join(map(str, self.cipher))
            cipher += char
        return "0b" + cipher

    def decrypt_b(self, cipher):
        cipher = cipher[2:]
        if re.match("^[01]+$", cipher):
            if len(cipher) % 8 != 0:
                return "密文位数不为8的倍数"
        else:
            return "密文二进制格式错误"

        message = str()
        for i in range(0, len(cipher), 8):
            string_b = cipher[i:i + 8]
            list_b = [int(char) for char in string_b]
            self.cipher = list_b

            self.decrypt()

            char = ''.join(map(str, self.message))
            message += char
        return "0b" + message

    def crack_b(self, message, cipher):
        keys = str()
        times = 0

        message = message[2:]
        cipher = cipher[2:]
        if len(message) != len(cipher):
            return "明密文不对应"
        else:
            if re.match("^[01]+$", message):
                if len(cipher) % 8 != 0:
                    return "明密文位数不为8的倍数"
                elif not re.match("^[01]+$", cipher):
                    return "密文二进制格式错误"
            else:
                return "明文二进制格式错误"

        for i in range(2 ** 10):
            string_b = bin(i)[2:]
            list_b = [int(char) for char in string_b]
            self.key = [0]*(10-len(list_b)) + list_b
            if "0b" + cipher == self.encrypt_b("0b" + message):
                string_k = ''.join(map(str, self.key))
                times += 1
                keys += string_k + ";"
        if times == 0:
            keys = "无密钥"
        return keys, times
