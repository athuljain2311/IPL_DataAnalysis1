def error_message(error,error_detail):
    _,_,tb = error_detail.exc_info()
    file_name = tb.tb_frame.f_code.co_filename
    message = f"ERROR OCCURED IN PYTHON SCRIPT : [{file_name}], IN LINE NUMBER : [{tb.tb_lineno}], WITH ERROR MESSAGE : [{str(error)}]"
    return message

class CustomException(Exception):
    def __init__(self,error,error_detail):
        self.message = error_message(error,error_detail)

    def __str__(self):
        return self.message