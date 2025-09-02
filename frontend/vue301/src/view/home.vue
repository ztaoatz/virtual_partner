<template>
  <div class="home-wrapper">
    <!-- 云朵装饰元素 -->
    <div class="cloud-decorations">
      <div class="cloud cloud1">☁</div>
      <div class="cloud cloud2">☁</div>
      <div class="cloud cloud3">☁</div>
    </div>
    
    <el-container class="home-container">
      <el-container>
        <el-header class="warm-header">
          <div class="header-content">
            <div class="logo-section">
              <img src="@/assets/linxi.png" class="header-logo" alt="灵犀一言" />
              <span class="app-name">灵犀一言</span>
            </div>
            
            <el-dropdown class="user-dropdown">
              <span class="user-info">
                <span class="welcome-text">您好，</span>
                <span class="username">{{ userForm.username }}</span>
                <el-icon class="dropdown-icon">
                  <arrow-down />
                </el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu class="warm-dropdown">
                  <el-dropdown-item @click.native="toUpdatePassword" class="dropdown-item">
                    <span class="item-icon">🔒</span>
                    修改密码
                  </el-dropdown-item>
                  <el-dropdown-item @click.native="logout" class="dropdown-item">
                    <span class="item-icon">👋</span>
                    退出系统
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-header>

        <el-main class="warm-main">
          <div class="main-content">
            <router-view v-slot="{ Component }">
              <transition name="fade-transition" mode="out-in">
                <component :is="Component" />
              </transition>
            </router-view>
          </div>
        </el-main>

        <el-footer class="warm-footer">
          <span class="footer-text">Copyright © 灵犀一言 - 让每一次交流都充满温暖</span>
        </el-footer>
      </el-container>
    </el-container>
  </div>
</template>
<script setup>
import { onBeforeMount, onMounted, ref, reactive } from "vue";
import router from "../router/index";
let menuList = JSON.parse(sessionStorage.getItem("menuList"));
let userForm = reactive(JSON.parse(sessionStorage.getItem("userInfo")));
// 挂载 DOM 之前
onBeforeMount(() => {
  // 当前激活的菜单
  activePath.value = sessionStorage.getItem("activePath")
    ? sessionStorage.getItem("activePath")
    : "/index";
});
// 当前激活的路由
let activePath = ref("");
// 保存链接的激活状态
const saveActiveNav = (path) => {
  // 当前激活的菜单
  activePath.value = path;
  sessionStorage.setItem("activePath", path);
};
const logout = () => {
  // 清除缓存
  sessionStorage.clear();
  router.push("/login");
};

const toUpdatePassword = () => {
  // 可以在这里添加修改密码的逻辑
  console.log("修改密码功能");
};
</script>

<style scoped>
.home-wrapper {
  min-height: 100vh;
  background: linear-gradient(135deg, 
    #fef7f0 0%,    /* 温暖的米色 */
    #fdf2e6 25%,   /* 奶油色 */
    #f8f4f0 50%,   /* 浅米色 */
    #e8f4fd 75%,   /* 淡天空蓝 */
    #d4e7f4 100%   /* 柔和蓝色 */
  );
  position: relative;
  overflow: hidden;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
}

/* 云朵装饰 */
.cloud-decorations {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

.cloud {
  position: absolute;
  font-size: 2rem;
  color: rgba(255, 255, 255, 0.4);
  animation: cloudFloat 12s ease-in-out infinite;
}

.cloud1 {
  top: 15%;
  right: 10%;
  animation-delay: 0s;
}

.cloud2 {
  bottom: 20%;
  left: 8%;
  animation-delay: 4s;
  font-size: 1.8rem;
}

.cloud3 {
  top: 60%;
  right: 5%;
  animation-delay: 8s;
  font-size: 1.5rem;
}

@keyframes cloudFloat {
  0%, 100% {
    transform: translateY(0px) translateX(0px);
    opacity: 0.4;
  }
  50% {
    transform: translateY(-10px) translateX(5px);
    opacity: 0.6;
  }
}

.home-container {
  min-height: 100vh;
  position: relative;
  z-index: 2;
}

/* 头部样式 */
.warm-header {
  height: auto !important;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  padding: 15px 30px;
  border-bottom: 1px solid rgba(216, 180, 140, 0.2);
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.05);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
}

.logo-section {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-logo {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  border: 2px solid rgba(216, 180, 140, 0.3);
}

.app-name {
  font-size: 1.3rem;
  font-weight: 500;
  color: #8b6f47;
  letter-spacing: 1px;
}

.user-dropdown {
  cursor: pointer;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 15px;
  border-radius: 20px;
  background: rgba(212, 197, 169, 0.1);
  transition: all 0.3s ease;
}

.user-info:hover {
  background: rgba(212, 197, 169, 0.2);
}

.welcome-text {
  color: #a0956b;
  font-size: 0.9rem;
}

.username {
  color: #8b6f47;
  font-weight: 500;
}

.dropdown-icon {
  color: #a0956b;
  transition: transform 0.3s ease;
}

.user-info:hover .dropdown-icon {
  transform: rotate(180deg);
}

/* 下拉菜单样式 */
:deep(.warm-dropdown) {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(216, 180, 140, 0.2);
  border-radius: 12px;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);
}

:deep(.dropdown-item) {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  color: #7a6f5d;
  transition: all 0.3s ease;
}

:deep(.dropdown-item:hover) {
  background: rgba(212, 197, 169, 0.1);
  color: #6b6054;
}

.item-icon {
  font-size: 14px;
}

/* 主内容区域 */
.warm-main {
  padding: 30px;
  min-height: calc(100vh - 140px);
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(20px);
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.3);
  min-height: 500px;
}

/* 底部样式 */
.warm-footer {
  height: auto !important;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  padding: 20px;
  border-top: 1px solid rgba(216, 180, 140, 0.2);
  text-align: center;
}

.footer-text {
  color: #a69884;
  font-size: 0.9rem;
  margin: 0;
}

/* 过渡动画 */
.fade-transition-enter-active,
.fade-transition-leave-active {
  transition: all 0.3s ease;
}

.fade-transition-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.fade-transition-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .warm-header {
    padding: 15px 20px;
  }
  
  .header-content {
    flex-direction: column;
    gap: 15px;
  }
  
  .logo-section {
    order: 1;
  }
  
  .user-dropdown {
    order: 2;
  }
  
  .warm-main {
    padding: 20px 15px;
  }
  
  .main-content {
    padding: 20px 15px;
    border-radius: 15px;
  }
  
  .app-name {
    font-size: 1.1rem;
  }
  
  .cloud {
    font-size: 1.5rem;
  }
}

@media (max-width: 480px) {
  .header-content {
    gap: 10px;
  }
  
  .header-logo {
    width: 35px;
    height: 35px;
  }
  
  .app-name {
    font-size: 1rem;
  }
  
  .warm-main {
    padding: 15px 10px;
  }
  
  .main-content {
    padding: 15px 10px;
    min-height: 400px;
  }
}

/* Element Plus 组件样式覆盖 */
:deep(.el-container) {
  background: transparent;
}

:deep(.el-header) {
  background: transparent;
  border-bottom: none;
  height: auto;
}

:deep(.el-main) {
  background: transparent;
}

:deep(.el-footer) {
  background: transparent;
  color: #a69884;
}

:deep(.el-dropdown-menu__item) {
  transition: all 0.3s ease;
}

:deep(.el-dropdown-menu__item:hover) {
  background-color: rgba(212, 197, 169, 0.1);
  color: #6b6054;
}
</style>
