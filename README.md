## 简介
通过 selenium 实现的一个 v2ex 网站自动签到领金币的程序。

## 注意
- 打包镜像前，先填写 config.json

## 打包镜像
```
docker build -t v2ex-signin .
```

## 运行容器
```
docker run --rm -it v2ex-signin
```

## 调试容器（如果需要）
```
docker run --rm -it --entrypoint /bin/bash v2ex-signin
```

## 定时执行
```
crontab -e
```

在 crontab 文件中添加一行来设置定时任务。例如，每天凌晨 1 点执行：
```
0 1 * * * docker run --rm v2ex-signin
```