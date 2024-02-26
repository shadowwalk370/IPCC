## 通信组网配置

#### 一、客户端

若要运行客户端代码，请按照如下修改**father_temp.py**中的部分代码：

- 在`inference_source()`中修改**src、dst**参数，用于加载传输源文件夹地址和接受数据的存放地址。
- 在`inference_source()`中设置子节点的**ip_list、port_list、name_list**。其中ip_list在Linux平台上可在终端中通过`ifconfig`获取，在windows平台上可在终端中通过`ipconfig`获取；端口号可以自行设定；子节点昵称名仅用于监视，同样可以自行确定。
- 在`inference_source()`中设置需要执行的通信组网命令，若采用默认的`scatter-gather`模式，只需在`inference_source()`中添加如下命令即可：


````py
father.father_sending_order("scatter")
father.father_sending_order("inference")
father.father_sending_order("gather")
father.father_sending_order("quit")
````
- 若想要持续一段时间监视某一文件夹下是否出现新的待处理文件夹，可以采用`supervised_inference`函数,需要设置**supervised**参数用于指定要持续监视的文件夹,以及指定**inference_record**用于已经推理过的文件夹的记录。需要注意的是，仅有当文件夹中出现`config.txt`文件时，才会自启动对该文件夹的推理~

#### 二、服务端

服务端的配置相对来说较为简单，仅需在**son_temp.py**中设置好每个子节点的**ip**地址、**port**端口号、**src**客户端从服务端取出文件时的位置、**dst**客户端传来的文件存放的位置、**name**子节点昵称，设置好这些后直接运行脚本即可持续等待连接和命令~