class DialogWithUser:
    @staticmethod
    def get_msg_to_user(msg_to_user) -> str:
        command = input(msg_to_user)
        return command

    @staticmethod
    def send_msg_to_user(msg: str) -> None:
        print(msg)
