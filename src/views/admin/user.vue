<template>
  <el-container>
    <el-main style="margin: 0 0 0;">
      <el-input v-model="input_name" placeholder="请输入姓名" style="width: 20%; margin-bottom: 20px"></el-input>
      <el-button type="primary" @click="select" style="margin: 0 20px 0">搜索</el-button>
      <el-button type="primary" @click="dialogFormVisible = true" style="margin: 0 20px 0">添加</el-button>
      <!--添加用户-->
      <el-dialog style="margin: 0 0 0" :visible.sync="dialogFormVisible">
        <el-form :rules="rules" label-width="150px" :model="form" ref="form">
          <el-form-item prop="username" label="用户名">
            <el-input class="form_item" v-model="form.username" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item prop="usertype" label="会员等级">
            <el-radio-group v-model="form.usertype">
              <el-radio label=0 value=0>普通会员</el-radio>
              <el-radio label=1 value=1>中级会员</el-radio>
              <el-radio label=2 value=2>高级会员</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item prop="phone" label="手机">
            <el-input class="form_item" v-model="form.phone" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item prop="mail" label="邮箱">
            <el-input class="form_item" v-model="form.mail" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item prop="password" label="密码">
            <el-input class="form_item" v-model="form.password" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item prop="permission" label="是否为管理员">
            <el-radio-group v-model="form.permission">
              <el-radio label=true>管理员</el-radio>
              <el-radio label=false>用户</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item prop="queries_num" :v-show="form.permission===true" label="剩余查询次数">
            <el-input class="form_item" v-model="form.queries_num" autocomplete="off"></el-input>
          </el-form-item>
          <el-form-item v-if="form.usertype !== '0'" prop="permission" label="会员过期时间">
            <el-date-picker class="form_item" value-format="yyyy-MM-dd" type="date"
                            placeholder="选择日期"
                            v-model="form.expire_date"></el-date-picker>
          </el-form-item>
        </el-form>
        <div slot="footer">
          <el-button @click="dialogFormVisible = false">取 消</el-button>
          <el-button type="primary" @click="add(form); resetForm('form');dialogFormVisible = false;">确 定</el-button>
        </div>
      </el-dialog>

      <el-button @click="selectUser">刷新</el-button>
      <!--显示所有用户-->
      <el-table :data="tableData">
        <el-table-column prop="userid" label="用户ID">
          <template v-slot="scope">
            <span>{{ scope.row.userid }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="username" label="用户名">
          <template v-slot="scope">
            <el-input v-show="scope.row.show" v-model="scope.row.username"></el-input>
            <span v-show="!scope.row.show">{{ scope.row.username }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="usertype" label="会员等级">
          <template v-slot="scope">
            <el-select v-show="scope.row.show" v-model="scope.row.usertype" placeholder="请选择">
              <el-option
                  label="0"
                  value="0">
              </el-option>
              <el-option
                  label="1"
                  value="1">
              </el-option>
              <el-option
                  label="2"
                  value="2">
              </el-option>
            </el-select>
            <span v-show="!scope.row.show">{{ scope.row.usertype }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="phone" label="手机">
          <template v-slot="scope">
            <el-input v-show="scope.row.show" v-model="scope.row.phone"></el-input>
            <span v-show="!scope.row.show">{{ scope.row.phone }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="mail" label="邮箱">
          <template v-slot="scope">
            <el-input v-show="scope.row.show" v-model="scope.row.mail"></el-input>
            <span v-show="!scope.row.show">{{ scope.row.mail }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="password" label="密码">
          <template v-slot="scope">
            <el-input v-show="scope.row.show" v-model="scope.row.password"></el-input>
            <span v-show="!scope.row.show">{{ scope.row.password }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="queries_num" label="剩余查询次数">
          <template v-slot="scope">
            <el-input v-show="scope.row.show" v-model="scope.row.queries_num"></el-input>
            <span v-show="!scope.row.show">{{ scope.row.queries_num }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="permission" label="是否为管理员">
          <template v-slot="scope">
            <el-select v-show="scope.row.show" v-model="scope.row.permission" placeholder="请选择">
              <el-option
                  label="true"
                  value="true">
              </el-option>
              <el-option
                  label="false"
                  value="false">
              </el-option>
            </el-select>
            <span v-show="!scope.row.show">{{ scope.row.permission }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="expire_date" label="会员过期时间">
          <template v-slot="scope">
            <el-date-picker value-format="yyyy-MM-dd" v-show="scope.row.show && scope.row.usertype!==0" type="date"
                            placeholder="选择日期"
                            v-model="scope.row.expire_date"></el-date-picker>
            <span v-show="!scope.row.show || scope.row.usertype===0">{{ scope.row.expire_date }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作">
          <template v-slot="scope">
            <el-button type="primary" icon="el-icon-edit" circle v-show="!scope.row.show"
                       @click="edit(scope.row.username, scope.row.usertype, scope.row.phone, scope.row.mail,
                       scope.row.password,scope.row.queries_num, scope.row.permission, scope.row.expire_date);
                       scope.row.show=!scope.row.show; show=!show"></el-button>
            <el-button style="margin: 0" type="success" icon="el-icon-check" v-show="scope.row.show"
                       @click="updateByAdmin(scope.row); scope.row.show=!scope.row.show; show=!show"
                       circle></el-button>
            <el-button type="danger" icon="el-icon-delete" circle @click="deleteByAdmin(scope.row.userid)"></el-button>
            <span v-show="show"></span>
          </template>
        </el-table-column>
      </el-table>
    </el-main>
  </el-container>
</template>

<script>
import {AdminUpdate} from "@/unity/api";
import qs from "qs";

export default {
  name: "test3",
  created() {
    this.selectUser()
  },
  data() {
    return {
      input_name: '',
      input_age: '',
      tableData: [],
      old_username: '',
      old_usertype: -1,
      old_phone: '',
      old_mail: '',
      old_password: '',
      old_queries_num: -1,
      old_permission: false,
      old_expire_date: '',
      show: false,
      dialogFormVisible: false,
      form: {
        username: '111',
        usertype: '',
        phone: '111',
        mail: '111',
        password: '111',
        queries_num: 10,
        permission: '',
        expire_date: '',
      },
      rules: {
        username: [
          {required: true, message: '请输入用户名', trigger: 'blur'},
          {min: 1, max: 6, message: '长度在 1 到 6 个字符', trigger: 'blur'}
        ],
        usertype: [{required: true, message: '请选择用户会员类别', trigger: 'change'}],
        phone: [{required: true, message: '请输入手机', trigger: 'blur'}],
        mail: [{required: true, message: '请输入邮箱', trigger: 'blur'}],
        password: [{required: true, message: '请输入密码', trigger: 'blur'}],
        queries_num: [{required: true, message: '请输入剩余查询时间次数', trigger: 'blur'}],
        permission: [{required: true, message: '请选择是否为管理员', trigger: 'change'}],
        expire_date: [{type: 'date', required: true, message: '请选择时间', trigger: 'blur'}]
      }
    }
  },
  methods: {
    selectUser() {
      this.$axios.get("http://localhost:8080/user_api/admin/select_all_user").then((res) => {
        console.log(res.data)
        this.tableData = res.data
      })
    },

    add(form) {
      if (form.usertype === '0') {
        form.expire_date = 'null'
      }
      let userData = qs.stringify({
        username: form.username,
        usertype: form.usertype,
        phone: form.phone,
        mail: form.mail,
        password: form.password,
        queries_num: form.queries_num,
        permission: form.permission,
        expire_date: form.expire_date,
      })
      this.$axios.post("http://localhost:8080/user_api/admin/add_user_by_admin", userData).then(res => {
        console.log(res)
        switch (res.data) {
          case 0:
            this.$message.warning("用户名已存在")
            break
          case 1:
            this.$message.success("用户添加成功")
            this.selectUser()
            break
          case 2:
            this.$message.error("用户添加失败")
            break
        }
      })
    },

    deleteByAdmin(userid) {
      this.$axios.get("http://localhost:8080/user_api/admin/delete_user/" + userid).then(() => {
        this.$message.success("删除成功")
        this.selectUser()
        this.$refs.form.resetFields()
      })
    },

    edit(username, usertype, phone, mail, password, queries_num, permission, expire_date) {
      this.old_username = username
      this.old_usertype = usertype
      this.old_phone = phone
      this.old_mail = mail
      this.old_password = password
      this.old_queries_num = queries_num
      this.old_permission = permission
      this.old_expire_date = expire_date
    },

    updateByAdmin(row) {
      if (this.old_username === row.username
          && this.old_usertype === row.usertype
          && this.old_phone === row.phone
          && this.old_mail === row.mail
          && this.old_password === row.password
          && this.old_queries_num === row.queries_num
          && this.old_permission === row.permission
          && this.old_expire_date === row.expire_date) {
        this.$message.warning("未进行修改")
      } else {
        AdminUpdate("http://localhost:8080/user_api/admin/update_user_by_admin", row).then((res) => {
          if (res) {
            this.$message({
              message: '更改成功',
              type: 'success'
            })
          } else {
            this.$message({
              message: '更改失败',
              type: 'error'
            })
          }
        })
      }
    },
    select() {
      if (this.input_name !== '') {
        this.$axios.get('http://localhost:8080/user_api/admin/select_user_by_admin/' + this.input_name).then((res) => {
          if (res.data.length > 0) {
            this.tableData = res.data
            this.$message.success("查找成功")
          } else {
            this.$message.error("查找失败")
          }
        })
      } else {
        this.selectUser()
      }
    },
    resetForm(formName) {
      this.$refs[formName].resetFields();
    }
  }
}
</script>

<style scoped>
.form_item {
  width: 500px;
}
</style>