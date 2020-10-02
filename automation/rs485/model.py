# region import libraries

from .resultValue import ResultValue
from ..command import Command
from ..supportClass import BColors
from ..application.database import db
from ..modules import Module

from datetime import datetime
from threading import Thread
from serial import Serial
from struct import unpack
from time import sleep
import json

# endregion


class RS485(db.Model):

    """Base class to work on rs485 line.
    """

    # db columns init
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    port = db.Column(db.String(50), nullable=False, default="COM1")
    address = db.Column(db.Integer, nullable=False, default=1)
    module_id = db.Column(db.Integer, db.ForeignKey("module.id"), nullable=False, default=1)

    def __init__(
        self,
        name=None,
        port=None,
        address=None,
        module_id=None,
        *args,
        **kwargs
    ):
        self.name = name or self.name
        self.port = port or self.port
        self.module_id = module_id or self.module_id
        self.address = address or self.address

    def __str__(self, *args, **kwargs):
        return json.dumps({
            "name": self.name,
            "port": self.port,
            "address": self.address,
            "module": self.module.name
            if self.module.name
            else "",
        })

    def __repr__(self, *args, **kwargs):
        return 'RS485 instance. Name: "{}", Module: "{}", Port: "{}", Sending data: {}\n'.format(
            self.name, self.module.name if self.module else "", self.port, self.sending_data
        )

    def open_port(self, result=None, *args, **kwargs):
        self.result = result or ResultValue()
        # init variables
        exchange = 10
        interrupt_data = None

        # try to open com port
        try:
            self.port_modbus = Serial(port=self.port, baudrate=115200, timeout=0.1)
            print("{}[{}] Port {} open{}".format(BColors.OKGREEN, datetime.now(), self.port, BColors.ENDC))
        except BaseException:
            print("{}[{}] Cannot open port {}{}".format(BColors.FAIL, datetime.now(), self.port, BColors.ENDC))
            self.port_modbus = None

        # start daemon thread to write and read data from modbus
        port_write_data_thread = Thread(target=self._start_endless_cycle_send_read_data)
        port_write_data_thread.daemon = True
        port_write_data_thread.start()

    def _get_calculated_crc_data(self, data, *args, **kwargs):
        """function to calculate hash sum from inputed data.

        Args:
            data (list): List of data, which needet to calculate.

        Returns:
            list: List of data with calculated crc in the end.
        """

        output = [data[x] if x < len(data) else 0 for x in range(len(data) + 2)]
        crc = 0xFFFF

        for pos in bytearray(data):
            crc ^= pos
            for i in range(8):
                if (crc & 0x0001) != 0:
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1

        output[-2] = crc & 0xFF
        output[-1] = crc >> 8

        return output

    def _start_endless_cycle_send_read_data(self, *args, **kwargs):
        """start endless cycle. Sending data to com port,
        then receive data from the same port.
        """

        if not self.port_modbus:
            return

        while self.port_modbus.isOpen():
            # check if have data to send
            if len(self.sending_data) > 0:
                for sended_data in self.sending_data:
                    # send data to port
                    sended_data = self._write_data_to_port(sended_data)

                    # receive data
                    received_data = self._receive_data_from_port()

                    # get data from received data
                    self._get_value_from_received_data(received_data, sended_data)
            # or just wait
            else:
                sleep(0.1)

    def _write_data_to_port(self, sending_data, *args, **kwargs):
        """function to send data from serial port.

        Args:
            sending_data (list): List of data to send from modbus.
        """

        # check if have interrupt
        sending_data = self.interrupt_data or sending_data
        self.interrupt_data = None
        sending_data[0] = self.address

        # send data
        try:
            self.port_modbus.write(self._get_calculated_crc_data(sending_data))
            if self.exchange < 10:
                self.exchange += 1
        except BaseException:
            pass

        sleep(0.1)
        return sending_data

    def _receive_data_from_port(self, *args, **kwargs):
        """function to receive data from com port.

        Returns:
            list: List of received data
        """

        receive = []

        try:
            receive = self.port_modbus.read_all()
        except BaseException:
            return None
        if len(receive) < 3:
            return None

        receive_crc = self._get_calculated_crc_data(
            [self._get_encoded_data(data) for data in receive[:-2]]
        )
        if (
            self._get_encoded_data(receive[-2]) != receive_crc[-2]
            or self._get_encoded_data(receive[-1]) != receive_crc[-1]
        ):
            return None

        self.exchange = 0
        return receive

    def _get_encoded_data(self, decoded_data, *args, **kwargs):
        """get decoded data, return encodet data

        Args:
            decoded_data (byte): Encoded data.

        Returns:
            int: Decoded data.
        """

        return int(decoded_data.encode('hex', 16))

    def _get_value_from_received_data(self, received_data, sended_data, *args, **kwargs):
        """Function get received data and sended data.
        from data gets resulted value.

        Args:
            received_data (list): List of received data.
            sended_data (list): List of sended data
        """

        if not received_data or not sended_data:
            return

        if received_data[1] == "\x02":
            self._get_indication_value(received_data, sended_data)
        elif received_data[1] == "\x04":
            self._get_result_value(received_data, sended_data)

    def _get_indication_value(self, received_data, sended_data, *args, **kwargs):
        """get indication value from received data

        Args:
            received_data (list): List of received data.
            sended_data (list): List of sended data.
        """

        full_result = 0

        # get index of value from received data
        for received_index in range(self._get_encoded_data(received_data[2])):
            full_result |= self._get_encoded_data(received_data[3 + received_index]) << (received_index * 8)

        # set indication value
        low_byte = sended_data[2]
        high_byte = sended_data[3]
        for value in range(self._get_encoded_data(received_data[2]) * 8):
            key = unpack(">H", bytearray([low_byte, high_byte]))[0] + value
            self.module_result.indication[key] = 1 if (full_result & (1 << value)) > 0 else 0

    def _get_result_value(self, received_data, sended_data, *args, **kwargs):
        """get result value from received data

        Args:
            received_data (list): List of received data.
            sended_data (list): List of sended data.
        """

        # get started position of received result
        low_byte = sended_data[2]
        high_byte = sended_data[3]
        start_postion = unpack(">H", bytearray([low_byte, high_byte]))[0]

        # set result
        for count in range(self._get_encoded_data(received_data[2]) // 4):
            key = start_postion + count * 2
            position = count * 4
            result = unpack("f",
                            bytearray([received_data[4 + position],
                                       received_data[3 + position],
                                       received_data[6 + position],
                                       received_data[5 + position]]),
                            )[0]
            self.module_result.result[key] = result

    # region property methods

    @property
    def sending_data(self, *args, **kwargs):
        return json.loads(self.module.sending_data) if self.module else ""

    @property
    def module(self, *args, **kwargs):
        return Module.query.get(self.module_id)

    # endregion
