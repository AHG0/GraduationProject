<template>
  <el-container>
    <el-main style="margin: 0 0 0;">
      <el-input v-model="input_name" placeholder="请输入姓名" style="width: 20%; margin-bottom: 20px"></el-input>
      <el-button type="primary" @click="select" style="margin-left: 20px">搜索</el-button>
      <el-table :data="tableData" stripe>
        <el-table-column prop="userid" label="id" width="180">
        </el-table-column>
        <el-table-column prop="username" label="用户名" width="180">
          <template v-slot="scope">
            <span>{{ scope.row.username }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="usertype" label="会员等级" width="180">
          <template v-slot="scope">
            <span>{{ scope.row.usertype }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="phone"  label="手机">
          <template v-slot="scope">
            <span>{{ scope.row.phone }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="mail"  label="邮箱">
          <template v-slot="scope">
            <span>{{ scope.row.mail }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="password"  label="密码">
          <template v-slot="scope">
            <span>{{ scope.row.password }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="queries_num"  label="剩余查询次数">
          <template v-slot="scope">
            <span>{{ scope.row.queries_num }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="permission"  label="权限">
          <template v-slot="scope">
            <span>{{ scope.row.permission }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="expire_date"  label="会员过期时间">
          <template v-slot="scope">
            <span>{{ scope.row.expire_date }}</span>
          </template>
        </el-table-column>
      </el-table>
    </el-main>
  </el-container>
</template>

<script>
export default {
  name: "test3",
  created() {
    this.$axios.get("http://localhost:8080/user_api/admin/select_all_user").then((res) => {
      console.log(res.data)
      this.tableData = res.data
    })
  },
  data() {
    return {
      input_name: '',
      tableData: [],
    }
  },
  methods: {
    select(){
      this.$axios.get('http://localhost:8080/user_api/admin/select_user/' + this.input_name).then((res)=>{
        if(res.data.length > 0){
          this.tableData = res.data
          this.$message.success("查找成功")
        }else{
          this.$message.error("查找失败")
        }
      })
    }
  }
}
</script>

<style scoped>

</style>