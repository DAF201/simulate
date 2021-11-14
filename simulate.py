import threading
import base64
import os
import time
from tkinter.filedialog import askopenfilenames
from tkinter import Tk
import sys
import time
from typing import Any

counter = 1
MAX_THREDINGS = threading.Semaphore(8)


class simulator:
    def __init__(self, current_file: str) -> None:
        '''init'''

        self.__file_size: int
        self.__file_name: str
        self.__file_path: str
        self.__file_number: str
        self.__is_key: bool
        self.__start_time: time
        self.__ori_name: str
        self.__file_ext: str

        self.__start_time = time.time()
        global counter
        self.__file_number = str(counter)
        counter += 1
        self.__lock = threading.Lock()
        self.__file_name = current_file.split('/')[-1]
        self.__file_path = current_file
        with open(current_file, 'r')as file:
            file.seek(0, os.SEEK_END)
            self.__file_size = file.tell()

        if self.__file_name.split('.')[-1] == 'txt' and self.__file_name.count('.') == 2:
            self.__is_key = True
            self.__ori_name = self.__file_name.split('.')[0]
            self.__file_ext = self.__file_name.split('.')[1]
        else:
            self.__is_key = False
            self.__ori_name = None
            self.__file_ext = None

    def __encode(self) -> str:
        '''to get b64 data from file'''

        try:
            with open(self.__file_path, 'rb') as file:
                content = file.read()
            content = str(base64.b64encode(content), 'utf-8')
            # print(content)
            return content
        except Exception as e:
            self.__into_error(e, 'encode')

    def __decode(self, binary_data: tuple) -> bytes:
        '''to get the base64 info'''
        fin = ''
        for x in binary_data:
            fin += x
        binary_data = base64.b64decode(fin)
        return binary_data

    def __to_binary(self, b64_data: str) -> tuple:
        '''to get binary data of file'''

        try:
            temp = []
            for x in b64_data:
                temp.append(format(ord(x), 'b'))
            temp = tuple(temp)
            return temp
        except Exception as e:
            self.__into_error(e, 'to binary')

    def __from_binary(self, binary_data: tuple) -> tuple:
        '''to get the binary data from text'''

        try:
            binary_data = list(binary_data)
            for x in range(len(binary_data)):
                binary_data[x] = chr(int(binary_data[x], 2))
            binary_data = tuple(binary_data)
            return binary_data
        except Exception as e:
            self.__into_error(e, 'from binary')

    def __to_text(self, binary_data: tuple) -> str:
        '''convert the binary into a file'''

        try:
            spliter: str
            spliter = '‍'

            data: str
            data = ''

            temp = list(binary_data)
            for x in range(len(temp)):
                temp[x] = temp[x].replace('0', '‌')  # 8204
                temp[x] = temp[x].replace('1', '​')  # 8203
            data = spliter.join(temp)
            return data
        except Exception as e:
            self.__into_error(e, 'to text')

    def __from_text(self) -> tuple:
        '''to get the binary data from file'''

        try:
            data: str
            with open(self.__file_path, 'r')as file:
                data = file.read()
            data = data.split('‍')
            for x in range(len(data)):
                data[x] = data[x].replace('​', '1')
                data[x] = data[x].replace('‌', '0')
            data = tuple(data)
            return data
        except Exception as e:
            self.__into_error(e, 'from text')

    def __into_error(self, e: Exception, name: str) -> None:
        '''to close a thread when it runs into an error'''

        print('%s: run into an error while processing %s, error type: %s\n' %
              (self.__file_name, name, e.__class__.__name__))
        sys.exit()

    @property
    def file_info(self) -> dict:
        '''to get infomation of the file'''

        self.__lock.acquire()
        global counter
        print('file %s:' % self.__file_number)
        print('file name: %s' % self.__file_name)
        print('file path: %s' % self.__file_path)
        print('file size: %s bytes' % str(self.__file_size))
        print('')
        self.__lock.release()
        return {'number': self.__file_number, 'name': self.__file_name, 'path': self.__file_path, 'size': self.__file_size}

    def main(self) -> None:
        '''main function'''

        data: Any
        self.file_info

        if self.__is_key:
            data = self.__from_text()
            data = self.__from_binary(data)
            data = self.__decode(data)
            with open(self.__ori_name+'.'+self.__file_ext, 'wb')as file:
                file.write(data)
            print('file %s finished, time cost: %sseconds\n' %
                  (self.__file_number, (time.time()-self.__start_time)))
        else:
            data = self.__encode()
            data = self.__to_binary(data)
            data = self.__to_text(data)
            with(open(self.__file_name+'.txt', 'w'))as file:
                file.write(data)
            print('file %s finished, time cost: %sseconds\n' %
                  (self.__file_number, (time.time()-self.__start_time)))


def main():
    with MAX_THREDINGS:
        Tk().withdraw()
        files = askopenfilenames()
        for x in files:
            new_file = simulator(x)
            t = threading.Thread(target=new_file.main)
            t.start()
            t.join()


if __name__ == '__main__':
    main()
