# DBot_monitor

DBot的监控模块服务程序。

## 功能说明

该机器人目前支持以下功能：
- 指令调取海康威视摄像头实时图像并发送给用户
- 查询可用摄像头列表
- 添加监控摄像头
- 权限控制

## 功能

#监控 指令 参数1 参数2 参数3 ......

---

### 调取

#### 功能说明

调取指定位置的监控摄像头并发送最新图像

#### 参数说明

参数为 `conf/camera_list/camera_list.yaml` 中设置的热键（`hotkeys`），支持同时输入多个热键。

例如：`#监控 调取 客厅 餐厅 192.168.1.16`

---

### 列表

#### 功能说明

发送当前可用监控摄像头列表

#### 参数说明

无参数。

---

### 添加

#### 功能说明

添加监控信息到配置文件

#### 参数说明

参数为 IP地址 用户名 密码。

例如：`#监控 添加 192.168.1.16 user pwd`

---

## 安装运行

### 安装

1. 安装DBot微服务的平台程序 [DBot_platform](https://github.com/dzming-git/DBot_platform) 。

1. 安装DBot微服务的SDK [DBot_SDK](https://github.com/dzming-git/DBot_SDK)

2. 下载代码到本地的`DBot_monitor`目录。

3. 将`conf/authority`文件夹中`authority_sample.yaml`重命名为 `authority.yaml` ，配置用户权限。

4. 将`conf/camera_list`文件夹中`camera_list_sample.yaml`重命名为 `camera_list.yaml`，配置摄像头列表。

5. 安装依赖库，运行以下命令：

   ``` python
   pip install -r requirements.txt
   ```

### 运行

1. 确保平台程序 [DBot_platform](https://github.com/dzming-git/DBot_platform)  正常运行，相关步骤可查询平台程序中的运行方法。

2. 运行监控服务程序 `app/server.py`：

   **注意 项目的工作目录必须是根目录**

   ``` python
   python -m app.server
   ```
   或者
   
   配置`run.bat`文件中运行该程序的python地址后，双击打开`run.bat`

## 配置文件

- `conf/camera_list/camera_list.yaml` - 配置文件，包括需要监控的摄像头列表及其相关信息。
- `con/authority/authority.yaml` - 配置文件，包括用户权限信息。
- `conf/route_info/route_info.yaml` - 配置文件，包括机器人API网关、消息代理、该服务程序的配置信息。

## 授权许可

本项目使用 MIT 许可证，有关更多信息，请参阅 LICENSE 文件。

## 联系我们

如果您对本项目有任何问题或建议，请随时通过以下方式联系我们：

- Email: dzm_work@163.com
- QQ: 715558579
