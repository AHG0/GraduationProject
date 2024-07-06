<template>
  <div class="notification-container">
    <div class="back-button" @click="goBack">
      <i class="el-icon-arrow-left"></i>
    </div>
    <h1 class="notification-title">通知内容</h1>
    <div class="notification-content">
      <h2>标题: {{ notification.title }}</h2>
      <p>内容: {{ notification.content }}</p>
    </div>
  </div>
</template>


<script>
export default {
  name: 'Notification',
  data() {
    return {
      notification: {
        title: '',
        content: ''
      }
    };
  },
  created() {
    // 监听事件，接收标题和内容
    this.titleVue.$on('emitTitle', title => {
      this.notification.title = title;
    });
    this.contentVue.$on('emitContent', content => {
      this.notification.content = content;
    });
  },
  methods: {
    goBack() {
      // 返回上一页
      this.$router.go(-1);
    }
  }
};
</script>

<style scoped>
.notification-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 40px;
  background-color: #f8f8f8;
  border-radius: 10px;
  position: relative;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); /* 添加阴影效果 */
}

.notification-title {
  font-size: 24px;
  color: #333333;
  margin-bottom: 20px;
}

.notification-content {
  font-size: 16px;
  color: #666666;
  line-height: 1.6;
  margin-bottom: 30px;
}

.back-button {
  position: fixed;
  top: 80px; /* 调整按钮位置，向下移动 */
  left: 20px;
  width: 50px;
  height: 50px;
  background-color: #cccccc;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  z-index: 9999; /* 确保按钮显示在其他内容上方 */
}

.back-button i {
  font-size: 24px;
  color: #ffffff;
}
</style>

