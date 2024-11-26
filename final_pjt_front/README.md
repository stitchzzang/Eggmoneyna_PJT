## Front : Vue 실행하기
1. front 파일로 들어가기
```bash
$ cd final_pjt_front
```

2. 필요 라이브러리 설치하기
```bash
$ npm i
$ npm i axios
$ npm i -g vue
$ npm i -g @vue/cli
```
- `npm i axios`
  - Django의 데이터를 불러오기 위해 `axios 라이브러리` 설치

- `npm i -g vue`
  - Vue.js의 핵심 라이브러리인 `vue` 설치
  - Vue.js 프레임워크 자체를 사용하기 위해 필요

- `npm i -g @vue/cli`
  - Vue CLI 설치
  - Vue 프로젝트를 쉽게 생성하고 관리하도록 도와주는 도구

- Vue에서 Django의 `requirements.txt` 파일과 같은 역할을 하는 것은 `package.json` 파일
- 추후에 `npm i` 만 실행하면 이 명령어 하나로 `package.json` 파일에 있는 모든 라이브러리를 설치 가능

3. vue 실행하기
```bash
npm dev run
```