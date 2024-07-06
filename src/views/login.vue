<template>
  <el-main>
    <el-form :rules="rules" ref="form" :model="form" label-width="80px" class="form"
             style="background-color: #f4f4f5">
      <h3 style="text-align: center; line-height: 100px; margin: 0; padding: 0; letter-spacing: 10px">登录界面</h3>
      <el-form-item prop="name" label="用户名">
        <el-input style="width: 305px" v-model="form.name"></el-input>
      </el-form-item>
      <el-form-item prop="password" label="密码">
        <el-input style="width: 305px" v-model="form.password" show-password></el-input>
      </el-form-item>

      <el-row>
        <el-col style="width: 270px">
          <el-form-item style="width: 270px" prop="inputCode" label="验证码">
            <el-input style="width: 180px" v-model="form.inputCode"></el-input>
          </el-form-item>
        </el-col>
        <el-col style="width: 100px; text-align: center">
          <div class="s-canvas" @click="createdCode">
            <canvas id="s-canvas" :width="contentWidth" :height="contentHeight"></canvas>
          </div>
        </el-col>
      </el-row>

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
        <el-button type="primary" @click="onSubmit">登录</el-button>
        <el-button style="text-align: center" @click="register">注册</el-button>
      </el-form-item>
    </el-form>
  </el-main>
</template>
<router-view></router-view>

<script>

import {GetRequests, numToText} from "@/unity/api";

export default {
  name: "Login",
  data() {
    return {
      identifyCode: '',
      form: {
        name: 'hst',
        password: '123',
        inputCode: '',
        checked: true,
      },
      rules: {
        name: [{required: true, message: "请输入用户名", trigger: 'blur'}],
        password: [{required: true, message: "请输入密码", trigger: 'blur'}],
        inputCode: [{required: true, message: "请输入验证码", trigger: 'blur'}],
      }
    }
  },
  mounted() {
    this.createdCode()
  },
  methods: {
    resetForm() {
      this.$refs.form.resetFields();
    },
    register() {
      this.$router.push('/register')
    },
    onSubmit() {
      GetRequests("http://localhost:8080/login_api/userLogin", this.form.name, this.form.password, this.form.inputCode).then((resp) => {
        if (this.form.inputCode === this.identifyCode) {
        // if (this.identifyCode === this.identifyCode) {
          if (resp != null) {
            if (resp.data.permission === false) {
              console.log(resp.data)
              this.$message.success("登陆成功")
              this.$axios.get("http://localhost:8080/user_api/countLogin", {
                headers: {
                  token: resp.data.token
                }
              })
              this.$router.push("/Home")
              if (resp.data.isExpire === 1) {
                this.$message.info("会员已过期")
              }
              this.$cookie.set('usertype', numToText(resp.data.usertype))
              this.$cookie.set('mail', resp.data.mail)
              this.$cookie.set('phone', resp.data.phone)
              this.$cookie.set('username', resp.data.username)
              this.$cookie.set('password', resp.data.password)
              this.$cookie.set('userid', resp.data.userid)
              this.$cookie.set('usertypeNum', resp.data.usertype)
              this.$cookie.set('permission', resp.data.permission)
              this.$cookie.set('expire_date', resp.data.expire_date)
              this.$cookie.set("queries_num", resp.data.queries_num)

              localStorage.setItem("token", resp.data.token)
              localStorage.setItem("userid", resp.data.userid)
              localStorage.setItem("usertype", resp.data.usertype)
              localStorage.setItem("queries_num", resp.data.queries_num)
            }
            if (resp.data.permission === true) {
              console.log(resp.data)
              this.$message.success("管理员登陆成功")
              this.$cookie.set('mail', resp.data.mail)
              this.$cookie.set('phone', resp.data.phone)
              this.$cookie.set('password', resp.data.password)
              this.$cookie.set('usertype', resp.data.usertype)
              this.$cookie.set('username', resp.data.username)
              this.$cookie.set('userid', resp.data.userid)
              this.$cookie.set('permission', resp.data.permission)
              this.$cookie.set('expire_date', resp.data.expire_date)
              localStorage.setItem("token", resp.data.token)
              this.$router.push("/Admin")
            }
          } else {
            this.$message.error("用户名或密码错误")
          }
        } else {
          if (this.form.inputCode === '') {
            this.$message.info("请输入验证码")
          } else {
            this.$message.error("验证码错误")
          }
        }
      })
    },

    // 生成4个随机数
    createdCode() {
      const len = 4
      const codeList = []
      const chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz0123456789'
      const charsLen = chars.length
      for (let i = 0; i < len; i++) {
        codeList.push(chars.charAt(Math.floor(Math.random() * charsLen)))
      }
      this.identifyCode = codeList.join('')
      this.$emit('getIdentifyCode', this.identifyCode.toLowerCase())
      this.drawPic()
    },

    // 生成一个随机数
    randomNum(min, max) {
      return Math.floor(Math.random() * (max - min) + min)
    },
    // 生成一个随机的颜色
    randomColor(min, max) {
      const r = this.randomNum(min, max)
      const g = this.randomNum(min, max)
      const b = this.randomNum(min, max)
      return 'rgb(' + r + ',' + g + ',' + b + ')'
    },

    drawPic() {
      const canvas = document.getElementById('s-canvas')
      const ctx = canvas.getContext('2d')
      ctx.textBaseline = 'bottom'
      // 绘制背景
      ctx.fillStyle = this.randomColor(this.backgroundColorMin, this.backgroundColorMax)
      ctx.fillRect(0, 0, this.contentWidth, this.contentHeight)
      // 绘制文字
      for (let i = 0; i < this.identifyCode.length; i++) {
        this.drawText(ctx, this.identifyCode[i], i)
      }
      this.drawLine(ctx)
      this.drawDot(ctx)
    },

    drawText(ctx, txt, i) {
      ctx.fillStyle = this.randomColor(this.colorMin, this.colorMax)
      ctx.font = this.randomNum(this.fontSizeMin, this.fontSizeMax) + 'px SimHei'
      const x = (i + 1) * (this.contentWidth / (this.identifyCode.length + 1))
      const y = this.randomNum(this.fontSizeMax, this.contentHeight - 5)
      var deg = this.randomNum(-45, 45)
      // 修改坐标原点和旋转角度
      ctx.translate(x, y)
      ctx.rotate(deg * Math.PI / 180)
      ctx.fillText(txt, 0, 0)
      // 恢复坐标原点和旋转角度
      ctx.rotate(-deg * Math.PI / 180)
      ctx.translate(-x, -y)
    },

    // 绘制干扰线
    drawLine(ctx) {
      for (let i = 0; i < 5; i++) {
        ctx.strokeStyle = this.randomColor(this.lineColorMin, this.lineColorMax)
        ctx.beginPath()
        ctx.moveTo(this.randomNum(0, this.contentWidth), this.randomNum(0, this.contentHeight))
        ctx.lineTo(this.randomNum(0, this.contentWidth), this.randomNum(0, this.contentHeight))
        ctx.stroke()
      }
    },

    // 绘制干扰点
    drawDot(ctx) {
      for (let i = 0; i < 80; i++) {
        ctx.fillStyle = this.randomColor(0, 255)
        ctx.beginPath()
        ctx.arc(this.randomNum(0, this.contentWidth), this.randomNum(0, this.contentHeight), 1, 0, 2 * Math.PI)
        ctx.fill()
      }
    }
  },
  props: {
    fontSizeMin: {
      type: Number,
      default: 25
    },
    fontSizeMax: {
      type: Number,
      default: 30
    },
    backgroundColorMin: {
      type: Number,
      default: 255
    },
    backgroundColorMax: {
      type: Number,
      default: 255
    },
    colorMin: {
      type: Number,
      default: 0
    },
    colorMax: {
      type: Number,
      default: 160
    },
    lineColorMin: {
      type: Number,
      default: 100
    },
    lineColorMax: {
      type: Number,
      default: 255
    },
    dotColorMin: {
      type: Number,
      default: 0
    },
    dotColorMax: {
      type: Number,
      default: 255
    },
    contentWidth: {
      type: Number,
      default: 100
    },
    contentHeight: {
      type: Number,
      default: 40
    }
  },
}

</script>
<style scoped>
.form {
  border: aliceblue;
  border-radius: 15px;
  height: 400px;
  width: 400px;
  margin: 120px auto;
  box-shadow: 0 1px 12px 0 rgba(0, 0, 0, 0.1)
}

.s-canvas {
  height: 40px;
  cursor: pointer;
}

.s-canvas canvas {
  margin-top: 1px;
  margin-left: 8px;
}

html {
  height: 100%;
}
</style>