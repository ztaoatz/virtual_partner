<template>
  <div class="reset-password-container">
    <!-- 云朵装饰元素 -->
    <div class="cloud-decorations">
      <div class="cloud cloud1">☁</div>
      <div class="cloud cloud2">☁</div>
      <div class="cloud cloud3">☁</div>
      <div class="cloud cloud4">☁</div>
    </div>
    
    <div class="reset-card">
      <div class="welcome-section">
        <img src="@/assets/linxi.png" class="logo" alt="灵犀一言" />
        <h2 class="welcome-title">重置密码</h2>
        <p class="welcome-subtitle">通过邮箱验证来重置您的密码</p>
      </div>

      <form @submit.prevent="resetPassword" class="reset-form">
        <div class="input-group">
          <div class="input-icon">📧</div>
          <input 
            v-model="email" 
            type="email" 
            placeholder="请输入注册邮箱"
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
            v-model="newPassword" 
            type="password" 
            placeholder="请输入新密码"
            class="warm-input"
            required
          />
        </div>

        <div class="input-group">
          <div class="input-icon">🔐</div>
          <input 
            v-model="confirmPassword" 
            type="password" 
            placeholder="请确认新密码"
            class="warm-input"
            required
          />
        </div>

        <button type="submit" class="reset-btn" :disabled="resetting">
          <span class="btn-icon">🔄</span>
          <span v-if="resetting">重置中...</span>
          <span v-else>重置密码</span>
        </button>

        <div class="divider">
          <span>还记得密码？</span>
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
import { ref } from 'vue';
import axios from 'axios';
import router from "../router/index";

const email = ref('');
const verificationCode = ref('');
const newPassword = ref('');
const confirmPassword = ref('');

// 状态管理
const resetting = ref(false);
const codeSending = ref(false);
const countdown = ref(0);

// 邮箱格式验证
const isValidEmail = (emailStr) => {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(emailStr);
};

// 发送验证码
const sendVerificationCode = async () => {
  if (!email.value || !isValidEmail(email.value)) {
    alert('请输入有效的邮箱地址');
    return;
  }

  try {
    codeSending.value = true;
    
    const response = await axios.post('http://127.0.0.1:8000/appp/send-verification-code/', {
      email: email.value,
      type: 'password_reset'
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

// 重置密码
const resetPassword = async () => {
  if (newPassword.value !== confirmPassword.value) {
    alert("两次输入的密码不一致");
    return;
  }

  if (newPassword.value.length < 6) {
    alert("密码长度至少6位");
    return;
  }

  if (!verificationCode.value || verificationCode.value.length !== 6) {
    alert('请输入6位数字验证码');
    return;
  }

  try {
    resetting.value = true;
    
    const response = await axios.post('http://127.0.0.1:8000/appp/reset-password/', {
      email: email.value,
      verification_code: verificationCode.value,
      new_password: newPassword.value
    });

    if (response.data.success) {
      alert("密码重置成功！请使用新密码登录");
      router.push("/login");
    } else {
      alert("密码重置失败: " + response.data.message);
    }
  } catch (error) {
    console.error("密码重置失败", error);
    if (error.response && error.response.data && error.response.data.message) {
      alert("密码重置失败: " + error.response.data.message);
    } else {
      alert("密码重置失败，请稍后重试");
    }
  } finally {
    resetting.value = false;
  }
};

const goToLogin = () => {
  router.push("/login");
};
</script>

<style scoped>
.reset-password-container {
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
  color: rgba(255, 255, 255, 0.6);
  animation: cloudFloat 20s ease-in-out infinite;
}

.cloud1 {
  top: 15%;
  left: 10%;
  animation-delay: 0s;
}

.cloud2 {
  top: 25%;
  right: 15%;
  animation-delay: -3s;
}

.cloud3 {
  bottom: 30%;
  left: 20%;
  animation-delay: -6s;
}

.cloud4 {
  bottom: 20%;
  right: 25%;
  animation-delay: -9s;
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

.reset-card {
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

.reset-card:hover {
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

.reset-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
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
  background: linear-gradient(135deg, #d4c5a9, #b8a082);
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
  background: linear-gradient(135deg, #c9b89c, #a89276);
  transform: translateY(-50%) scale(1.02);
}

.send-code-btn:disabled {
  background: #ccc;
  cursor: not-allowed;
  transform: translateY(-50%);
}

.reset-btn {
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

.reset-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(212, 197, 169, 0.4);
  background: linear-gradient(135deg, #c9b89c, #a89276);
}

.reset-btn:disabled {
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
  .reset-password-container {
    padding: 15px;
  }
  
  .reset-card {
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
}
</style>
