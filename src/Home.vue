<template>
  <el-container style="height: 705px">
    <el-container>
      <el-header class="el-header">
        <div style="display: flex; height: 60px">
          <div style="text-align: center; font-size: 25px; color: #f4f4f4; width: 260px;">DESIGN DEMO</div>
          <div style="width: 1120px"></div>
          <div style="text-align: right">
            <div>
              <div style="display: flex; text-align: right; height: 60px;vertical-align: middle">
                <div style="display: flex">
                  <el-popover placement="bottom-end" style="padding: 0">
                    <template #reference>
                      <el-button icon="el-icon-bell" circle style="margin-right: 30px"></el-button>
                    </template>
                    <el-table
                        :data="notifications"
                        style="width: 100%"
                        :cell-class-name="cellClassName">
                      <el-table-column
                          prop="title"
                          label="通知"
                          width="180"
                          @click="handleClickCell">
                      </el-table-column>
                      <el-table-column>
                        <template scope="scope">
                          <el-link @click="viewNotification(scope.row)" type="primary" target="_blank">
                            查看
                          </el-link>
                        </template>
                      </el-table-column>
                    </el-table>
                  </el-popover>
                </div>
                <div style="margin: 0 10px 0; height: 60px">
                  <el-popover style="padding: 0" placement="bottom-end">
                    <template #reference>
                      <el-button icon="el-icon-user" circle style="margin-right: 30px"></el-button>
                    </template>
                    <div style="padding: 20px 25px 0; width: 210px">
                      <div style="display: flex">
                        <template>
                          <el-avatar :src="circleUrl"/>
                        </template>
                        <div style="margin-left: 20px">
                          <div>
                            {{ this.username }}*
                          </div>
                          <div>
                            {{ this.userid }}#
                          </div>
                        </div>
                      </div>
                      <div
                          style="display: flex; padding-top: 20px; width: 100%; line-height: 22px; justify-content: space-between;">
                        <div>
                          <span>{{ this.usertype }}</span>
                        </div>
                        <div v-if="usertypeNum < 2">
                          <el-link @click="pay" target="_blank" :underline="false" type="primary">升级</el-link>
                        </div>
                        <div v-else>
                          <el-link target="_blank" disabled :underline="false" type="info">已是最高级</el-link>
                        </div>
                      </div>
                      <el-divider></el-divider>
                    </div>
                    <div style="padding: 0 25px 0; width: 210px">
<!--                      <div class="user-menu-item">-->
<!--                        <el-link href="https://element.eleme.io" target="_blank" :underline="false">-->
<!--                          <i class="el-icon-star-off" style="margin-right: 15px"></i>UI官网-->
<!--                        </el-link>-->
<!--                      </div>-->
                      <div class="user-menu-item">
                        <el-link @click="toUserInfo()" target="_blank" :underline="false">
                          <i class="el-icon-user" style="margin-right: 15px"></i>账号信息
                        </el-link>
                      </div>
                      <div class="user-menu-item">
                        <el-link @click="toOrder()" :underline="false">
                          <i class="el-icon-tickets" style="margin-right: 15px"></i>订单管理
                        </el-link>
                      </div>
                      <div class="user-menu-item">
                        <el-link @click="toSub()" :underline="false">
                          <i class="el-icon-star-off" style="margin-right: 15px"></i>使用记录
                        </el-link>
                      </div>
<!--                      <div class="user-menu-item">-->
<!--                        <el-link @click="toCSub()" :underline="false">-->
<!--                          <i class="el-icon-files" style="margin-right: 15px"></i>使用记录2-->
<!--                        </el-link>-->
<!--                      </div>-->
                      <div class="user-menu-item">
                        <el-link @click="toFeedBack()" :underline="false">
                          <i class="el-icon-files" style="margin-right: 15px"></i>错误反馈
                        </el-link>
                      </div>
                      <el-divider></el-divider>
                    </div>
                    <div style="padding: 0 25px 0">
                      <div class="user-menu-item">
                        <el-link @click="backToHome()" :underline="false">
                          <i class="el-icon-back" style="margin-right: 15px"></i>返回主页
                        </el-link>
                      </div>
                      <div class="user-menu-item">
                        <el-link @click="toLogin()" :underline="false">
                          <i class="el-icon-right" style="margin-right: 15px"></i>退出登录
                        </el-link>
                      </div>
                    </div>
                  </el-popover>
                  <div style="text-align: left">
                    <el-dialog
                        :visible.sync="dialogVisible"
                        width="70%">
                      <div>标题：{{ this.title }}</div>
                      <div>内容：{{ this.content }}</div>
                    </el-dialog>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </el-header>
      <div style="display: flex; background-color:#fafafa; height: 60px"
           v-if=$route.meta.showMenu>
<!--        <div style="width: 260px; background-color:#ffffff;"></div>-->
        <div style="display: flex; background-color:#ffffff; width: 260px;">
          <div class="innerUpper" style="margin-left: 26px">
            <el-button class="button" index="1" @click="to_file_home2" v-model="this.item_3">{{
                this.item_3
              }}
            </el-button>
          </div>
<!--          <div class="innerUpper">-->
<!--            <el-button class="button" index="2" @click="to_file_home1" v-model="this.item_4">{{-->
<!--                this.item_4-->
<!--              }}-->
<!--            </el-button>-->
<!--          </div>-->
          <div class="innerUpper">
            <el-button class="button" index="3" @click="to_home2" v-model="this.item_1">{{
                this.item_1
              }}
            </el-button>
          </div>
<!--          <div class="innerUpper">-->
<!--            <el-button class="button" index="4" @click="to_home1" v-model="this.item_2">{{-->
<!--                this.item_2-->
<!--              }}-->
<!--            </el-button>-->
<!--          </div>-->
        </div>
      </div>
      <el-main class="main" style="padding: 0">
        <keep-alive exclude="Dashboard">
          <router-view/>
        </keep-alive>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import {numToText} from "@/unity/api";

export default {
  data() {
    return {
      item_1: "文本",
      item_2: "text_class",
      item_3: "文件",
      item_4: "file_class",
      username: this.$cookie.get("username"),
      userid: this.$cookie.get("userid"),
      usertype: '',
      usertypeNum: '',
      circleUrl: "https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png",
      notifications: [],
      dialogVisible: false,
      row: '',
      title: '',
      content: '',
      notificationId: '',
    }
  },
  mounted() {
    this.$router.push('/file_home2')
    this.selectNotify()
    if (typeof WebSocket == "undefined") {
      console.log("您的浏览器不支持WebSocket");
    } else {
      this.setupWebSocket(); // 创建WebSocket连接
    }
  },
  methods: {
    selectNotify() {
      this.$axios.get('http://localhost:8080/notify_api/selectNotification').then((resp) => {
        this.notifications = resp.data
      })
    },
    cellClassName({row, rowIndex}) {
      row.index = rowIndex;
    },
    //点击某个单元格
    handleClickCell(row) {
      this.row = row.index;
      this.title = this.notifications[this.row].title
      this.content = this.notifications[this.row].content
      // 存储通知ID
      this.notificationId = this.notifications[this.row].id;
      // this.$emit('notificationSelected', { title: this.title, content: this.content });
    },
    toOrder() {
      this.$router.push('/orderInfo')
    },
    toUserInfo() {
      this.$router.push('/userInfo')
    },
    to_home1() {
      this.$router.push('/home1')
    },
    to_home2() {
      this.$router.push('/home2')
    },
    to_file_home2() {
      this.$router.push('/file_home2')
    },
    to_file_home1() {
      this.$router.push('/file_home1')
    },
    toLogin() {
      this.$router.push('/')
    },
    backToHome() {
      this.$router.push('/file_home2')
    },
    pay() {
      this.$router.push('/pay')
    },
    toSub() {
      this.$router.push('/subInfo')
    },
    toCSub() {
      this.$router.push('/cSubInfo')
    },
    toFeedBack() {
      this.$router.push('/feedback')
    },

    // websocket初始化
    setupWebSocket() {
      this.websocket = new WebSocket("ws://localhost:8080/socket_api/socket/" + this.userid); // 创建WebSocket连接
      this.websocket.onopen = this.onWebSocketOpen; // WebSocket连接打开时的处理函数
      this.websocket.onmessage = this.onWebSocketMessage; // 收到WebSocket消息时的处理函数
      this.websocket.onclose = this.onWebSocketClose; // WebSocket连接关闭时的处理函数
    },
    // 关闭WebSocket连接
    closeWebSocket() {
      if (this.websocket) {
        this.websocket.close();
      }
    },
    // 开启 WebSocket，启动心跳检测
    onWebSocketOpen() {
      console.log("WebSocket connection is open");
      this.startHeartbeat();
    },
    // 处理从服务器接收的消息
    onWebSocketMessage(event) {
      if (event.data) {
        try {
          const message = JSON.parse(event.data);
          console.log(message)
          //根据业务来处理数据
          console.log("Message from server ", message);
          localStorage.setItem("queries_num", message.queries_num)
          localStorage.setItem("usertype", message.usertype)
          this.queries_num = message.queries_num
          this.usertypeNum = message.usertype
          this.usertype = numToText(message.usertype)
          this.bus.$emit('submitUpload', this.queries_num)//注册事件，传值
          this.type.$emit('updateUsertype', numToText(message.usertype))
        } catch (e) {
          console.log(event.data())
        }
      }
    },
    // 关闭 WebSocket，停止心跳检测
    onWebSocketClose() {
      this.stopHeartbeat(); // WebSocket连接关闭时，停止心跳检测
      console.log("WebSocket connection is closed");
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
    beforeDestroy() {
      this.stopHeartbeat() // 停止心跳
      this.stopRestartWebsocket() // 停止重启
      this.closeWebSocket(); // 在组件销毁前关闭WebSocket连接
    },
    viewNotification(row) {
      this.row = row.index;
      this.title = this.notifications[this.row].title
      this.content = this.notifications[this.row].content
      this.titleVue.$emit('emitTitle', this.title)//注册事件，传值
      this.contentVue.$emit('emitContent', this.content)//注册事件，传值
      this.$router.push('/notification');
    },
  }
};
</script>

<style scoped>
.el-header {
  height: auto;
  background-color: #003366;
  color: #303133;
  line-height: 60px;
  align-content: center;
  padding: 0;
}

.main {
  background-color: #fafafa;
  height: 100%;
}

.user-menu-item {
  display: flex;
  padding: 8px 0;
  align-items: center;
}

.innerUpper {
  padding-left: 1rem;
  padding-right: 1rem;
  margin: 10px 5px 10px;
}

.button {
  border-radius: .6rem;
}
</style>
