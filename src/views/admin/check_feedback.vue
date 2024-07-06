<template>
  <div>
    <h2>反馈数据</h2>
    <el-table :data="feedbackList.slice((currentPage-1)*PageSize,currentPage*PageSize)" style="width: 100%">
      <el-table-column prop="id" label="ID"></el-table-column>
      <el-table-column prop="userid" label="用户ID"></el-table-column>
      <el-table-column prop="name" label="姓名"></el-table-column>
      <el-table-column prop="email" label="邮箱"></el-table-column>
      <el-table-column prop="phone" label="电话"></el-table-column>
      <el-table-column prop="module" label="模块"></el-table-column>
      <el-table-column prop="file_path" label="文件路径">
        <template v-slot="scope">
          <el-button type="text" @click="download(scope.row.file_path)">下载</el-button>
        </template>
      </el-table-column>
      <el-table-column prop="sub_time" label="提交时间" sortable></el-table-column>
      <el-table-column label="操作">
        <template v-slot="scope">
          <el-button v-if="!scope.row.content" type="primary" @click="openForm(scope.row)">处理</el-button>
          <el-button v-else type="info" @click="openForm(scope.row)">修改</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 表单 -->
    <el-dialog :visible.sync="formVisible" title="处理反馈" width="50%">
      <el-form :model="form" label-width="100px">
        <el-form-item label="用户ID">
          <el-input v-model="form.userid" disabled></el-input>
        </el-form-item>
        <el-form-item label="姓名">
          <el-input v-model="form.name" disabled></el-input>
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="form.email" disabled></el-input>
        </el-form-item>
        <el-form-item label="电话">
          <el-input v-model="form.phone" disabled></el-input>
        </el-form-item>
        <el-form-item label="模块">
          <el-input v-model="form.module" disabled></el-input>
        </el-form-item>
        <el-form-item label="反馈内容">
          <el-input type="textarea" v-model="form.content" :rows="4"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitForm">提交</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
    <div class="page">
      <el-pagination
          :background="true"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page.sync="currentPage"
          :page-sizes="pageSizes"
          :page-size="PageSize"
          :total="totalCount"
          layout="total, sizes, prev, pager, next, jumper">
      </el-pagination>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      feedbackList: [],
      currentPage: 1,
      totalCount: 0,
      pageSizes: [1, 5, 10],
      PageSize: 5,
      formVisible: false,
      form: {
        id: '',
        userid: '',
        name: '',
        email: '',
        phone: '',
        module: '',
        file_path: '',
        content: '',
        processResult: '',
      }
    };
  },
  mounted() {
    this.fetchFeedbackData();
  },
  methods: {
    fetchFeedbackData() {
      this.$axios.get('/feedback_api/getFeedback')
          .then(response => {
            this.feedbackList = response.data;
            console.log(response.data)
            this.totalCount = this.feedbackList.length
          })
          .catch(error => {
            console.error('获取反馈数据出错:', error);
          });
    },
    download(filepath) {
      let params = {filePath: filepath};

      this.$axios({
        url: "http://localhost:8096/downloadFile",
        method: "get",
        responseType: 'blob',
        params: params, // 通过params选项发送查询参数
      }).then(data => {
        // 获取数据（重点如何处理数据）
        var response = data.data;
        let url = window.URL.createObjectURL(new Blob([response]));
        let a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        // 设置新文件名称（注意文件后缀名）
        a.setAttribute('download', '');
        document.body.appendChild(a);
        // 点击下载
        a.click();
        // 下载完成移除元素
        document.body.removeChild(a);
        // 释放掉blob对象
        window.URL.revokeObjectURL(url);
      }).catch(error => {
        this.$message({message: error, type: 'error'});
      })
    },
    handleSizeChange(val) {
      this.PageSize = val
      this.currentPage = 1
    },
    handleCurrentChange(val) {
      this.currentPage = val
    },
    openForm(row) {
      this.formVisible = true;
      // 填充表单数据
      this.form.id = row.id;
      this.form.userid = row.userid;
      this.form.name = row.name;
      this.form.email = row.email;
      this.form.phone = row.phone;
      this.form.module = row.module;
      this.form.file_path = row.file_path;
      this.form.content = row.content;
    },
    submitForm() {
      // 提交表单
      const formData = {
        id: this.form.id,
        userid: this.form.userid,
        name: this.form.name,
        email: this.form.email,
        phone: this.form.phone,
        module: this.form.module,
        file_path: this.form.file_path,
        content: this.form.content,
      };
      console.log('提交处理结果:', formData.content);
      // 发送POST请求，将表单数据以JSON格式提交给后端
      this.$axios.post("/feedback_api/updateFeedback", formData, {
        headers: {
          'Content-Type': 'application/json'
        }
      })
          .then(() => {
            // 处理请求成功的逻辑
            this.$message.success('处理结果提交成功');
            this.formVisible = false;
            // 更新反馈列表中的处理状态和处理结果
            const feedbackIndex = this.feedbackList.findIndex(item => item.id === this.form.id);
            if (feedbackIndex !== -1) {
              this.feedbackList[feedbackIndex].processed = true;
              this.feedbackList[feedbackIndex].processResult = "处理完成";
            }
          })
          .catch(error => {
            // 处理请求失败的逻辑
            console.error('处理结果提交失败:', error);
            // 可以显示错误提示给用户
            this.$message({message: '处理结果提交失败', type: 'error'});
          });
    },
  }
};
</script>

<style scoped>
.page {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 0;
  padding: 0;
}
</style>
