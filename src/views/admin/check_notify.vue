<template>
  <div>
    <el-card>
      <div slot="header" class="clearfix">
        <span>通知列表</span>
      </div>
      <el-table :data="notifications" style="width: 100%">
        <el-table-column label="标题" prop="title" width="180"></el-table-column>
        <el-table-column label="内容" prop="content"></el-table-column>
        <el-table-column label="发布时间" prop="time" sortable></el-table-column>
        <el-table-column label="操作">
          <template v-slot="scope">
            <el-button type="primary" icon="el-icon-edit" circle
                       @click="edit(scope.row.id, scope.row.title, scope.row.content)"></el-button>
            <el-button type="danger" icon="el-icon-delete" circle @click="deleteNotify(scope.row.id)"></el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog title="修改通知" :visible.sync="dialogFormVisible">
      <el-form :model="form" ref="form">
        <el-form-item label="标题">
          <el-input v-model="form.title" autocomplete="off" placeholder="请输入通知标题"></el-input>
        </el-form-item>
        <el-form-item label="内容">
          <el-input v-model="form.content" type="textarea" placeholder="请输入通知内容">
          </el-input>
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="dialogFormVisible = false">取 消</el-button>
        <el-button type="primary" @click="update()">保 存</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
    return {
      notifications: [],
      dialogFormVisible: false,
      old_title: '',
      old_content: '',
      form: {
        id: '',
        title: '',
        content: '',
      },
    }
  },
  created() {
    this.selectNotify()
  },
  methods: {
    selectNotify() {
      this.$axios.get('http://localhost:8080/notify_api/selectNotification').then((resp) => {
        this.notifications = resp.data
      })
    },

    edit(id, title, content) {
      this.dialogFormVisible = true
      this.old_title = title
      this.old_content = content
      this.form.id = id
      this.form.title = title
      this.form.content = content
    },

    update() {
      if (this.old_title === this.form.title && this.old_content === this.form.content) {
        this.$message.warning("未进行修改")
      } else {
        this.$axios.get("http://localhost:8080/notify_api/update_notify", {params: this.form}).then((res) => {
          this.dialogFormVisible = false
          if (res) {
            this.$message.success("更改成功")
            this.selectNotify()
          }
        })
      }
    },
    deleteNotify(id) {
      this.$axios.get("http://localhost:8080/notify_api/delete_notify", {params: {"id": id}}).then(() => {
        this.$message.success("删除成功")
        this.selectNotify()
      })
    },
  }
};
</script>

<style scoped>
.clearfix {
  text-align: left;
}
</style>