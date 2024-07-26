import gzip
import io
class SimpleCompressor:
    @staticmethod
    def compress(data):
        out = io.BytesIO()
        with gzip.GzipFile(fileobj=out, mode='wb', compresslevel=9) as f:
            f.write(data)
        return out.getvalue()

    @staticmethod
    def decompress(data):
        in_ = io.BytesIO(data)
        with gzip.GzipFile(fileobj=in_, mode='rb') as f:
            return f.read()
