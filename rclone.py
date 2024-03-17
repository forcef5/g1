import subprocess
# Sử dụng subprocess.Popen để chạy lệnh
import sys
import os
import subprocess
import re
import time
from datetime import datetime
sys.stdout.reconfigure(encoding='utf-8')

thoi_diem_hien_tai = datetime.now()
file_remote_storage = open('log.remote_storage.txt','w',encoding='utf-8')
file_remote_storage.close()
def run_rclone_lsf(remote_name):
    try:
        # Thực hiện lệnh rclone lsf và bắt kết quả bằng stdout=subprocess.PIPE
        process = subprocess.Popen(['rclone', 'lsf', f'{remote_name}:'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Đọc kết quả từ stdout
        output, error = process.communicate()
        
        # Kiểm tra nếu có lỗi
        if error:
            print("Error:", error.decode())
        else:
            # Hiển thị kết quả
            print("Output:", output.decode())
    except FileNotFoundError:
        print("rclone không được cài đặt hoặc không tìm thấy.")

# Gọi hàm chạy lệnh rclone lsf
def upload_to_google_drive(file_path,remote_name):
    try:
        # Thực hiện lệnh rclone copy và bắt kết quả bằng stdout=subprocess.PIPE
        process = subprocess.Popen(['rclone', 'copy', '-P', '--ignore-existing', file_path, f'{remote_name}:'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        

        # Đọc kết quả từ stdout
        output, error = process.communicate()
        
        # Kiểm tra nếu có lỗi
        if error:
            print("Error:", error.decode())
        else:
            # Hiển thị kết quả
            print("Upload Successful.")
            # print(output.decode())
    except FileNotFoundError:
        print("rclone không được cài đặt hoặc không tìm thấy.")

# Đường dẫn đến tệp bạn muốn tải lên Google Drive
file_path = "/root/logdrive.txt"

# Gọi hàm upload

def check_drive_storage(file_path,remote_name):
    try:
        # Thực hiện lệnh rclone about và bắt kết quả bằng stdout=subprocess.PIPE
        process = subprocess.Popen(['rclone', 'about', f'{remote_name}:'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Đọc kết quả từ stdout
        output, error = process.communicate()
        
        # Kiểm tra nếu có lỗi
        if error:
            print("Error:", error.decode())
            with open('logdrive_err.txt',mode='a+',encoding='utf-8') as file:
                file.write(f"{datetime.now()}\n{remote_name}\n{output.decode()}\n")
        else:
            # Hiển thị kết quả
            print('+---------+---------+---------+')
            print(datetime.now())
            print(f"{remote_name}\nDrive Storage Information:")
            print(output.decode())
            with open(file_path,mode='w',encoding='utf-8') as file:
                file.write(f"{datetime.now()}\n{remote_name}\nDrive Storage Information:\n{output.decode()}")
            with open('log.remote_storage.txt',mode='a+',encoding='utf-8') as file2:
                file2.write(f"+---------+---------+---------+\n{datetime.now()}\n{remote_name}\nDrive Storage Information:\n{output.decode()}\n")
                
            upload_to_google_drive(file_path,remote_name)
            print('+---------+---------+---------+')
    except FileNotFoundError:
        print("rclone không được cài đặt hoặc không tìm thấy.")


with open('rclone.conf','r',encoding='utf-') as file:
    lines = file.readlines()
file_remove_drive = open('log.remote.txt','w',encoding='utf-')
for line in lines:
    email = re.findall(r'\[(.*?)\]',line)
    if len(email) >0:
        
        if ('@' in email[0]):
            print (email[0])
            file_remove_drive.write(f'rclone copy -P  /root/downloaded/ {email[0]}:\n')
        
           
    else:
        pass
    # print(line)     
    # print('-'*80)
file_remove_drive.close()
print('------------------------------------')
print ("Thông tin chi tiết")
print('------------------------------------')

with open('/root/.config/rclone/rclone.conf','r',encoding='utf-') as file:
    lines = file.readlines()

for line in lines:
    email = re.findall(r'\[(.*?)\]',line)
    if len(email) >0:
        
        if ('@' in email[0]):
            print (email[0])
            check_drive_storage(file_path,email[0])
    else:
        pass
    # print(line)     
    # print('-'*80)

