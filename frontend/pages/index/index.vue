<template>
  <div class="index-container">
    <!-- 头部信息 -->
    <div class="header">
      <div class="time">你还在吗？</div>
      <div class="contact-info" v-if="contact">
        <text class="contact-label">您的联系人</text>
        <text class="contact-name">{{ contact.name }}</text>
        <text class="contact-email">{{ maskedEmail(contact.email) }}</text>
      </div>
    </div>
    
    <!-- 签到按钮区域 -->
    <div class="checkin-section">
      <div class="checkin-button-container">
        <button
          class="checkin-button"
          :class="{ 'checked-in': checkinStatus.has_checked_in_today }"
          @click="handleCheckin"
          :disabled="checkinStatus.has_checked_in_today"
        >
          <svg v-if="!checkinStatus.has_checked_in_today" class="heartbeat-svg" viewBox="-20 0 240 100" xmlns="http://www.w3.org/2000/svg">
            <path class="heartbeat-line" d="M-20,50 L10,50 L20,20 L30,80 L40,30 L50,70 L60,50 L220,50" stroke="white" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <svg v-else class="success-svg" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
            <circle class="success-circle" cx="50" cy="50" r="45" stroke="white" stroke-width="4" fill="none" stroke-linecap="round"/>
            <path class="success-check" d="M30,50 L45,65 L70,35" stroke="white" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          <div class="checkin-text">{{ checkinStatus.has_checked_in_today ? '又活了一天' : '我在' }}</div>
        </button>
        <div class="checkin-status" v-if="checkinStatus.has_checked_in_today">
          签到成功
        </div>
      </div>
      
      <!-- 连续签到天数 -->
      <div class="consecutive-days" v-if="checkinStatus.consecutive_days > 0">
        <text class="days-label">连续签到</text>
        <text class="days-number">{{ checkinStatus.consecutive_days }}</text>
        <text class="days-unit">天</text>
      </div>
    </div>
    
    <!-- 提示信息 -->
    <div class="tips">
      <text class="tips-text">每日签到，系统将为您记录状态，若连续多日未签到，系统将于次日自动发送邮件告知您的紧急联系人</text>
    </div>
  </div>
</template>

<script>
import request from '../../utils/request';

export default {
  data() {
    return {

      contact: null,
      checkinStatus: {
        has_checked_in_today: false,
        checkin_date: null,
        consecutive_days: 0
      },
      timer: null
    };
  },
  onLoad() {
    // 初始化数据
    this.initData();

  },
  onUnload() {
    // 清除定时器
    if (this.timer) {
      clearInterval(this.timer);
    }
  },
  methods: {
    // 初始化数据
    async initData() {
      // 获取设备ID
      const deviceId = uni.getStorageSync('deviceId');
      if (!deviceId) {
        // 生成设备ID
        const newDeviceId = 'device_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        uni.setStorageSync('deviceId', newDeviceId);
      }

      // 先从缓存读取签到状态
      this.loadCheckinStatusFromCache();

      // 无感知登录
      await this.login();

      // 获取紧急联系人信息
      await this.getContact();

      // 获取签到状态
      await this.getCheckinStatus();
    },
    
    // 无感知登录
    async login() {
      try {
        const deviceId = uni.getStorageSync('deviceId');
        const res = await request.post('/auth/login', { device_id: deviceId });
        // 保存token
        uni.setStorageSync('token', res.access_token);
      } catch (err) {
        console.error('登录失败:', err);
      }
    },
    

    
    // 脱敏显示邮箱
    maskedEmail(email) {
      if (!email) return '';
      const [username, domain] = email.split('@');
      if (username.length <= 2) {
        return username + '***@' + domain;
      }
      const maskedUsername = username.substring(0, 2) + '***' + username.substring(username.length - 1);
      return maskedUsername + '@' + domain;
    },
    
    // 获取紧急联系人
    async getContact() {
      try {
        const res = await request.get('/contact');
        this.contact = res;
      } catch (err) {
        console.error('获取联系人失败:', err);
        // 没有联系人时不报错，提示用户设置
      }
    },
    
    // 从缓存加载签到状态
    loadCheckinStatusFromCache() {
      try {
        const cachedStatus = uni.getStorageSync('checkinStatus');
        const cachedDate = uni.getStorageSync('checkinDate');
        const today = this.getTodayDate();

        // 检查缓存是否是今天的
        if (cachedDate === today && cachedStatus) {
          this.checkinStatus = cachedStatus;
          this.checkinStatusLoaded = true;
        }
      } catch (err) {
        console.error('从缓存加载签到状态失败:', err);
      }
    },

    // 保存签到状态到缓存
    saveCheckinStatusToCache() {
      try {
        const today = this.getTodayDate();
        uni.setStorageSync('checkinStatus', this.checkinStatus);
        uni.setStorageSync('checkinDate', today);
      } catch (err) {
        console.error('保存签到状态到缓存失败:', err);
      }
    },

    // 获取今天的日期字符串
    getTodayDate() {
      const now = new Date();
      const year = now.getFullYear();
      const month = String(now.getMonth() + 1).padStart(2, '0');
      const day = String(now.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    },

    // 获取签到状态
    async getCheckinStatus() {
      try {
        const res = await request.get('/checkin/status');
        this.checkinStatus = res;
        // 保存到缓存
        this.saveCheckinStatusToCache();
      } catch (err) {
        console.error('获取签到状态失败:', err);
      }
    },

    // 处理签到
    async handleCheckin() {
      try {
        const res = await request.post('/checkin');
        // 更新签到状态
        this.checkinStatus.has_checked_in_today = true;
        this.checkinStatus.consecutive_days = res.consecutive_days;

        // 保存到缓存
        this.saveCheckinStatusToCache();

        // 显示成功提示
        uni.showToast({
          title: res.message,
          icon: 'success',
          duration: 2000
        });
      } catch (err) {
        console.error('签到失败:', err);
        uni.showToast({
          title: '签到失败，请重试',
          icon: 'none',
          duration: 2000
        });
      }
    }
  }
};
</script>

<style scoped>
.index-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 0 20px;
  background-color: #f8f8f8;
}

.header {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-shrink: 0;
  margin-bottom: 10px;
}

.time {
  font-size: 48px;
  font-weight: bold;
  margin-bottom: 10px;
  color: #333;
}

.contact-info {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 10px;
}

.contact-label {
  font-size: 14px;
  color: #666;
  margin-bottom: 5px;
}

.contact-name {
  font-size: 20px;
  font-weight: bold;
  color: #333;
  margin-bottom: 5px;
}

.contact-email {
  font-size: 14px;
  color: #999;
}

.checkin-section {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
}

.checkin-button-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}

.checkin-button {
  width: 95vw;
  height: 95vw;
  max-width: 500px;
  max-height: 500px;
  border-radius: 50%;
  background-color: #4CD964;
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  box-shadow: 0 0 20px rgba(76, 217, 100, 0.5);
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  animation: breathe 2s ease-in-out infinite;
}

@keyframes breathe {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 0 20px rgba(76, 217, 100, 0.5);
  }
  50% {
    transform: scale(1.05);
    box-shadow: 0 0 40px rgba(76, 217, 100, 0.7);
  }
}

.checkin-button::before {
  content: '';
  position: absolute;
  width: 120%;
  height: 120%;
  background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, rgba(255,255,255,0) 70%);
  transform: scale(0);
  transition: transform 0.5s ease;
}

.checkin-button:active::before {
  transform: scale(1);
}

.checkin-button.checked-in {
  background-color: #999;
  box-shadow: 0 0 20px rgba(153, 153, 153, 0.5);
}

.heartbeat-svg {
  width: 130%;
  height: auto;
  max-width: 550px;
}

.heartbeat-line {
  stroke-dasharray: 320 640;
  stroke-dashoffset: 320;
  animation: heartbeat 3s linear infinite;
}

@keyframes heartbeat {
  0% {
    stroke-dashoffset: 320;
  }
  100% {
    stroke-dashoffset: -640;
  }
}

.success-svg {
  width: 140px;
  height: 140px;
}

.success-circle {
  stroke-dasharray: 283;
  stroke-dashoffset: 283;
  animation: drawCircle 1s ease-out forwards;
}

.success-check {
  stroke-dasharray: 60;
  stroke-dashoffset: 60;
  animation: drawCheck 0.5s ease-out 0.5s forwards;
}

@keyframes drawCircle {
  0% {
    stroke-dashoffset: 283;
  }
  100% {
    stroke-dashoffset: 0;
  }
}

@keyframes drawCheck {
  0% {
    stroke-dashoffset: 60;
  }
  100% {
    stroke-dashoffset: 0;
  }
}

.checkin-text {
  font-size: 36px;
  font-weight: bold;
  margin-top: 10px;
}

.checkin-status {
  margin-top: 15px;
  font-size: 16px;
  color: #4CD964;
  font-weight: bold;
}

.consecutive-days {
  display: flex;
  align-items: baseline;
  justify-content: center;
  margin-top: 15px;
}

.days-label {
  font-size: 16px;
  color: #666;
  margin-right: 10px;
}

.days-number {
  font-size: 36px;
  font-weight: bold;
  color: #333;
  margin-right: 5px;
}

.days-unit {
  font-size: 18px;
  color: #666;
}

.tips {
  width: 100%;
  text-align: center;
  padding: 0;
  flex-shrink: 0;
}

.tips-text {
  font-size: 14px;
  color: #999;
  line-height: 1.5;
}
</style>