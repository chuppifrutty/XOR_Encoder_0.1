class SimpleEncryptor:
    @staticmethod
    def xor_encrypt_decrypt(data, key):
        return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

    @staticmethod
    def encrypt(data, key):
        return SimpleEncryptor.xor_encrypt_decrypt(data, key)

    @staticmethod
    def decrypt(data, key):
        return SimpleEncryptor.xor_encrypt_decrypt(data, key)
