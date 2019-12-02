import itertools
import sys
from struct import unpack

try:
    import cStringIO
    BytesIO = cStringIO.StringIO
except ImportError:
    from io import BytesIO  # noqa

PY2 = sys.version_info[0] == 2


class KaitaiStruct(object):
    def __init__(self, stream):
        self._io = stream

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    @classmethod
    def from_file(cls, filename):
        f = open(filename, 'rb')
        try:
            return cls(KaitaiStream(f))
        except Exception:
            # close file descriptor, then reraise the exception
            f.close()
            raise

    def close(self):
        self._io.close()


class KaitaiStream(object):
    def __init__(self, io):
        self._io = io
        self.align_to_byte()

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    def close(self):
        self._io.close()

    # ========================================================================
    # Stream positioning
    # ========================================================================

    def is_eof(self):
        io = self._io
        t = io.read(1)
        if t == b'':
            return True
        else:
            io.seek(io.tell() - 1)
            return False

    def seek(self, n):
        self._io.seek(n)

    def pos(self):
        return self._io.tell()

    def size(self):
        # Python has no internal File object API function to get
        # current file / StringIO size, thus we use the following
        # trick.
        io = self._io

        # Remember our current position
        cur_pos = io.tell()

        # Seek to the end of the File object
        io.seek(0, 2)

        # Remember position, which is equal to the full length
        full_size = io.tell()

        # Seek back to the current position
        io.seek(cur_pos)

        return full_size

    # ========================================================================
    # Integer numbers
    # ========================================================================

    # ------------------------------------------------------------------------
    # Signed
    # ------------------------------------------------------------------------

    def read_s1(self):
        return unpack('b', self.read_bytes(1))[0]

    # ........................................................................
    # Big-endian
    # ........................................................................

    def read_s2be(self):
        return unpack('>h', self.read_bytes(2))[0]

    def read_s4be(self):
        return unpack('>i', self.read_bytes(4))[0]

    def read_s8be(self):
        return unpack('>q', self.read_bytes(8))[0]

    # ........................................................................
    # Little-endian
    # ........................................................................

    def read_s2le(self):
        return unpack('<h', self.read_bytes(2))[0]

    def read_s4le(self):
        return unpack('<i', self.read_bytes(4))[0]

    def read_s8le(self):
        return unpack('<q', self.read_bytes(8))[0]

    # ------------------------------------------------------------------------
    # Unsigned
    # ------------------------------------------------------------------------

    def read_u1(self):
        return unpack('B', self.read_bytes(1))[0]

    # ........................................................................
    # Big-endian
    # ........................................................................

    def read_u2be(self):
        return unpack('>H', self.read_bytes(2))[0]

    def read_u4be(self):
        return unpack('>I', self.read_bytes(4))[0]

    def read_u8be(self):
        return unpack('>Q', self.read_bytes(8))[0]

    # ........................................................................
    # Little-endian
    # ........................................................................

    def read_u2le(self):
        return unpack('<H', self.read_bytes(2))[0]

    def read_u4le(self):
        return unpack('<I', self.read_bytes(4))[0]

    def read_u8le(self):
        return unpack('<Q', self.read_bytes(8))[0]

    # ========================================================================
    # Floating point numbers
    # ========================================================================

    # ........................................................................
    # Big-endian
    # ........................................................................

    def read_f4be(self):
        return unpack('>f', self.read_bytes(4))[0]

    def read_f8be(self):
        return unpack('>d', self.read_bytes(8))[0]

    # ........................................................................
    # Little-endian
    # ........................................................................

    def read_f4le(self):
        return unpack('<f', self.read_bytes(4))[0]

    def read_f8le(self):
        return unpack('<d', self.read_bytes(8))[0]

    # ========================================================================
    # Unaligned bit values
    # ========================================================================

    def align_to_byte(self):
        self.bits = 0
        self.bits_left = 0

    def read_bits_int(self, n):
        bits_needed = n - self.bits_left
        if bits_needed > 0:
            # 1 bit  => 1 byte
            # 8 bits => 1 byte
            # 9 bits => 2 bytes
            bytes_needed = ((bits_needed - 1) // 8) + 1
            buf = self.read_bytes(bytes_needed)
            for byte in buf:
                # Python 2 will get "byte" as one-character str, thus
                # we need to convert it to integer manually; Python 3
                # is fine as is.
                if isinstance(byte, str):
                    byte = ord(byte)
                self.bits <<= 8
                self.bits |= byte
                self.bits_left += 8

        # raw mask with required number of 1s, starting from lowest bit
        mask = (1 << n) - 1
        # shift mask to align with highest bits available in self.bits
        shift_bits = self.bits_left - n
        mask <<= shift_bits
        # derive reading result
        res = (self.bits & mask) >> shift_bits
        # clear top bits that we've just read => AND with 1s
        self.bits_left -= n
        mask = (1 << self.bits_left) - 1
        self.bits &= mask

        return res

    # ========================================================================
    # Byte arrays
    # ========================================================================

    def read_bytes(self, n):
        r = self._io.read(n)
        if len(r) < n:
            raise EOFError(
                "requested %d bytes, but got only %d bytes" % (n, len(r))
            )
        return r

    def read_bytes_full(self):
        return self._io.read()

    def ensure_fixed_contents(self, expected):
        actual = self._io.read(len(expected))
        if actual != expected:
            raise Exception(
                "Unexpected fixed contents: got %s, was waiting for %s" %
                (str(actual), str(expected))
            )
        return actual

    # ========================================================================
    # Strings
    # ========================================================================

    def read_str_eos(self, encoding):
        return self._io.read().decode(encoding)

    def read_str_byte_limit(self, size, encoding):
        return self.read_bytes(size).decode(encoding)

    def read_strz(self, encoding, term, include_term, consume_term, eos_error):
        r = b''
        while True:
            c = self._io.read(1)
            if c == b'':
                if eos_error:
                    raise Exception(
                        "End of stream reached, but no terminator %d found" %
                        (term,)
                    )
                else:
                    return r.decode(encoding)
            elif ord(c) == term:
                if include_term:
                    r += c
                if not consume_term:
                    self._io.seek(self._io.tell() - 1)
                return r.decode(encoding)
            else:
                r += c

    # ========================================================================
    # Byte array processing
    # ========================================================================

    @staticmethod
    def process_xor_one(data, key):
        if PY2:
            r = bytearray(data)
            for i in range(len(r)):
                r[i] ^= key
            return bytes(r)
        else:
            return bytes(v ^ key for v in data)

    @staticmethod
    def process_xor_many(data, key):
        if PY2:
            r = bytearray(data)
            k = bytearray(key)
            ki = 0
            kl = len(k)
            for i in range(len(r)):
                r[i] ^= k[ki]
                ki += 1
                if ki >= kl:
                    ki = 0
            return bytes(r)
        else:
            return bytes(a ^ b for a, b in zip(data, itertools.cycle(key)))

    @staticmethod
    def process_rotate_left(data, amount, group_size):
        if group_size != 1:
            raise Exception(
                "unable to rotate group of %d bytes yet" %
                (group_size,)
            )

        mask = group_size * 8 - 1
        anti_amount = -amount & mask

        r = bytearray(data)
        for i in range(len(r)):
            r[i] = (r[i] << amount) & 0xff | (r[i] >> anti_amount)
        return bytes(r)
