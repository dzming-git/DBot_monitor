# DBot_monitor

DBot的监控模块服务程序，主程序为[DBot_main](https://github.com/dzming-git/DBot_main) 。

## 功能说明

该机器人目前支持以下功能：
- 指令调取海康威视摄像头实时图像并发送给用户
- 查询可用摄像头列表
- 权限控制

## 功能与权限要求

| 指令               | 举例             | 功能                                   | 权限要求 |
| ------------------ | ---------------- | -------------------------------------- | -------- |
| `#调取监控` <热键> | `#调取监控 客厅` | 调取指定位置的监控摄像头并发送最新图像 | `USER`   |
| `#监控列表`        | `#监控列表`      | 发送当前可用监控摄像头列表             | `USER`   |

## 安装运行

### 安装

1. 安装DBot微服务的主程序[DBot_main](https://github.com/dzming-git/DBot_main) 。

2. 下载代码到本地的`DBot_monitor`目录。

3. 将`conf/authority`文件夹中`authority_sample.yaml`重命名为 `authority.yaml` ，配置用户权限。未来将增加通过指令进行编辑的功能。

4. 将`conf/camera_list`文件夹中`camera_list_sample.yaml`重命名为 `camera_list.yaml`，配置摄像头列表。未来将增加通过指令进行编辑的功能。

5. 安装依赖库，运行以下命令：

   ``` python
   pip install -r requirements.txt
   ```

### 运行

1. 确保主程序 [DBot_main](https://github.com/dzming-git/DBot_main) 正常运行，相关步骤可查询主程序中的运行方法。

2. 运行监控服务程序 `app/monitor_server.py`：

   **注意 项目的工作目录必须是根目录**

   ``` python
   python  -m app.monitor_server run
   ```
   或者
   
   配置`run.bat`文件中运行该程序的python地址后，双击打开`run.bat`

## 配置文件

- `conf/camera_list/camera_list.yaml` - 配置文件，包括需要监控的摄像头列表及其相关信息。
- `con/authority/authority.yaml` - 配置文件，包括用户权限信息。
- `conf/route_info/route_info.yaml` - 配置文件，包括机器人主程序、消息代理、该服务程序的配置信息。

## 授权许可

本项目使用 MIT 许可证，有关更多信息，请参阅 LICENSE 文件。

## 联系我们

如果您对本项目有任何问题或建议，请随时通过以下方式联系我们：

- Email: dzm_work@163.com
- QQ: 715558579
