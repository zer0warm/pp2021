from domains.validator import *

class CommandList:
    def __init__(self, cmd_list=None):
        self.__cmd_list = []
        if cmd_list and isinstance(cmd_list, list):
            for cmd_desc, cmd_callback in cmd_list:
                self.add(cmd_desc, cmd_callback)

    def add(self, cmd_desc, cmd_callback):
        cmd_validator = Validator(cmd_desc, '[A-Za-z][A-Za-z\'" ]+')
        if cmd_validator.is_ok() and callable(cmd_callback):
            self.__cmd_list.append({'desc': cmd_desc, 'callback': cmd_callback})
        else:
            raise Exception("Can't add command to list.")

    def list_commands(self):
        for i in range(len(self.__cmd_list)):
            desc = self.__cmd_list[i]['desc']
            print(f'[{i+1}] {desc}')

    def get_command(self, cmd_num):
        return self.__cmd_list[cmd_num]

    def get_length(self):
        return len(self.__cmd_list)

class CommandPrompt:
    state = -1

    def __init__(self, msg, cmd_list=None, pat=None):
        self.__prompt_msg = msg
        self.__cmd_list = cmd_list
        self.__accept_command_pattern = pat
        self.__PS = ['>>>', '->', '--->']
        CommandPrompt.state += 1

    def _list_commands(self):
        self.__cmd_list.list_commands()

    def _execute(self, cmd_num):
        return self.__cmd_list.get_command(cmd_num-1)['callback']()

    def _get_prompt_string(self):
        return self.__PS[CommandPrompt.state]

    def main_loop(self):
        while True:
            self._list_commands()
            cmd = Validator(
                    input(f'{self._get_prompt_string()} {self.__prompt_msg} '),
                    accept_pattern=self.__accept_command_pattern)
            if cmd.is_ok():
                status = self._execute(cmd.value(int))
                if status == -10:
                    CommandPrompt.state -= 1
                    break
                elif status == False:
                    print('Error: Invalid response. Try again.')
            else:
                print('Error: Invalid command. Try again.')
