<div align="center">
    <img src="pics/shortmark.jpg" alt="">
</div>
<div align="center">
    <h2>
        IPCC : Intelligent Perception and Cooperative Computing Platform on  Constellation Network
    </h2>
</div>
<div align="center">
    <a href="#">
        <span>项目主页</span>
    </a>
</div>
<br>


<div align="center">

[![GitHub stars](https://badgen.net/github/stars/shadowwalk370/IPCC)](https://github.com/shadowwalk370/IPCC) &nbsp; [![license](https://img.shields.io/badge/license-Apache--2.0-green)](LICENSE)

</div>

## 简介

本项目是基于多个 **[NVIDIA Jetson Orin NX](https://www.nvidia.cn/autonomous-machines/embedded-systems/jetson-orin/)** 边缘计算设备所搭建的🌏 **分布式遥感图像智能解译平台** 🌏。

其中各个🌟 **后端模型** 🌟基于 **[mmsegmentation](https://github.com/open-mmlab/mmsegmentation)、[mmpretrain](https://github.com/open-mmlab/mmpretrain)、[mmdetection](https://github.com/open-mmlab/mmdetection)** 等开源项目进行开发，并基于 **[mmdeploy](https://github.com/open-mmlab/mmdeploy)** 进行模型的部署和推理工作。

本项目的后端模型目前支持的版本为Python 3.8 、 PyTorch 1.11 、 mmcv 2.0.1 、 mmdet 3.3.0 、 mmsegmentation 1.2.2 、 mmpretrain 1.2.0 , 在NVIDIA Jetson Orin NX 上采用JetPack 5.1.1 ,其余具体环境配置请参考📜 **[IPCC终端环境配置指南](./env.md)、[补丁包更新说明](./patch_update.md)** 📜。

本项目所应用到的🚀 **后端模型及其处理脚本** 🚀可以直接从 **[这个云盘](https://bhpan.buaa.edu.cn/link/AA532216B6F54E4ABE9AED79200C90E84D)** 获取。

## 主要特性

✨ **多场景智能感知**

提供不同数据集场景下的 **多种后端模型** ，涵盖遥感场景分类、遥感地物分割、遥感目标检测等不同任务，并且 **支持fp16与int8量化** ，便于轻松部署和推理

✨ **分布式协同计算** （暂未更新）

提供大容量数据的分布式推理思路和脚本

✨ **多星通信组网** （暂未更新）

提供多张板卡之间的通信组网脚本

✨ **半实物仿真与可视化前端** （暂未更新）

实现半实物的仿真系统以及流量负载可视化前端

## 更新日志

🎉 **2024.2.1** 正式发布IPCC项目，更新了基本的模型推理脚本以及90余个不同的mmseg模型后端。

🎉 **2024.2.6** 更新了后端模型补丁更新脚本、后端检查脚本，修复了模型推理脚本多张图片存储不一致的问题，新增支持mmseg模型后端，总共包含162个不同的后端。

## 模型库


## 教程文档

<details>
<summary>环境配置</summary>

- [云服务器开发环境配置](./env.md#一云服务器开发环境配置)
- [NVIDIA Jetson 环境配置](./env.md#二jetson-orin-nx开发环境配置)

</details>

<details>
<summary>模型部署和推理</summary>

- [模型推理](./env.md#二jetson-orin-nx开发环境配置)
- [补丁更新](./patch_update.md)

</details>


## 致谢

本项目是基于 **[mmsegmentation](https://github.com/open-mmlab/mmsegmentation)、[mmpretrain](https://github.com/open-mmlab/mmpretrain)、[mmdetection](https://github.com/open-mmlab/mmdetection)** 等项目进行开发、基于 **[mmdeploy](https://github.com/open-mmlab/mmdeploy)** 进行落地部署的，诚挚感谢相关的开发者们！

## 开源许可证

该项目采用 **[Apache 2.0 开源许可证](LICENSE)**。

## 欢迎联系和交流

如果您有任何想交流的问题或者建议，可以通过以下邮箱联系我们😁。
```
shadowwalk370@hotmail.com
```
