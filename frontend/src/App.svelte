<script>
  import Router from 'svelte-spa-router'
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

  import { access_token, username, is_login } from './lib/store';
  import * as myurl from "./lib/myurl"


  const routes = {    // 속성값으로 path와 component를 받으며 path는 경로를 나타내는 문자열, component는 경로와 일치하는 경우 표시할 svelte 컴포넌트를 나타낸다.
    [myurl.home_url] : Home,
    [myurl.mypage_url+'/:username']: MyPage,

    [myurl.postlist_url] : PostList,
    [myurl.postdetail_url+'/:post_id'] : PostDetail,
    [myurl.postcreate_url] : PostCreate,
    [myurl.postmodify_url+'/:post_id'] : PostModify,

    [myurl.usercreate_url] : UserCreate,
    [myurl.userlogin_url] : UserLogin,
  }

  if ($is_login) {
    const payload = JSON.parse(atob($access_token.split('.')[1]))
    const expiry = payload.exp * 1000 
    const now = new Date()
    const now_utc_1 = now.toUTCString()
    const now_utc_2 = new Date(now_utc_1)
    const now_utc = now_utc_2.getTime()
    //console.log('token and now time', expiry - now_utc)

    if (now >= expiry) {
      $access_token = ''
      $username = ''
      $is_login = false
    }
  }

</script>


<Navigation />
<main>
  <Router {routes}/>
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
  }

</style> 