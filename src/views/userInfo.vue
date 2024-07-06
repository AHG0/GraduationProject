<template>
  <el-container style="width: 100%">
    <el-main style="margin: 10px 100px 0;">
<!--      <el-button @click="selectById()">刷新</el-button>-->
      <el-table
          :data="tableData"
          style="width: 100%">
        <el-table-column prop="key" label="账号信息" width="600">
          <template v-slot="scope">
            <span class="accountTitle">{{ scope.row.key }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="value">
          <template v-slot="scope" style="display: flex">
            <el-input style="width: 80%" placeholder="请输入" v-show="scope.row.show"
                      v-model="new_value"></el-input>
            <span v-if="showPassword===true || scope.row.key!=='密码'" v-show="!scope.row.show">
              {{ scope.row.value }}
            </span>
            <span v-if="showPassword===false && scope.row.key==='密码'" v-show="!scope.row.show">*****</span>
            <span style="margin: 0 10px 0">
              <i @click="showPass()" class="el-icon-view" v-show="scope.row.key==='密码'"></i>
            </span>
          </template>
        </el-table-column>
        <el-table-column label="操作" align="right">
          <template v-slot="scope">
            <el-link type="primary" :underline="false"
                     v-show="!scope.row.show && scope.row.key !=='会员等级' && scope.row.key !=='会员过期时间'&& scope.row.key !=='今日剩余查询次数'"
                     @click="edit(scope.row.key, scope.row.value); scope.row.show = !scope.row.show; show=!show">
              编辑
            </el-link>
            <el-link type="primary" :underline="false" v-show="!scope.row.show && scope.row.key==='会员等级'"
                     @click="pay()">
              升级会员
            </el-link>
            <el-link v-if="scope.row.key ==='会员过期时间'"></el-link>
            <el-button size="small" style="margin: 0" type="success" icon="el-icon-check" v-show="scope.row.show"
                       @click="update(scope.row.key, scope.row.value); scope.row.show=!scope.row.show; show=!show"
                       circle></el-button>
            <el-button size="small" style="margin: 0 10px 0" type="danger" icon="el-icon-close" v-show="scope.row.show"
                       @click="back(scope.row.key, scope.row.value); scope.row.show=!scope.row.show; show=!show"
                       circle></el-button>
            <span v-show="show"></span>
          </template>
        </el-table-column>
      </el-table>
    </el-main>
  </el-container>
</template>

<script>
import {GetRequestByUserId, UserUpdate} from "@/unity/api";

export default {
  name: "test3",
  data() {
    return {
      tableData: [],
      // username: {key: '用户名', value: this.$cookie.get("username")},
      // phone: {key: '手机号码', value: this.$cookie.get("phone")},
      // password: {key: '密码', value: this.$cookie.get("password")},
      // mail: {key: '电子邮箱', value: this.$cookie.get("mail")},
      // expire_date: {key: '会员过期时间', value: this.$cookie.get("expire_date")},
      username: {key: '用户名', value: ''},
      phone: {key: '手机号码', value: ''},
      password: {key: '密码', value: ''},
      mail: {key: '电子邮箱', value: ''},
      expire_date: {key: '会员过期时间', value: ''},
      usertype: {key: '会员等级', value: ''},
      queries_num: {key: '今日剩余查询次数', value: ''},
      input_name: '',
      input_age: '',
      old_name: '',
      old_password: '',
      old_phone: '',
      old_mail: '',
      show: false,
      userid: this.$cookie.get("userid"),
      showPassword: false,
      new_value: '',
    }
  },
  created() {
    this.bus.$on('submitUpload', name => {
      this.queries_num.value = name
    })
    this.type.$on('updateUsertype', name => {
      this.usertype.value = name
    })

    this.selectById()
  },
  mounted() {
    this.selectById()
  },
  methods: {
    getUserInfo() {
      this.tableData = []
      this.tableData.push(this.username)
      this.tableData.push(this.phone)
      this.tableData.push(this.password)
      this.tableData.push(this.mail)
      this.tableData.push(this.usertype)
      this.tableData.push(this.expire_date)
      this.tableData.push(this.queries_num)
    },

    selectById() {
      GetRequestByUserId("http://localhost:8080/user_api/select_by_userid", this.userid).then((res) => {
        this.tableData = []
        var resData = res.data
        this.username.value = resData.username
        this.phone.value = resData.phone
        this.password.value = resData.password
        this.mail.value = resData.mail
        this.expire_date.value = resData.expire_date
        this.queries_num.value = localStorage.getItem("queries_num")
        this.usertype.value = localStorage.getItem("usertype")
        switch (resData.usertype) {
          case 0:
            this.usertype.value = '普通会员'
            break
          case 1:
            this.usertype.value = '中级会员'
            break
          case 2:
            this.usertype.value = '高级会员'
            break
        }
        this.getUserInfo()
      })
    },

    showPass() {
      this.showPassword = !this.showPassword
    },
    edit(key, value) {
      this.new_value = ''
      if (key === "用户名") {
        this.old_name = value;
      } else if (key === "密码") {
        this.old_password = value;
      } else if (key === "手机号码") {
        this.old_phone = value;
      } else if (key === "电子邮箱") {
        this.old_mail = value;
      }
    },

    update(key) {
      if (key === "用户名" && this.old_name === this.new_value) {
        this.$message.warning("未进行修改")
      } else if (key === "手机号码" && this.old_phone === this.new_value) {
        this.$message.warning("未进行修改")
      } else if (key === "密码" && this.old_password === this.new_value) {
        this.$message.warning("未进行修改")
      } else if (key === "电子邮箱" && this.old_mail === this.new_value) {
        this.$message.warning("未进行修改")
      } else {
        UserUpdate("http://localhost:8080/user_api/update_user", this.userid, key, this.new_value).then((res) => {
          if (res) {
            this.$message({
              message: '更改成功',
              type: 'success'
            })
            this.selectById()
          }
        })
      }
    },
    back() {
      this.$message.info("修改取消")
    },
    pay() {
      this.$router.push('/pay')
    },
  }
}
</script>

<style scoped>
.accountTitle {
  vertical-align: middle;
  width: 120px;
  display: inline-block;
  font-size: 13px;
  color: #888;
  margin: auto;
  height: 40px;
}
</style>