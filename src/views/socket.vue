<template>
  <div>
    <el-row class="app-container">
      <el-button type="primary" @click="testSend">主要按钮</el-button>
    </el-row>
    {{ data }}
  </div>
</template>

<script>
export default {
  name: 'Monitoring',
  data() {
    return {
      websocket: null, // WebSocket对象
      reconnectInterval: 3000, // 重连间隔时间（毫秒）
      restartWebsocket: null, // 重启定时器
      heartbeatInterval: null, // 心跳定时器
      userid: localStorage.getItem("userid"),
      data: localStorage.getItem("queries_num"),
    };
  },
  created() {
    if (typeof WebSocket == "undefined") {
      console.log("您的浏览器不支持WebSocket");
    } else {
      this.setupWebSocket(); // 创建WebSocket连接
    }
  },
  methods: {
    testSend() { // 测试
      const send = {
        "toUID": this.userid,
        "data": this.data
      }
      this.sendMessage(JSON.stringify(send));
    },
    // websocket初始化
    setupWebSocket() {
      this.websocket = new WebSocket("ws://localhost:8094/socket/" + this.userid); // 创建WebSocket连接
      this.websocket.onopen = this.onWebSocketOpen; // WebSocket连接打开时的处理函数
      this.websocket.onmessage = this.onWebSocketMessage; // 收到WebSocket消息时的处理函数
      this.websocket.onclose = this.onWebSocketClose; // WebSocket连接关闭时的处理函数
    },
    closeWebSocket() { // 关闭
      if (this.websocket) {
        this.websocket.close(); // 关闭WebSocket连接
      }
    },
    // 开启 WebSocket;启动心跳检测
    onWebSocketOpen() {
      console.log("WebSocket connection is open");
      this.startHeartbeat();
    },
    // 处理从服务器接收的消息
    onWebSocketMessage(event) {
      if (event.data) {
        try {
          const message = JSON.parse(event.data);
          //    根据业务来处理数据
          console.log("Message from server ", message);
          this.data = localStorage.getItem("queries_num")
        } catch (e) {
          console.log(event.data())
        }

      }
    },
    // 关闭 WebSocket;停止心跳检测
    onWebSocketClose() {
      console.log("WebSocket connection is closed");
      this.stopHeartbeat(); // WebSocket连接关闭时，停止心跳检测
      this.restartWebsocket = setTimeout(this.setupWebSocket, this.reconnectInterval); // 在一定时间后重连WebSocket
    },
    // 向服务器发送消息
    sendMessage(message) {
      if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
        this.websocket.send(message); // 发送消息到WebSocket服务器
      }
    },
    // 开启心跳检测
    startHeartbeat() {
      this.heartbeatInterval = setInterval(() => {
        if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
          this.websocket.send('heartbeat'); // 发送心跳消息
        }
      }, 30000); // 每30秒发送一次心跳
    },
    // 停止心跳检测
    stopHeartbeat() {
      if (this.heartbeatInterval) {
        clearInterval(this.heartbeatInterval); // 停止心跳检测定时器
      }
    },
    // 停止重启检测
    stopRestartWebsocket() {
      if (this.restartWebsocket) {
        clearInterval(this.restartWebsocket); // 停止心跳检测定时器
      }
    },
  },
  beforeDestroy() {
    this.stopHeartbeat() // 停止心跳
    this.stopRestartWebsocket() // 停止重启
    this.closeWebSocket(); // 在组件销毁前关闭WebSocket连接
  },
}
</script>

<style scoped>

</style>