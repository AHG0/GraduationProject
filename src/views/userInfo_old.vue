<template>
  <main class="el-main common-main-entity">
    <div class="main-content">
      <div class="cm-content">
        <div style="margin-top: 4px;">
          <div class="product-title flexRow" style="justify-content: space-between; align-items: center;">
            <div class="desc-title" style="display: inline-block; vertical-align: middle;">账号信息</div>
            <div class="login-out desc-title"
                 style="vertical-align: middle; font-weight: normal;">退出登录
            </div>
          </div>
          <div class="accountSettingContent">
            <div class="accountTitle">头像</div>
            <div class="accountSub">
              <div class="user-icon-container"><span
                  class="el-avatar el-avatar--small el-avatar--circle"
                  style="vertical-align: middle;"><img
                  src="https://thirdwx.qlogo.cn/mmopen/vi_32/LricIxYhlhvhgGnsQfwdHYop0Oeu502bS5n9NZDdNicBYiaM4Yg8eoZQJpvjDMN3DEDYvRxodmaczrvolxeeKSEWQ/132"
                  style="object-fit: cover;"></span>
                <div class="top-left-corner"></div>
              </div></div>
            <div class="updateDiv">修改头像</div>
            <div class="accountTitle"><span>昵称</span></div>
            <div class="accountSub"><span>Daisy</span></div>
            <div class="updateDiv">修改昵称</div>
            <div class="accountTitle"><span>手机号码</span></div>
            <div class="accountSub"><span>139****1891</span></div>
            <div data-tag-id="updatePhone" class="updateDiv">修改手机</div>
            <div class="accountTitle"><span>登录密码</span></div>
            <div class="accountSub"><span>******</span></div>
            <div data-tag-id="updatePassword" class="updateDiv">修改密码</div>
            <div class="accountTitle"><span>电子邮箱</span></div>
            <div class="accountSub"><span></span></div>
            <div data-tag-id="updateEmail" class="updateDiv">修改邮箱</div>
            <div class="accountTitle"><span>账号类型</span></div>
            <div class="accountSub"><span>免费版</span></div>
            <div data-tag-id="updateAccount" class="updateDiv">账户升级</div>
            <div></div>
            <div></div>
            <div data-tag-id="updateAccount" class="updateDiv logOffAccount">注销账户</div>
          </div>
        </div>
      </div>
    </div>
  </main>
</template>
<script setup>

</script>
<style scoped>
.common-main-entity {
  overflow-y: auto;
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  flex-flow: column;
}

.el-footer, .el-main {
  box-sizing: border-box;
}

.el-main {
  display: block;
  flex: 1;
  flex-basis: auto;
  overflow: auto;
}

.el-card__body, .el-main {
  padding: 20px;
}

.main-content {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  flex-flow: column;
}

.cm-content {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: 0 40px;
}

.fullscreen, .product-title {
  margin-bottom: 24px;
}

.flexRow, .flexRow-center {
  display: -webkit-box;
  display: -ms-flexbox;
  display: flex;
  flex-direction: row;
  align-items: center;
}

.desc-title {
  font-weight: 700;
  line-height: 24px;
  color: #4b4b4b;
  font-size: 16px;
}

.fullscreen .product-title .login-out {
  float: right;
  display: inline-block;
  cursor: pointer;
}

.desc-title {
  font-weight: 700;
  line-height: 24px;
  color: #4b4b4b;
  font-size: 16px;
}

.accountSettingContent {
  display: grid;
  align-items: center;
  grid-template-columns: max-content 5fr max-content;
  grid-auto-rows: 56px;
}

.accountSettingContent .accountTitle {
  width: 80px;
  display: inline-block;
  font-size: 13px;
  color: #888;
  padding-right: 10px;
}

.accountSettingContent .accountSub {
  display: -ms-inline-flexbox;
  display: inline-flex;
  align-items: center;
  gap: 20px;
  width: 550px;
  font-size: 13px;
  color: #111;
}

.accountSettingContent .updateDiv {
  display: inline-block;
  width: 100%;
  color: #2470ff;
  cursor: pointer;
  font-size: 13px;
  text-align: right;
}
</style>