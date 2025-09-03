<template>
  <div class="start-container">
    <!-- 云朵装饰元素 -->
    <div class="cloud-decorations">
      <div class="cloud cloud1">☁</div>
      <div class="cloud cloud2">☁</div>
      <div class="cloud cloud3">☁</div>
      <div class="cloud cloud4">☁</div>
    </div>
    
    <!-- 主要内容 -->
    <div class="content-wrapper">
      <div class="logo-section">
        <img src="@/assets/linxi.png" class="main-logo" alt="灵犀一言" />
        <h1 class="app-title">灵犀一言</h1>
        <p class="app-subtitle">温暖的AI社交助手</p>
      </div>
      
      <div class="description-section">
        <p class="main-description">
          以礼相待，智慧沟通<br>
          让每一次交流都充满温暖
        </p>
        <p class="sub-description">
          帮助您在人际交往中找到最合适的表达方式，<br>
          让言语成为连接心灵的桥梁
        </p>
      </div>
        <div class="action-section">
        <button class="start-btn" @click="handleLogin">
          <span class="btn-icon">🌟</span>
          开始温暖旅程
        </button>
        
        <button class="trial-btn" @click="handleTrial">
          <span class="btn-icon">✨</span>
          立即体验对话
        </button>
        
        <p class="hint-text">让AI陪伴您的每一次真诚交流</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

function handleLogin() {
  router.push('/login');
}

function handleTrial() {
  router.push('/conversation-new');
}
</script>

<style scoped>
.start-container {
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
  font-size: 3rem;
  color: rgba(255, 255, 255, 0.6);
  animation: cloudFloat 8s ease-in-out infinite;
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
  font-size: 2.5rem;
}

.cloud3 {
  bottom: 30%;
  left: 8%;
  animation-delay: 4s;
  font-size: 2rem;
}

.cloud4 {
  bottom: 20%;
  right: 12%;
  animation-delay: 6s;
  font-size: 2.8rem;
}

@keyframes cloudFloat {
  0%, 100% {
    transform: translateY(0px) translateX(0px);
    opacity: 0.6;
  }
  50% {
    transform: translateY(-15px) translateX(10px);
    opacity: 0.8;
  }
}

/* 主要内容容器 */
.content-wrapper {
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(20px);
  border-radius: 30px;
  padding: 60px 40px;
  max-width: 500px;
  width: 100%;
  text-align: center;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.3);
  position: relative;
  z-index: 2;
  animation: contentSlideIn 1s ease-out;
}

@keyframes contentSlideIn {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Logo 部分 */
.logo-section {
  margin-bottom: 40px;
}

.main-logo {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  margin-bottom: 20px;
  border: 3px solid rgba(216, 180, 140, 0.3);
  transition: transform 0.3s ease;
}

.main-logo:hover {
  transform: scale(1.05) rotate(2deg);
}

.app-title {
  font-size: 2.5rem;
  font-weight: 300;
  color: #8b6f47;
  margin: 0 0 10px 0;
  letter-spacing: 2px;
}

.app-subtitle {
  font-size: 1.1rem;
  color: #a0956b;
  margin: 0;
  font-weight: 400;
}

/* 描述部分 */
.description-section {
  margin-bottom: 40px;
}

.main-description {
  font-size: 1.3rem;
  color: #7a6f5d;
  line-height: 1.6;
  margin: 0 0 20px 0;
  font-weight: 400;
}

.sub-description {
  font-size: 0.95rem;
  color: #9b8f7c;
  line-height: 1.5;
  margin: 0;
  opacity: 0.9;
}

/* 操作部分 */
.action-section {
  margin-top: 30px;
}

.start-btn {
  background: linear-gradient(135deg, #d4c5a9, #b8a082);
  color: white;
  border: none;
  padding: 15px 40px;
  border-radius: 25px;
  font-size: 1.1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  letter-spacing: 0.5px;
  box-shadow: 0 8px 25px rgba(212, 197, 169, 0.3);
}

.start-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 35px rgba(212, 197, 169, 0.4);
  background: linear-gradient(135deg, #c9b89c, #a89276);
}

.start-btn:active {
  transform: translateY(-1px);
}

.trial-btn {
  background: linear-gradient(135deg, #e8f4fd, #d4e7f4);
  color: #7a6f5d;
  border: none;
  padding: 12px 35px;
  border-radius: 25px;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  letter-spacing: 0.5px;
  box-shadow: 0 6px 20px rgba(212, 231, 244, 0.3);
  margin-top: 15px;
}

.trial-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(212, 231, 244, 0.4);
  background: linear-gradient(135deg, #d4e7f4, #c4ddf0);
  color: #6b6054;
}

.trial-btn:active {
  transform: translateY(-1px);
}

.btn-icon {
  font-size: 1.2rem;
}

.hint-text {
  margin-top: 20px;
  font-size: 0.9rem;
  color: #a69884;
  opacity: 0.8;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .content-wrapper {
    padding: 40px 30px;
    margin: 20px;
    border-radius: 25px;
  }
  
  .app-title {
    font-size: 2rem;
  }
  
  .main-description {
    font-size: 1.1rem;
  }
  
  .sub-description {
    font-size: 0.9rem;
  }
  
  .cloud {
    font-size: 2rem;
  }
  
  .cloud2 {
    font-size: 1.8rem;
  }
  
  .cloud3 {
    font-size: 1.5rem;
  }
  
  .cloud4 {
    font-size: 2rem;
  }
}

@media (max-width: 480px) {
  .content-wrapper {
    padding: 30px 20px;
  }
  
  .main-logo {
    width: 60px;
    height: 60px;
  }
  
  .app-title {
    font-size: 1.8rem;
    letter-spacing: 1px;
  }
  
  .start-btn {
    padding: 12px 30px;
    font-size: 1rem;
  }
}
</style>
