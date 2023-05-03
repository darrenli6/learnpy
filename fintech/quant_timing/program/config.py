import os

current_file =  __file__


# 程序根目录地址，os.pardir：父目录
root_path = os.path.abspath(os.path.join(current_file,os.pardir,os.pardir))


input_data_path = os.path.abspath(os.path.join(root_path, 'data', 'input_data'))

output_data_path = os.path.abspath(os.path.join(root_path, 'data', 'output_data'))

