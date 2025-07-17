一、把telegram的rss订阅链接引用的telegrah在阅读器里面能够拉取全文:

二、实现效果如下：

转换前：
<img width="1059" height="665" alt="image" src="https://github.com/user-attachments/assets/88a3f2fe-f641-49c5-bbe8-c957672f9c69" />

转换后：
<img width="1124" height="680" alt="image" src="https://github.com/user-attachments/assets/7ebd84aa-fd3f-45b2-82c1-6934c359aa4c" />
三、部署：

docker build -t telegrah2rss .

docker run -d --name telegrah2rss -p 5000:5000 telegrah2rss
