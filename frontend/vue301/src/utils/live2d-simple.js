import * as PIXI from 'pixi.js'
import { Live2DModel, MotionPreloadStrategy } from 'pixi-live2d-display';

// 挂载PIXI到全局
window.PIXI = PIXI;

export async function initSimple() {
  try {
    console.log('开始初始化Live2D模型...');
    
    // 创建PIXI应用 - 必须先创建应用
    const app = new PIXI.Application({
      view: document.getElementById('canvas_view'),
      backgroundColor: 0xf0f0f0, // 设置背景色以便观察
      antialias: true,
      width: 800,
      height: 600,
      autoDensity: true
    });

    console.log('PIXI应用创建成功, 画布大小:', app.view.width, 'x', app.view.height);

    // 加载模型
    const model = await Live2DModel.from('/live2d/miku/runtime/miku.model3.json', { 
      motionPreload: MotionPreloadStrategy.NONE 
    });
    
    console.log('模型加载成功, 模型边界:', model.getBounds());

    // 添加模型到舞台
    app.stage.addChild(model);
    
    // 设置模型位置和大小
    model.anchor.set(0.5); // 设置锚点为中心
    model.x = app.view.width / 2; // 居中
    model.y = app.view.height / 2; // 居中
    model.scale.set(0.25); // 缩放

    console.log('模型位置设置:', model.x, model.y, '缩放:', model.scale.x);

    // 启用基本交互
    model.interactive = true;
    model.buttonMode = true;

    // 添加点击事件
    model.on('pointerdown', () => {
      console.log('模型被点击');
      if (model.motion) {
        model.motion('Idle');
      }
    });

    console.log('Live2D模型初始化完成');
    return { app, model };

  } catch (error) {
    console.error('Live2D初始化失败:', error);
    throw error;
  }
}
