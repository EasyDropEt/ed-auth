from abc import ABCMeta, abstractmethod

from ed_auth.application.features.auth.dtos.delete_user_dto import \
    DeleteUserDto


class ABCAuthRabbitMQSubscriber(metaclass=ABCMeta):
    @abstractmethod
    def delete_user(self, delete_user_dto: DeleteUserDto) -> None: ...
