from app.message_handler.message_handler import send_current_camera_image, send_camera_list

func_dict = {
    '#调取监控': lambda gid=None, qid=None, msg_list=[]: send_current_camera_image(gid, qid, msg_list),
    '#监控列表': lambda gid=None, qid=None, msg_list=[]: send_camera_list(gid, qid, msg_list)
}