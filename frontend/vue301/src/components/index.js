import * as PIXI from 'pixi.js'
import {
  Live2DModel,
  MotionPreloadStrategy,
  InternalModel,
} from 'pixi-live2d-display';

// 挂载PIXI到全局
window.PIXI = PIXI;

export async function init() {
  try {
    // 加载模型
    const model = await Live2DModel.from('/live2d/miku/runtime/miku.model3.json', { 
      motionPreload: MotionPreloadStrategy.NONE 
    });

    // 创建模型对象
    const app = new PIXI.Application({
      // 配置模型舞台
      view: document.getElementById('canvas_view'),
      // 背景是否透明
      transparent: true,
      autoDensity: true,
      autoResize: true,
      antialias: true,
      // 高度
      height: 1080,
      // 宽度
      width: 1900
    });    // 将模型添加到舞台并配置
    app.stage.addChild(model);
    model.scale.set(0.1);
    
    // y相较于窗口左上角
    model.x = 950; // 水平居中
    model.y = 540; // 垂直居中
    
    // 启用交互
    model.interactive = true;
    model.buttonMode = true;

    console.log('Live2D模型初始化完成');
    return { app, model };

  } catch (error) {
    console.error('Live2D初始化失败:', error);
    throw error;
  }
}
