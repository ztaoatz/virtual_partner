<template>
  <div class="register-container">
    <!-- 云朵装饰元素 -->
    <div class="cloud-decorations">
      <div class="cloud cloud1">☁</div>
      <div class="cloud cloud2">☁</div>
      <div class="cloud cloud3">☁</div>
      <div class="cloud cloud4">☁</div>
      <div class="cloud cloud5">☁</div>
    </div>
    
    <div class="register-card">      <div class="welcome-section">
        <img src="@/assets/linxi.png" class="logo" alt="灵犀一言" />
        <h2 class="welcome-title">加入我们</h2>
        <p class="welcome-subtitle">开始您的AI陪伴之旅 · 邮箱注册</p>
      </div>

      <form @submit.prevent="register" class="register-form">
        <!-- 邮箱注册表单 -->
        <div class="input-group">
          <div class="input-icon">👤</div>
          <input 
            v-model="username" 
            type="text" 
            placeholder="请输入用户名"
            class="warm-input"
            required
          />
        </div>

        <div class="input-group">
          <div class="input-icon">📧</div>
          <input 
            v-model="email" 
            type="email" 
            placeholder="请输入邮箱地址"
            class="warm-input"
            required
          />
        </div>

        <div class="input-group verification-group">
          <div class="input-icon">🔢</div>
          <input 
            v-model="verificationCode" 
            type="text" 
            placeholder="请输入邮箱验证码"
            class="warm-input verification-input"
            maxlength="6"
            required
          />
          <button 
            type="button" 
            class="send-code-btn"
            @click="sendVerificationCode"
            :disabled="!email || !isValidEmail(email) || codeSending || countdown > 0"
          >
            <span v-if="codeSending">发送中...</span>
            <span v-else-if="countdown > 0">{{ countdown }}s</span>
            <span v-else>发送验证码</span>
          </button>
        </div>
        
        <div class="input-group">
          <div class="input-icon">🔒</div>
          <input 
            v-model="password" 
            type="password" 
            placeholder="请设置密码"
            class="warm-input"
            required
          />
        </div>

        <div class="input-group">
          <div class="input-icon">🔐</div>
          <input 
            v-model="confirmPassword" 
            type="password" 
            placeholder="请确认密码"
            class="warm-input"
            required
          />
        </div>

        <div class="agreement-section">
          <label class="checkbox-label">
            <input type="checkbox" v-model="agreeToTerms" required />
            <span class="checkbox-custom"></span>
            <span class="agreement-text">我已阅读并同意 <a href="#" class="warm-link">用户协议</a> 和 <a href="#" class="warm-link">隐私政策</a></span>
          </label>
        </div>

        <button type="submit" class="register-btn" :disabled="!agreeToTerms || registering">
          <span class="btn-icon">🎨</span>
          <span v-if="registering">注册中...</span>
          <span v-else>创建账号</span>
        </button>

        <div class="divider">
          <span>已有账号？</span>
        </div>

        <button type="button" class="login-link" @click="goToLogin">
          <span class="btn-icon">🏠</span>
          返回登录
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue';
import axios from 'axios';
import router from "../router/index";

// 注册模式固定为邮箱注册
const registerMode = ref('email');
const username = ref('');
const email = ref('');
const password = ref('');
const confirmPassword = ref('');
const verificationCode = ref('');
const agreeToTerms = ref(false);

// 状态管理
const registering = ref(false);
const codeSending = ref(false);
const countdown = ref(0);

// 兼容性：保持原有的phoneNumber变量
const phoneNumber = ref('');
watch(username, (newVal) => {
  phoneNumber.value = newVal;
});

// 邮箱格式验证
const isValidEmail = (emailStr) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(emailStr);
};

// 发送邮箱验证码
const sendVerificationCode = async () => {
  if (!email.value || !isValidEmail(email.value)) {
    alert('请输入有效的邮箱地址');
    return;
  }

  try {
    codeSending.value = true;
    
    const response = await axios.post('http://127.0.0.1:8000/appp/send-verification-code/', {
      email: email.value,
      type: 'register'
    });

    if (response.data.success) {
      alert('验证码发送成功，请查收邮件');
      
      // 开始倒计时
      countdown.value = 60;
      const timer = setInterval(() => {
        countdown.value--;
        if (countdown.value <= 0) {
          clearInterval(timer);
        }
      }, 1000);
      
    } else {
      alert('验证码发送失败：' + response.data.message);
    }
  } catch (error) {
    console.error('发送验证码失败', error);
    alert('发送验证码失败，请稍后重试');
  } finally {
    codeSending.value = false;
  }
};

// 注册函数 - 只支持邮箱注册
const register = async () => {
  if (password.value !== confirmPassword.value) {
    alert("密码不一致，请重新确认");
    return;
  }

  // 密码强度检查
  if (password.value.length < 6) {
    alert("密码长度至少6位");
    return;
  }

  // 邮箱验证
  if (!email.value || !isValidEmail(email.value)) {
    alert('请输入有效的邮箱地址');
    return;
  }
  
  if (!verificationCode.value || verificationCode.value.length !== 6) {
    alert('请输入6位数字验证码');
    return;
  }

  try {
    registering.value = true;
    
    // 邮箱注册数据
    const registerData = {
      username: username.value,
      password: password.value,
      email: email.value,
      verification_code: verificationCode.value,
      nickname: username.value
    };

    const response = await axios.post('http://127.0.0.1:8000/appp/register/', registerData);

    if (response.data.success) {
      // 保存用户ID到localStorage
      if (response.data.user_id) {
        localStorage.setItem('virtual_partner_user_id', response.data.user_id);
      }
      
      alert("注册成功！您的邮箱已通过验证，欢迎加入灵犀一言大家庭");
      router.push("/login");
    } else {
      alert("注册失败: " + response.data.message);
    }
  } catch (error) {
    console.error("注册请求失败", error);
    if (error.response && error.response.data && error.response.data.message) {
      alert("注册失败: " + error.response.data.message);
    } else {
      alert("注册请求失败，请稍后重试");
    }
  } finally {
    registering.value = false;
  }
};

const goToLogin = () => {
  router.push("/login");
};
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  background: linear-gradient(135deg, 
    #fef7f0 0%,    /* 温暖的米色 */
    #fdf2e6 25%,   /* 奶油色 */
    #f8f4f0 50%,   /* 浅米色 */
    #e8f4fd 75%,   /* 淡天空蓝 */
    #d4e7f4 100%   /* 柔和蓝色 */
  );
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
  position: relative;
  overflow: hidden;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* 云朵装饰 */
.cloud-decorations {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

.cloud {
  position: absolute;
  font-size: 2.5rem;
  color: rgba(255, 255, 255, 0.7);
  animation: cloudFloat 10s ease-in-out infinite;
}

.cloud1 {
  top: 15%;
  left: 10%;
  animation-delay: 0s;
}

.cloud2 {
  top: 25%;
  right: 15%;
  animation-delay: 2s;
  font-size: 2rem;
}

.cloud3 {
  bottom: 30%;
  left: 8%;
  animation-delay: 4s;
  font-size: 2.2rem;
}

.cloud4 {
  bottom: 20%;
  right: 12%;
  animation-delay: 6s;
  font-size: 2.3rem;
}

.cloud5 {
  top: 50%;
  right: 5%;
  animation-delay: 8s;
  font-size: 1.8rem;
}

@keyframes cloudFloat {
  0%, 100% {
    transform: translateY(0px) translateX(0px);
    opacity: 0.7;
  }
  50% {
    transform: translateY(-15px) translateX(10px);
    opacity: 0.9;
  }
}

.register-card {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border-radius: 25px;
  padding: 40px;
  width: 100%;
  max-width: 450px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.3);
  position: relative;
  z-index: 2;
  transition: transform 0.3s ease;
  animation: cardSlideIn 0.8s ease-out;
}

@keyframes cardSlideIn {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.register-card:hover {
  transform: translateY(-3px);
}

.welcome-section {
  text-align: center;
  margin-bottom: 30px;
}

.logo {
  width: 70px;
  height: 70px;
  margin-bottom: 20px;
  border-radius: 50%;
  border: 3px solid rgba(216, 180, 140, 0.3);
  transition: transform 0.3s ease;
}

.logo:hover {
  transform: scale(1.05) rotate(3deg);
}

.welcome-title {
  font-size: 1.8rem;
  font-weight: 400;
  color: #8b6f47;
  margin-bottom: 8px;
  letter-spacing: 1px;
}

.welcome-subtitle {
  color: #a0956b;
  font-size: 0.9rem;
  margin-bottom: 0;
  font-weight: 400;
  line-height: 1.4;
}

.register-form {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.input-group {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 15px;
  font-size: 16px;
  z-index: 3;
  pointer-events: none;
  color: #9b8f7c;
}

.warm-input {
  width: 100%;
  padding: 15px 15px 15px 45px;
  border: 2px solid rgba(216, 180, 140, 0.3);
  border-radius: 12px;
  font-size: 15px;
  background: rgba(255, 255, 255, 0.8);
  transition: all 0.3s ease;
  outline: none;
  color: #7a6f5d;
}

.warm-input:focus {
  border-color: #d4c5a9;
  background: rgba(255, 255, 255, 0.95);
  box-shadow: 0 0 15px rgba(212, 197, 169, 0.2);
  transform: translateY(-1px);
}

.warm-input::placeholder {
  color: #b5a593;
  font-weight: 400;
}

.agreement-section {
  margin: 10px 0;
}

.checkbox-label {
  display: flex;
  align-items: flex-start;
  cursor: pointer;
  font-size: 13px;
  color: #8b7d6f;
  line-height: 1.4;
}

.checkbox-label input[type="checkbox"] {
  display: none;
}

.checkbox-custom {
  width: 16px;
  height: 16px;
  border: 2px solid #d4c5a9;
  border-radius: 3px;
  margin-right: 10px;
  margin-top: 2px;
  position: relative;
  transition: all 0.3s ease;
  flex-shrink: 0;
}

.checkbox-label input[type="checkbox"]:checked + .checkbox-custom {
  background: linear-gradient(135deg, #d4c5a9, #b8a082);
  border-color: #d4c5a9;
}

.checkbox-label input[type="checkbox"]:checked + .checkbox-custom::after {
  content: "✓";
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  color: white;
  font-size: 10px;
  font-weight: bold;
}

.agreement-text {
  flex: 1;
}

.warm-link {
  color: #a89276;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.3s ease;
}

.warm-link:hover {
  color: #8b6f47;
  text-decoration: underline;
}

.register-btn {
  background: linear-gradient(135deg, #d4c5a9, #b8a082);
  color: white;
  border: none;
  padding: 15px 30px;
  border-radius: 12px;
  font-size: 15px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  letter-spacing: 0.5px;
  box-shadow: 0 6px 20px rgba(212, 197, 169, 0.3);
}

.register-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(212, 197, 169, 0.4);
  background: linear-gradient(135deg, #c9b89c, #a89276);
}

.register-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-icon {
  font-size: 16px;
}

.divider {
  text-align: center;
  color: #b5a593;
  font-size: 13px;
  position: relative;
  margin: 15px 0;
}

.divider::before,
.divider::after {
  content: '';
  position: absolute;
  top: 50%;
  width: 35%;
  height: 1px;
  background: linear-gradient(to right, transparent, rgba(181, 165, 147, 0.3), transparent);
}

.divider::before {
  left: 0;
}

.divider::after {
  right: 0;
}

.login-link {
  background: linear-gradient(135deg, #e8f4fd, #d4e7f4);
  color: #7a6f5d;
  border: none;
  padding: 12px 30px;
  border-radius: 12px;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.login-link:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(212, 231, 244, 0.4);
  color: #6b6054;
}

/* 响应式设计 */
@media (max-width: 480px) {
  .register-container {
    padding: 15px;
  }
  
  .register-card {
    padding: 30px 25px;
    border-radius: 20px;
    max-width: 100%;
  }
  
  .welcome-title {
    font-size: 1.6rem;
  }
  
  .warm-input {
    padding: 12px 12px 12px 40px;
    font-size: 14px;
  }
  
  .input-icon {
    left: 12px;
    font-size: 15px;
  }
  
  .cloud {
    font-size: 2rem;
  }
  
  .cloud2, .cloud3, .cloud4, .cloud5 {
    font-size: 1.8rem;
  }
}

/* 增强动画效果 */
.input-group {
  animation: slideIn 0.6s ease-out both;
}

.input-group:nth-child(1) { animation-delay: 0.2s; }
.input-group:nth-child(2) { animation-delay: 0.3s; }
.input-group:nth-child(3) { animation-delay: 0.4s; }
.agreement-section { animation-delay: 0.5s; }
.register-btn { animation-delay: 0.6s; }
.login-link { animation-delay: 0.7s; }

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.agreement-section,
.register-btn,
.login-link {
  animation: slideIn 0.6s ease-out both;
}

/* 验证码输入组 */
.verification-group {
  position: relative;
}

.verification-input {
  padding-right: 140px !important;
}

.send-code-btn {
  position: absolute;
  right: 5px;
  top: 50%;
  transform: translateY(-50%);
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  white-space: nowrap;
}

.send-code-btn:hover:not(:disabled) {
  background: linear-gradient(135deg, #5a6fd8, #6a3093);
  transform: translateY(-50%) scale(1.02);
}

.send-code-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
  transform: translateY(-50%);
}
</style>