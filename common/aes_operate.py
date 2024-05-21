import base64
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


class AESCipher:
    def __init__(self, key):
        # 确保密钥长度为32字节（256位）
        if len(key) != 32:
            raise ValueError("Key must be 32 bytes long")
        self.key = key

    def encrypt(self, plaintext):
        # 初始化填充器
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext.encode('utf-8')) + padder.finalize()

        # 初始化加密器
        iv = os.urandom(16)  # 生成随机的初始化向量
        c = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        encryptor = c.encryptor()

        # 加密数据
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        # 返回初始化向量和密文（通常一起传输）
        return base64.urlsafe_b64encode(iv + ciphertext).decode('utf-8')

    def decrypt(self, ciphertext):
        # 解码密文并分离初始化向量和密文
        ciphertext = base64.urlsafe_b64decode(ciphertext)
        iv = ciphertext[:16]
        ciphertext = ciphertext[16:]

        # 初始化解密器
        c = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=default_backend())
        decryptor = c.decryptor()

        # 解密数据
        decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()

        # 去除填充
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(decrypted_padded) + unpadder.finalize()

        return plaintext.decode('utf-8')


key = base64.b64decode("JWMB276HW+u9GnMiyG4HZtlpIV2spHW1OOcORwfSRXo=")
cipher = AESCipher(key)

