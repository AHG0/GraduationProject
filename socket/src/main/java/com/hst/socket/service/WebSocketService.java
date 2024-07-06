package com.hst.socket.service;

import com.alibaba.fastjson.JSON;
import jakarta.websocket.OnOpen;
import jakarta.websocket.Session;
import lombok.extern.slf4j.Slf4j;
import com.alibaba.fastjson.JSONObject;
import org.springframework.stereotype.Component;
import org.springframework.util.StringUtils;

import jakarta.websocket.*;
import jakarta.websocket.server.PathParam;
import jakarta.websocket.server.ServerEndpoint;

import java.io.IOException;
import java.util.concurrent.ConcurrentHashMap;


@Component
@ServerEndpoint("/socket/{uid}")
@Slf4j
public class WebSocketService {
    // 用来记录当前在线连接数量,应该把它设计成线程安全的。
    private static int onlineCount = 0;
    //concurrent包是线程安全的Set，用来存放每个客户端对应的WebSocket对象。
    private static ConcurrentHashMap<String, WebSocketService> webSocketMap = new ConcurrentHashMap<>();
    //与某个客户端的连接会话，需要通过它来给客户端发送数据.
    private Session session;
    //接收客户端消息的uid
    private String uid = "";
    private SQLThread sqlThread;

    //连接建立成功调用的方法
    @OnOpen
    public void onOpen(Session session, @PathParam("uid") String uid) {
        this.session = session;
        this.uid = uid;
        // 创建数据库轮询线程，并启动
        sqlThread = new SQLThread(uid);
        Thread thread = new Thread(sqlThread);
        thread.start();
        if (webSocketMap.containsKey(uid)) {
            webSocketMap.remove(uid);
        }
        //加入到set中
        webSocketMap.put(uid, this);
        addOnlineCount();
        log.info("用户连接:" + uid + ",当前在线人数为:" + getOnlineCount());
        new Thread(sqlThread).start();
        try {
            sendMsg("连接成功");
        } catch (IOException e) {
            log.error("用户:" + uid + ",网络异常!!!!!!");
        }
    }

    //连接关闭调用的方法
    @OnClose
    public void onClose() {
        if (webSocketMap.containsKey(uid)) {
            webSocketMap.remove(uid);
            //从set中删除
            subOnlineCount();
        }
        // 停止数据库轮询线程
        if (sqlThread != null) {
            sqlThread.stopPolling();
        }
        log.info("用户退出:" + uid + ",当前在线人数为:" + getOnlineCount() + ",用户剩余查询次数");
    }

    /**
     * 收到客户端消息后调用的方法
     * @param message 客户端发送过来的消息
     */
    @OnMessage
    public void onMessage(String message) {
        log.info("用户id:" + uid + ",发送的报文:" + message);
        //可以群发消息
        //消息保存到数据库、redis
        if (!StringUtils.isEmpty(message)) {
            try {
                //解析发送的报文
                JSONObject jsonObject = JSON.parseObject(message);
                //追加发送人(防止串改)
                jsonObject.put("fromUID", this.uid);
                int file_num = Integer.parseInt(jsonObject.getString("file_num"));
                int queries_num = Integer.parseInt(jsonObject.getString("queries_num"));
                int remain_queries_num = queries_num - file_num;
                jsonObject.put("queries_num", remain_queries_num);
                String toUID = jsonObject.getString("toUID");
                //传送给对应的toUserId用户的WebSocket
                if (!StringUtils.isEmpty(toUID) && webSocketMap.containsKey(toUID)) {
                    webSocketMap.get(toUID).sendMsg(jsonObject.toJSONString());
                    log.info("向UserId:" + toUID + "发送成功");
                } else {
                    //若果不在这个服务器上，可以考虑发送到mysql或者redis
                    log.error("请求的UserId:" + toUID + "不在该服务器上");
                }
            } catch (Exception e) {
                e.getMessage();
                log.info(message);
            }
        }
    }

    //处理错误
    @OnError
    public void onError(Session session, Throwable error) {
        log.error("用户错误:" + this.uid + ",原因:" + error.getMessage());
        error.printStackTrace();
    }

    //实现服务器主动推送
    private void sendMsg(String msg) throws IOException {
        this.session.getBasicRemote().sendText(msg);
    }

    //发送自定义消息
    public static void sendInfo(String message, @PathParam("uid") String uid) throws IOException {
        log.info("发送消息到:" + uid + ",发送的报文:" + message);
        if (!StringUtils.isEmpty(uid) && webSocketMap.containsKey(uid)) {
            webSocketMap.get(uid).sendMsg(message);
        } else {
            log.error("用户" + uid + ",不在线！");
        }
    }

    private static synchronized int getOnlineCount() {
        return onlineCount;
    }

    private static synchronized void addOnlineCount() {
        WebSocketService.onlineCount++;
    }

    private static synchronized void subOnlineCount() {
        WebSocketService.onlineCount--;
    }
}
