import { createRouter, createWebHashHistory } from "vue-router";
import register from "../view/register.vue";
import Conversation from '../view/Conversation.vue';
import Conversation2 from '../view/Conversation2.vue';
import Conversation3 from '../view/Conversation3.vue';
import Conversation4 from '../view/Conversation4.vue';
import ConversationNew from '../view/ConversationNew.vue';
import start from "../view/start.vue";
import welcome from "../view/welcome.vue"
const routes = [
  {
    path: '/start',
    name: 'start',
    component: () => import('../view/start.vue'),
  },
  {
      path: '/',
      redirect: '/start', // 重定向根路径到 /art
    },  {
    path: '/live2d-demo',
    name: 'Live2DDemo',
    component: () => import('../view/Live2DDemo.vue'),
    meta: {
      title: 'Live2D模型演示'
    }
  },
  {
    path: '/live2d-simple',
    name: 'Live2DSimple',
    component: () => import('../view/Live2DSimple.vue'),
    meta: {
      title: '简单Live2D示例'
    }
  },  {
    path: '/conversation-live2d',
    name: 'ConversationWithLive2D',
    component: () => import('../view/ConversationWithLive2D.vue'),
    meta: {
      title: '带Live2D的对话页面'
    }
  },  {
    path: '/live2d-test',
    name: 'Live2DTest',
    component: () => import('../view/Live2DTest.vue'),
    meta: {
      title: 'Live2D简化测试'
    }
  },
  {
    path: '/live2d-switcher',
    name: 'Live2DModelSwitcher',
    component: () => import('../view/Live2DModelSwitcher.vue'),
    meta: {
      title: 'Live2D模型切换器'
    }
  },
  {
    path: "/login",
    name: "login",
    meta: {
      title: "登录",
    },
    component: () => import("../view/login.vue"),
  },
  {
    path: "/home",
    name: "主页",
    meta: {
      title: "主页",
    },
    component: () => import("../view/home.vue"),
    redirect: "/index",
    children: [
      {
        path: "/index",
        name: "index",
        meta: {
          title: "首页",
        },
        component: () => import("../view/welcome.vue"),
      },
    ],
  },
  {
      path: '/conversation',
      name: 'conversation',
  	  component: Conversation,
  },
  {
      path: '/conversation2',
      name: 'conversation2',
  	  component: Conversation2,
  },
  {
      path: '/conversation3',
      name: 'conversation3',
  	  component: Conversation3,
  },  {
      path: '/conversation4',
      name: 'conversation4',
  	  component: Conversation4,
  },
  {
      path: '/conversation-new',
      name: 'conversation-new',
      meta: {
        title: "沉浸式对话",
      },
  	  component: ConversationNew,
  },
  {
      path: '/start',
      name: 'start',
  	  component: start,
  },
  {
      path: '/welcome',
      name: 'welcome',
  	  component: welcome,
  },
  {
      path: '/register',
      name: 'register',
  	  component: register,
  },
];
const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  // 修改页面 title
  if (to.meta.title) {
    document.title = "知否技术 - " + to.meta.title;
  }

  if (to.path === "art") {
    return next();
  } 

  if (to.path === "/login") {
    return next();
  } else {
    let menuList = JSON.parse(sessionStorage.getItem("menuList"));
    if (!Array.isArray(menuList)) {
      console.error('menuList should be an array');
      menuList = [];
    }
    const menus = filterRouter(menuList);
    menus.forEach((route) => {
      router.addRoute(route);
    });
    return next();
  }
});

const filterRouter = (menuList) => {
  if (!Array.isArray(menuList)) {
    console.error('menuList should be an array');
    return [];
  }

  const modules = import.meta.glob("../views/**/*.vue");

  for (let index = 0; index < menuList.length; index++) {
    const e = menuList[index];
    e.component = modules["../views/home.vue"];
    if (e.children) {
      for (let index = 0; index < e.children.length; index++) {
        const item = e.children[index];
        item.component = modules[`../views/${item.component}.vue`];
      }
    }
  }
  return menuList;
};
export default router;
