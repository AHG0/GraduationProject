<template>
  <div style="margin: 30px 30px 0">
    <el-form :model="notificationForm" ref="notificationForm" label-width="80px">
      <el-form-item label="通知标题" prop="title">
        <el-input v-model="notificationForm.title" placeholder="请输入通知标题"></el-input>
      </el-form-item>
      <el-form-item label="通知内容" prop="content">
        <el-input v-model="notificationForm.content" type="textarea" placeholder="请输入通知内容"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm">发布通知</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
export default {
  data() {
    return {
      notificationForm: {
        title: '',
        content: ''
      }
    };
  },
  methods: {
    submitForm() {
      var jsonData = {
        title: this.notificationForm.title,
        content: this.notificationForm.content
      }
      this.$axios.get('http://localhost:8080/notify_api/publishNotification', {params: jsonData}).then(resp => {
        this.$message.success("发布成功")
        console.log(resp.data)
      }).catch(() => {
        this.$message.error("发布失败")
      });
      this.$refs.notificationForm.resetFields();
    }
  }
};
</script>

<style>
/* 可以根据需要添加样式 */
</style>