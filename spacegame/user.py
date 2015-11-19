import os.path
import uuid

from pantsmud.driver import storage, util
from pantsmud.world import mobile


USER_FILE_PATH = "data/users/%s.user.json"
PLAYER_FILE_PATH = "data/players/%s.mobile.json"


class User(object):
    def __init__(self, user_uuid=None):
        if user_uuid:
            self.uuid = user_uuid
        else:
            self.uuid = uuid.uuid4()
        self.player_uuid = None

    def load_data(self, data):
        self.uuid = uuid.UUID(data["uuid"])
        self.player_uuid = uuid.UUID(data["player_uuid"]) if data["player_uuid"] else None

    def save_data(self):
        return {
            "uuid": str(self.uuid),
            "player_uuid": str(self.player_uuid) if self.player_uuid else ''
        }


def user_exists(user_uuid):
    return os.path.exists(USER_FILE_PATH % util.uuid_to_base32(user_uuid))


def load_user(user_uuid):
    return storage.load_file(USER_FILE_PATH % util.uuid_to_base32(user_uuid), User)


def save_user(user):
    storage.save_object(USER_FILE_PATH % util.uuid_to_base32(user.uuid), user)


def player_exists(player_uuid):
    return os.path.exists(PLAYER_FILE_PATH % util.uuid_to_base32(player_uuid))


def load_player(player_uuid):
    return storage.load_file(PLAYER_FILE_PATH % util.uuid_to_base32(player_uuid), mobile.Mobile)


def save_player(mob):
    storage.save_object(PLAYER_FILE_PATH % util.uuid_to_base32(mob.uuid), mob)
