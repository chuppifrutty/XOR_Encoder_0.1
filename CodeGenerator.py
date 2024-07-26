import random
import string
class CodeGenerator:
    @staticmethod
    def generate_code(length=8):
        symbols = string.ascii_letters + string.digits
        return ''.join(random.choice(symbols) for i in range(length))
