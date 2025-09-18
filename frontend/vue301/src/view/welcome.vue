
<template>
  <div class="welcome-container">
    <!-- 云朵装饰元素 -->
    <div class="cloud-decorations">
      <div class="cloud cloud1">☁</div>
      <div class="cloud cloud2">☁</div>
      <div class="cloud cloud3">☁</div>
      <div class="cloud cloud4">☁</div>
      <div class="cloud cloud5">☁</div>
    </div>
    
    <div class="content-wrapper">
      <div class="header-section">
        <img src="@/assets/linxi.png" class="logo" alt="灵犀一言" />
        <h1 class="main-title">请选择您想解决的问题</h1>
        <p class="subtitle">温暖的AI助手为您提供贴心的交流建议</p>
      </div>
        <div class="buttons-grid">
        <!-- 敬酒模块暂时隐藏 -->
        <button class="scenario-button toast-btn hidden-module" @click="handleClick('敬酒', 'conversation')" style="display: none;">
          <div class="btn-icon">🥂</div>
          <div class="btn-text">
            <span class="btn-title">敬酒</span>
            <span class="btn-desc">优雅得体的敬酒词</span>
          </div>
        </button>
          <!-- 化解尴尬模块已隐藏 -->
        <button class="scenario-button awkward-btn hidden-module" @click="handleClick('化解尴尬', 'conversation2')" style="display: none !important;">
          <div class="btn-icon">😊</div>
          <div class="btn-text">
            <span class="btn-title">化解尴尬</span>
            <span class="btn-desc">轻松化解尴尬时刻</span>
          </div>
        </button>
        
        <!-- 送祝福模块已隐藏 -->
        <button class="scenario-button blessing-btn hidden-module" @click="handleClick('送祝福', 'conversation3')" style="display: none !important;">
          <div class="btn-icon">🎉</div>
          <div class="btn-text">
            <span class="btn-title">送祝福</span>
            <span class="btn-desc">温暖真诚的祝福语</span>
          </div>
        </button>
        
        <!-- 小红书祝福模块已隐藏 -->
        <button class="scenario-button special-btn hidden-module" @click="handleClick('送祝福小红书版', 'conversation4')" style="display: none !important;">
          <div class="btn-icon">📱</div>
          <div class="btn-text">
            <span class="btn-title">小红书祝福</span>
            <span class="btn-desc">时尚有趣的网络祝福</span>
          </div>
        </button>
        
        <button class="scenario-button immersive-btn" @click="handleClick('沉浸式对话', 'conversation-new')">
          <div class="btn-icon">🌟</div>
          <div class="btn-text">
            <span class="btn-title">沉浸式对话</span>
            <span class="btn-desc">全新的AI伙伴交流体验</span>
          </div>
        </button>
      </div>
      
      <div class="footer-section">
        <p class="footer-text">选择一个场景，让AI为您提供最合适的表达方式</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router';
	const router = useRouter();
const handleClick = (scenario, page) => {
  console.log(`用户选择了场景: ${scenario}`);
  router.push({ name: page });
  
};



</script>

<style scoped>
.welcome-container {
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
  animation: cloudFloat 10s ease-in-out infinite;
}

.cloud1 {
  top: 10%;
  left: 8%;
  animation-delay: 0s;
}

.cloud2 {
  top: 20%;
  right: 12%;
  animation-delay: 2s;
  font-size: 2rem;
}

.cloud3 {
  bottom: 25%;
  left: 10%;
  animation-delay: 4s;
  font-size: 2.2rem;
}

.cloud4 {
  bottom: 15%;
  right: 8%;
  animation-delay: 6s;
  font-size: 2.3rem;
}

.cloud5 {
  top: 50%;
  left: 5%;
  animation-delay: 8s;
  font-size: 1.8rem;
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

.content-wrapper {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border-radius: 30px;
  padding: 50px 40px;
  max-width: 800px;
  width: 100%;
  text-align: center;
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.08);
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

.header-section {
  margin-bottom: 40px;
}

.logo {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  margin-bottom: 25px;
  border: 3px solid rgba(216, 180, 140, 0.3);
  transition: transform 0.3s ease;
}

.logo:hover {
  transform: scale(1.05) rotate(3deg);
}

.main-title {
  font-size: 2.2rem;
  font-weight: 400;
  color: #8b6f47;
  margin: 0 0 15px 0;
  letter-spacing: 1px;
}

.subtitle {
  color: #a0956b;
  font-size: 1rem;
  margin: 0;
  opacity: 0.9;
}

.buttons-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.scenario-button {
  background: rgba(255, 255, 255, 0.8);
  border: 2px solid rgba(216, 180, 140, 0.3);
  border-radius: 18px;
  padding: 25px 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 15px;
  text-align: left;
  position: relative;
  overflow: hidden;
}

.scenario-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
  transition: left 0.5s ease;
}

.scenario-button:hover::before {
  left: 100%;
}

.scenario-button:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.1);
  border-color: rgba(216, 180, 140, 0.6);
}

.btn-icon {
  font-size: 2.5rem;
  flex-shrink: 0;
}

.btn-text {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.btn-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #7a6f5d;
}

.btn-desc {
  font-size: 0.9rem;
  color: #9b8f7c;
  opacity: 0.8;
}

/* 按钮特殊样式 */
.toast-btn:hover {
  background: linear-gradient(135deg, rgba(255, 218, 185, 0.3), rgba(255, 228, 196, 0.3));
}

.awkward-btn:hover {
  background: linear-gradient(135deg, rgba(173, 216, 230, 0.3), rgba(176, 224, 230, 0.3));
}

.blessing-btn:hover {
  background: linear-gradient(135deg, rgba(255, 182, 193, 0.3), rgba(255, 192, 203, 0.3));
}

.special-btn:hover {
  background: linear-gradient(135deg, rgba(221, 160, 221, 0.3), rgba(238, 130, 238, 0.3));
}

.immersive-btn:hover {
  background: linear-gradient(135deg, rgba(212, 197, 169, 0.3), rgba(184, 160, 130, 0.3));
}

.footer-section {
  margin-top: 20px;
}

.footer-text {
  color: #a69884;
  font-size: 0.9rem;
  margin: 0;
  opacity: 0.8;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .content-wrapper {
    padding: 40px 25px;
    margin: 20px;
  }
  
  .main-title {
    font-size: 1.8rem;
  }
  
  .buttons-grid {
    grid-template-columns: 1fr;
    gap: 15px;
  }
  
  .scenario-button {
    padding: 20px 15px;
  }
  
  .btn-icon {
    font-size: 2rem;
  }
  
  .cloud {
    font-size: 2rem;
  }
  
  .cloud2, .cloud3, .cloud4, .cloud5 {
    font-size: 1.8rem;
  }
}

@media (max-width: 480px) {
  .content-wrapper {
    padding: 30px 20px;
  }
  
  .logo {
    width: 60px;
    height: 60px;
  }
  
  .main-title {
    font-size: 1.6rem;
  }
  
  .scenario-button {
    flex-direction: column;
    text-align: center;
    gap: 10px;
  }
  
  .btn-text {
    align-items: center;
  }
}

/* 动画效果 */
.scenario-button {
  animation: slideIn 0.6s ease-out both;
}

.scenario-button:nth-child(1) { animation-delay: 0.2s; }
.scenario-button:nth-child(2) { animation-delay: 0.3s; }
.scenario-button:nth-child(3) { animation-delay: 0.4s; }
.scenario-button:nth-child(4) { animation-delay: 0.5s; }

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

/* 隐藏的功能模块 */
.hidden-module {
  display: none !important;
}
</style>