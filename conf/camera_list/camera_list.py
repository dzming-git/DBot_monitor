import yaml

class CameraList:
    _camera_list = {}
    _img_save_dir = ""

    @classmethod
    def _load_config(cls, config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            cls._camera_list = data['camera_list']
            cls._img_save_dir = data['path_conf']['img_save_dir']
    
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