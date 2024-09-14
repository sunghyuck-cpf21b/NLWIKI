<script>
  import Router, { push, location } from 'svelte-spa-router'
  import { onMount } from 'svelte';

  import Home from './routes/Home.svelte';
  import PostList from "./routes/PostList.svelte"
  import PostDetail from "./routes/PostDetail.svelte"
  import PostCreate from './routes/PostCreate.svelte';
  import PostModify from './routes/PostModify.svelte';
  import Navigation from "./components/Navigation.svelte";
  import TempImage from './routes/TempImage.svelte';
  import UserCreate from './routes/UserCreate.svelte';
  import UserLogin from './routes/UserLogin.svelte';
  import MyPage from './routes/MyPage.svelte';
  import SideBar from './components/Side_Bar.svelte';
  import JFF from './routes/JFF.svelte';

  import { access_token, username, is_login } from './lib/store';
  import * as store from './lib/store'
  import * as myurl from "./lib/myurl"


  const routes = {    // 속성값으로 path와 component를 받으며 path는 경로를 나타내는 문자열, component는 경로와 일치하는 경우 표시할 svelte 컴포넌트를 나타낸다.
    [myurl.home_url] : Home,
    [myurl.mypage_url+'/:username']: MyPage,
    [myurl.jff_url]: JFF,

    [myurl.postlist_url] : PostList,
    [myurl.postdetail_url+'/:post_id'] : PostDetail,
    [myurl.postcreate_url] : PostCreate,
    [myurl.postmodify_url+'/:post_id'] : PostModify,

    [myurl.usercreate_url] : UserCreate,
    [myurl.userlogin_url] : UserLogin,
  }
  

  // 상태에 따른 api 에러메세지 방지를 위함
  // 컴포넌트 렌더링 전에 script를 먼저 실행하기 위함
  let render_ready = true

  $: if ($location) {
    if ($location == myurl.home_url) {
      store.ST_category.set('전체')
    }

    if ($is_login) { // 토큰 만료됐는지 확인
      const payload = JSON.parse(atob($access_token.split('.')[1]))
      const expiry = payload.exp * 1000 
      const now = new Date()
      const now_utc_1 = now.toUTCString()
      const now_utc_2 = new Date(now_utc_1)
      const now_utc = now_utc_2.getTime()

      if (now >= expiry) { // 토큰 시간 만료됐다면 모든 상태 초기화 후 로그인 페이지로 이동      
        $access_token = ''
        $username = ''
        $is_login = false 
        render_ready = false 
        push(myurl.userlogin_url)
      }
    } 

    if (!$is_login) { // 로그아웃 상태에서 사용자의 이동 제한
      if (!($location===myurl.home_url || $location===myurl.usercreate_url || $location===myurl.userlogin_url)) {
        render_ready = false // api 오류메세지 방지를 위해 컴포넌트 렌더링 비활성화
        push(myurl.userlogin_url) // 로그인 페이지로 이동
      } else {
        render_ready = true
      }
    }

    if ($location==myurl.userlogin_url) { // 로그인창으로 이동할 때에는 컴포넌트 렌더링 활성화
      render_ready = true
    }
  }


</script>


<Navigation />
<main>
  {#if render_ready}
  <Router {routes}/>
  {/if}
</main>

<style>
  
  main{
    /*
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;*/
    margin: 50px auto;
    /*min-width: 800px;
    width: 90vw;*/
    width: 1150px;
    /* 최소 너비 설정 + 창 크기에 맞춰서 크기 설정*/
    overflow: hidden;

    background-color: var(--main-bg-color);
  }

</style> 