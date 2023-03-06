import ruamel.yaml
from utils.watch_config import WatchDogThread

class CameraList:
    _config_path = ''
    _watch_dog = None
    _camera_list = {}
    _img_save_dir = ""

    @classmethod
    def load_config(cls, config_path, reload_flag=False):
        with open(config_path, 'r', encoding='utf-8') as f:
            data = ruamel.yaml.load(f, Loader=ruamel.yaml.RoundTripLoader)
            cls._camera_list = data['camera_list']
            cls._img_save_dir = data['path_conf']['img_save_dir']
            if not reload_flag:
                cls._config_path = config_path
                cls._watch_dog = WatchDogThread(config_path, cls.reload_config)
                cls._watch_dog.start()
    
    @classmethod
    def reload_config(cls):
        cls.load_config(config_path=cls._config_path, reload_flag=True)
    
    @classmethod
    def save_config(cls):
        data = ruamel.yaml.comments.CommentedMap()
        data['path_conf'] = ruamel.yaml.comments.CommentedMap({'img_save_dir': cls._img_save_dir})
        data['camera_list'] = cls._camera_list
        with open(cls._config_path, 'w', encoding='utf-8') as f:
            ruamel.yaml.dump(data, f, allow_unicode=True, Dumper=ruamel.yaml.RoundTripDumper)

    @classmethod
    def add_camera(cls, ip_address, username, password):
        cls._camera_list.append({
            'ip': ip_address,
            'username': username,
            'password': password,
            'location': '',
            'hotkeys': [ip_address]
        })
        cls.save_config()

    @classmethod
    def get_camera_ip_list(cls):
        return [camera["ip"] for camera in cls._camera_list]

    @classmethod
    def get_camera_by_hotkey(cls, hotkey):
        for camera in cls._camera_list:
            if hotkey in camera.get('hotkeys', []):
                return (camera['ip'], camera['username'], camera['password'])
        return None, None, None

    @classmethod
    def get_location_by_hotkey(cls, hotkey):
        for camera in cls._camera_list:
            if hotkey in camera.get('hotkeys', []):
                return camera['location']
        return None

    @classmethod
    def get_img_save_dir(cls):
        return cls._img_save_dir
