<template>
  <div class="register-page">
    <div class="register-box">
      <h2>注册</h2>
      <form @submit.prevent="register">
        <div class="form-group">
          <input
            type="text"
            v-model="phoneNumber"
            placeholder="账号"
            required
          />
        </div>
        <div class="form-group">
          <input
            type="password"
            v-model="password"
            placeholder="密码"
            required
          />
        </div>
        <div class="form-group">
          <input
            type="password"
            v-model="confirmPassword"
            placeholder="确认密码"
            required
          />
        </div>
        <button type="submit" class="register-button">注册</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'; // 添加：导入 ref
import axios from 'axios'; // 添加：导入 axios
import router from "../router/index";
const phoneNumber = ref('');
const password = ref('');
const confirmPassword = ref('');

const register = async () => { // 添加：定义 register 函数
  if (password.value !== confirmPassword.value) {
    alert("密码不一致");
    return;
  }

  try {
    const response = await axios.post('http://127.0.0.1:8000/appp/register/', {
      phoneNumber: phoneNumber.value,
      password: password.value,
    });

    if (response.data.success) {
      alert("注册成功");
	  router.push("/login");
    } else {
      alert("注册失败: " + response.data.message);
    }
  } catch (error) {
    console.error("注册请求失败", error);
    alert("注册请求失败，请稍后重试");
  }
};
</script>

<style scoped>
.register-page {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f8ff;
}

.register-box {
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  padding: 40px;
  width: 300px;
  text-align: center;
}

h2 {
  margin-bottom: 20px;
  color: #333333;
}

.form-group {
  margin-bottom: 20px;
}

input {
  width: 100%;
  padding: 10px;
  margin: 5px 0;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.register-button {
  width: 100%;
  padding: 10px;
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.register-button:hover {
  background-color: #357abd;
}
</style>