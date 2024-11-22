<template>
  <div class="education-container">
    <h1 class="education-title">📚 금융 교육 콘텐츠</h1>
    <div class="education-grid">
      <div v-for="video in videos" :key="video.id" class="video-card">
        <div class="video-thumbnail" @click="watchVideo(video.videoId)">
          <img :src="getVideoThumbnail(video.videoId)" :alt="video.title">
          <div class="play-button">
            <i class="fas fa-play"></i>
          </div>
        </div>
        <div class="video-info">
          <h3>{{ video.title }}</h3>
          <p>{{ video.description }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const videos = ref([
  {
    id: 1,
    videoId: "UIJj0DzEVDQ",  // 예시 YouTube 영상 ID
    title: "금융 기초 개념은 이걸로 끝내자!",
    description: "이 영상 하나로, 금융 기본 지식을 뽀개봅시다🔥"
  },
  {
    id: 2,
    videoId: "5lHHAxyXI_g",
    title: "가장 기본적인 투자방법",
    description: "대한민국 청년들에게 희망을 주는 명강의"
  },
  {
    id: 3,
    videoId: "OlNSaSOxStc",
    title: "어려운 금융 공부, 쉽게 공부하는 방법",
    description: "신한은행 오건영 부부장이 알려주는 금융 공부법"
  },
  {
    id: 4,
    videoId: "wzQ8AvA5Jog",
    title: "재테크 입문자가 봐야하는 딱 1가지",
    description: "나만 알고 싶었던 경제 잡지 Top3"
  },
  {
    id: 5,
    videoId: "kasJ9qYXAp4",
    title: "목돈은 이렇게 굴리세요",
    description: "이자 3%대 CMA 계좌의 모든 것"
  },
  {
    id: 6,
    videoId: "o7yQ2G3OqLY",
    title: "돈의 속성을 이해하면 우리도 부자 될 수 있다!",
    description: "부자만 점점 더 잘 살게 된다? 돈의 속성을 이해하면 우리도 부자 될 수 있다!"
  },
  {
    id: 7,
    videoId: "9RrDZjbu--o",
    title: "금리 기초개념 다지기😎",
    description: "'금리'를 정말 기초부터 다루는 강의"
  },
  {
    id: 8,
    videoId: "9vpyCeZHl84",
    title: "금융투자를 하고 싶다면 경제공부부터!",
    description: "투자의 첫걸음은 경제 상식으로부터 시작한다!"
  },
  {
  id: 9,
    videoId: "T2Unam50vEc",
    title: "절세 투자 전략",
    description: "재.테.크. 어렵지 않아여, 아.시.겠.어.요?"
  }
])

const getVideoThumbnail = (videoId) => {
  return `https://img.youtube.com/vi/${videoId}/mqdefault.jpg`
}

const watchVideo = (videoId) => {
  window.open(`https://www.youtube.com/watch?v=${videoId}`, '_blank')
}
</script>

<style scoped>
.education-container {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.education-title {
  text-align: center;
  color: #1f6b1f;
  margin-bottom: 2rem;
  font-weight: 600;
}

.education-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  padding: 1rem;
}

.video-card {
  background: white;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease;
}

.video-card:hover {
  transform: translateY(-5px);
}

.video-thumbnail {
  position: relative;
  width: 100%;
  padding-top: 56.25%; /* 16:9 비율 */
}

.video-thumbnail img {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.play-button {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: rgba(51, 129, 51, 0.8);
  width: 50px;
  height: 50px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.video-thumbnail:hover .play-button {
  opacity: 1;
}

.play-button i {
  color: white;
  font-size: 20px;
}

.video-info {
  padding: 1rem;
}

.video-info h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
  color: #333;
}

.video-info p {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 1rem;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.video-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  position: relative;
  width: 80%;
  max-width: 800px;
  aspect-ratio: 16/9;
}

.modal-content iframe {
  width: 100%;
  height: 100%;
}

.close-button {
  position: absolute;
  top: -40px;
  right: -40px;
  background: none;
  border: none;
  color: white;
  font-size: 2rem;
  cursor: pointer;
}

.thumbnail-placeholder {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: #f5f5f5;
  display: flex;
  align-items: center;
  justify-content: center;
}

.fa-spinner {
  font-size: 24px;
  color: #338133;
}

/* 비활성화된 버튼 스타일 */
.watch-button:disabled {
  background: #cccccc;
  cursor: not-allowed;
}
</style>