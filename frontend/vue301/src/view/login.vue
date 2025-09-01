<template>
  <div class="content">
    <el-card class="login-card">
      <!-- 添加图片 -->
      <img src="@/assets/linxi.png" class="login-image" />
      <el-form :model="form">
        <el-form-item label="账号">
          <el-input v-model="form.username" placeholder="请输入账号" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" class="login-button" @click="onSubmit">登录</el-button>
        </el-form-item>
        <el-form-item>
          <el-button class="register-button" @click="onRegister">注册</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { reactive } from "vue";
import axios from "axios";
import router from "../router/index";



const form = reactive({
  username: "",
  password: "",
});

// 登录
const onSubmit = async () => {
  try {
    // 发送 POST 请求到后端进行登录验证
    const response = await axios.post('http://127.0.0.1:8000/appp/login/', {
      username: form.username,
      password: form.password,
    });

    // 检查响应结果
    if (response.data.success) {
      sessionStorage.setItem("menuList", JSON.stringify(response.data.menuList));
      sessionStorage.setItem("userInfo", JSON.stringify({ username: form.username }));
	  alert(response.data.message || "登录成功");
      router.push('/welcome');
    } else {
      alert(response.data.message || "登录失败");
    }
  } catch (error) {
    console.error("登录请求失败", error);
    alert("登录请求失败，请稍后重试");
  }
};

const onRegister = () => {
  router.push("/register"); // 假设注册页面的路径是 '/register'
};
</script>

<style lang="scss" scoped>
.content {
  background: linear-gradient(135deg, #C3C8F0, #5465E6);
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-card {
  padding: 30px;
  width: 400px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  border-radius: 10px;
  background-color: white;
}

.el-form-item {
  margin-bottom: 20px;
}

.login-button, .register-button {
  width: 100%;
  height: 45px;
  border-radius: 5px;
  font-size: 16px;
}

.login-button {
  background-color: #5465E6;
  color: white;
  border: none;
}

.register-button {
  background-color: #C3C8F0;
  color: white;
  border: none;
}

.login-image {
  width: 150px;
  height: auto; /* 自动调整高度以保持图片比例 */
  margin-bottom: 20px;
}
</style>