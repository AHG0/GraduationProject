<template>
  <div style="text-align: center; margin: 20px 0 0">
    <el-button type="primary" @click="openFeedbackForm">打开反馈表单</el-button>
    <el-divider></el-divider>
    <el-dialog
        title="反馈表单"
        :visible.sync="dialogVisible"
        :close-on-click-modal="false"
        @close="handleDialogClose"
    >
      <div class="feedback-form" style="text-align: left">
        <el-form ref="feedbackForm" :model="feedback" label-width="100px">
          <el-form-item label="姓名" prop="name">
            <el-input v-model="feedback.name"></el-input>
          </el-form-item>
          <el-form-item label="邮箱" prop="email">
            <el-input v-model="feedback.email"></el-input>
          </el-form-item>
          <el-form-item label="联系电话" prop="phone">
            <el-input v-model="feedback.phone"></el-input>
          </el-form-item>
          <el-form-item label="出错模块" prop="module">
            <el-select v-model="feedback.module" placeholder="请选择">
              <el-option label="抽取" value="抽取"></el-option>
              <el-option label="分类" value="分类"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="上传文件">
            <el-upload
                class="upload-demo"
                action=""
                drag
                multiple
                :auto-upload="false"
                :file-list="fileList"
                :on-change="handleChange"
                :http-request="submitForm">
              <i class="el-icon-upload"></i>
              <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
              <div class="el-upload__tip" slot="tip">上传txt格式文件</div>
            </el-upload>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitForm">提交反馈</el-button>
            <el-button type="info" @click="removeFiles">清空文件</el-button>
          </el-form-item>
        </el-form>
      </div>
    </el-dialog>
    <el-table :data="form" style="width: 100%">
      <el-table-column prop="id" label="ID"></el-table-column>
      <el-table-column prop="userid" label="用户ID"></el-table-column>
      <el-table-column prop="name" label="姓名"></el-table-column>
      <el-table-column prop="email" label="邮箱"></el-table-column>
      <el-table-column prop="phone" label="电话"></el-table-column>
      <el-table-column prop="module" label="模块"></el-table-column>
      <el-table-column prop="content" label="处理结果"></el-table-column>
    </el-table>
  </div>
</template>

<script>
import {PostFile} from "@/unity/api";

export default {
  data() {
    return {
      form: [],
      feedback: {
        name: '1',
        email: '1',
        phone: '1',
        module: ''
      },
      fileList: [],
      dialogVisible: false
    };
  },
  created() {
    this.selectById()
  },
  methods: {
    openFeedbackForm() {
      this.dialogVisible = true;
    },
    handleDialogClose() {
      this.feedback = {
        name: '',
        email: '',
        phone: '',
        module: ''
      };
      this.fileList = [];
    },
    submitForm() {
      if (this.fileList.length === 0) {
        this.$message.warning("提交文件为空")
      } else {
        var formData = new FormData;
        formData.append('name', this.feedback.name);
        formData.append('email', this.feedback.email);
        formData.append('phone', this.feedback.phone);
        formData.append('module', this.feedback.module);
        this.fileList.forEach(val => {
          formData.append('files', val.raw);
        });
        PostFile("http://localhost:8096/submitFeedback", formData)
            .then(resp => {
              this.$message.success(resp.data)
              // 处理成功提交后的逻辑
            })
            .catch(error => {
              console.error('Error submitting feedback:', error);
              // 处理提交失败后的逻辑
            });
      }
    },
    selectById() {
      this.$axios.get("/feedback_api/getFeedbackById", {params: {userid: this.$cookie.get("userid")}})
          .then((rsep) => {
            this.form = rsep.data
          })
    },
    handleChange(file) {
      this.fileList.push(file);
    },
    removeFiles() {
      this.fileList = []
    },

  }
};
</script>

<style>
.feedback-form {
  max-width: 500px;
  margin: 0 auto;
}
</style>
