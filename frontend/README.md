# React가 실행되는 순서
1. index.html 
   : 브라우저가 제일 먼저 여는 파일.

2. main.jsx 
   : React의 entry point.
     #root div를 찾고, 이 div 안에 'React 앱을 그릴 거야'라고 선언한다.
     그리고 <App/>을 그리라고 지시한다.

* 여기까지가 React 엔진 시동으로, 처음으로 App.jsx가 호출된다.
   
3. App.jsx
   : '시작점'이 아니라 '첫 화면 컴포넌트'

# 전체 흐름을 한 줄로 그리면 다음과 같다.

브라우저
 → index.html
   → main.jsx
     → ReactDOM.render()
       → App()
         → CollectPage()
           → ResultList()   
   

   





# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Babel](https://babeljs.io/) (or [oxc](https://oxc.rs) when used in [rolldown-vite](https://vite.dev/guide/rolldown)) for Fast Refresh
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/) for Fast Refresh

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
