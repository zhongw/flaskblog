A flask based blog.

## 启动应用的步骤
1. 创建一个virtualenv，然后active
2. 安装依赖 pip install -r requirement.txt
3. 运行 python manager.py runserver -r -d 启动应用
   -r 参数表示有python文件被修改，程序会自动重新加载该文件
   -d 参数表示使用debug模式
   -h 指定Host
   -p 指定端口，默认端口为5000