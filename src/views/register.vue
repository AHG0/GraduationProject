<template>
  <el-form :rules="rules" ref="form" :model="form" label-width="80px" class="form"
           style="background-color: #f4f4f5">
    <h3 style="text-align: center; line-height: 100px; margin: 0; padding: 0; letter-spacing: 10px">注册界面</h3>
    <el-form-item prop="username" label="用户名">
      <el-input style="width: 305px" v-model="form.username"></el-input>
    </el-form-item>
    <el-form-item prop="password" label="密码">
      <el-input style="width: 305px" v-model="form.password" show-password></el-input>
    </el-form-item>
    <el-form-item prop="phone" label="手机">
      <el-input style="width: 305px" v-model="form.phone"></el-input>
    </el-form-item>
    <el-form-item prop="mail" label="邮箱">
      <el-input style="width: 305px" v-model="form.mail"></el-input>
    </el-form-item>

    <el-form-item style="width: 400px; height: 30px" label-width="25px">
      <el-row style="height: 40px; width: 400px">
        <el-col style="width: 60px; text-align: left">
          <el-checkbox v-model="form.checked" label="记住密码"></el-checkbox>
        </el-col>
        <el-col style="width: 290px;text-align: right">
          <el-button type="info" @click="resetForm" style="align-content: center" round="round">重置</el-button>
        </el-col>
      </el-row>

    </el-form-item>
    <el-form-item style="width: 400px;text-align: center" label-width="0px">
      <el-button type="primary" @click="back">返回登录</el-button>
      <el-button style="text-align: center" @click="register">注册</el-button>
    </el-form-item>
  </el-form>
</template>
<router-view></router-view>

<script>

import {addUser} from "@/unity/api";

export default {
  name: "register",
  data() {
    return {
      form: {
        username: '',
        password: '',
        phone: '',
        mail: '',
        checked: true,
      },
      rules: {
        username: [{required: true, message: "请输入用户名", trigger: 'blur'}],
        password: [{required: true, message: "请输入密码", trigger: 'blur'}],
        phone: [{required: true, message: "请输入手机", trigger: 'blur'}],
        mail: [{required: true, message: "请输入邮箱", trigger: 'blur'}],
      }
    }
  },
  methods: {
    resetForm() {
      this.$refs.form.resetFields();
    },
    register() {
      console.log(this.form)
      if (this.form.name === "" || this.form.password === "") {
        this.$message.error("请输入用户名或密码")
      } else {
        addUser("http://localhost:8080/login_api/add_login", this.form.username, this.form.password, this.form.phone, this.form.mail).then(res => {
          if (res.data) {
            console.log(res)
            this.$message.success("注册成功")
            this.$router.push("/")
          } else {
            this.$message.error("用户名重复")
          }
        })
      }
    },
    back() {
      this.$router.push("/")
    }
  }
}

</script>
<style scoped>
.form {
  border: aliceblue;
  border-radius: 10px;
  height: 470px;
  width: 400px;
  margin: 100px auto;
  box-shadow: 0 1px 6px 0 rgba(0, 0, 0, 0.1)
}

html {
  height: 100%;
}

</style>