import struct
from twisted.python import log
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
import transaction
from skylines.model import DBSession, User, TrackingFix, Location
from skylines.tracking.crc import check_crc, set_crc

# More information about this protocol can be found in the XCSoar
# source code, source file src/Tracking/SkyLines/Protocol.hpp

MAGIC = 0x5df4b67b
TYPE_PING = 1
TYPE_ACK = 2
TYPE_FIX = 3

FLAG_ACK_BAD_KEY = 0x1

FLAG_LOCATION = 0x1
FLAG_TRACK = 0x2
FLAG_GROUND_SPEED = 0x4
FLAG_AIRSPEED = 0x8
FLAG_ALTITUDE = 0x10
FLAG_VARIO = 0x20
FLAG_ENL = 0x40

class TrackingServer(DatagramProtocol):
    def pingReceived(self, host, port, key, payload):
        if len(payload) != 8: return
        id, reserved, reserved2 = struct.unpack('!HHI', payload)

        flags = 0

        pilot = User.by_tracking_key(key)
        if not pilot:
            flags |= FLAG_ACK_BAD_KEY

        data = struct.pack('!IHHQHHI', MAGIC, 0, TYPE_ACK, 0,
                           id, 0, flags)
        data = set_crc(data)
        self.transport.write(data, (host, port))

    def fixReceived(self, host, key, payload):
        if len(payload) != 32: return
        data = struct.unpack('!IIIiiHHHhhH', payload)

        pilot = User.by_tracking_key(key)
        if not pilot:
            log.err("No such pilot: %d" % key)
            return

        flags = data[0]

        fix = TrackingFix()
        fix.ip = host
        fix.pilot = pilot

        if flags & FLAG_LOCATION:
            fix.location = Location(latitude=data[2] / 1000000.,
                                    longitude=data[3] / 1000000.)

        if flags & FLAG_TRACK:
            fix.track = data[5]

        if flags & FLAG_GROUND_SPEED:
            fix.ground_speed = data[6] / 16.

        if flags & FLAG_AIRSPEED:
            fix.airspeed = data[7] / 16.

        if flags & FLAG_ALTITUDE:
            fix.altitude = data[8]

        if flags & FLAG_VARIO:
            fix.vario = data[9] / 256.

        if flags & FLAG_ENL:
            fix.engine_noise_level = data[10]

        log.msg("%s %s %s" % (host, pilot, fix.location))

        DBSession.add(fix)
        DBSession.flush()
        transaction.commit()

    def datagramReceived(self, data, (host, port)):
        if len(data) < 16: return

        header = struct.unpack('!IHHQ', data[:16])
        if header[0] != MAGIC: return
        if not check_crc(data): return

        if header[2] == TYPE_FIX:
            self.fixReceived(host, header[3], data[16:])
        elif header[2] == TYPE_PING:
            self.pingReceived(host, port, header[3], data[16:])
