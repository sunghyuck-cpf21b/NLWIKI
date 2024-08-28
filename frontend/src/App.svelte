<script>
  import Router from 'svelte-spa-router'
  import Home from "./routes/Home.svelte"
  import Detail from "./routes/Detail.svelte"
  import NonlanCreate from './routes/NonlanCreate.svelte';
  import NonlanModify from './routes/NonlanModify.svelte';
  import Navigation from "./components/Navigation.svelte";
  import TempImage from './routes/TempImage.svelte';
  import UserCreate from './routes/UserCreate.svelte';
  import UserLogin from './routes/UserLogin.svelte';
  import MyPage from './routes/MyPage.svelte';

  import { access_token, username, is_login } from './lib/store';


  const routes = {    // 속성값으로 path와 component를 받으며 path는 경로를 나타내는 문자열, component는 경로와 일치하는 경우 표시할 svelte 컴포넌트를 나타낸다.
    '/' : Home,
    '/detail/:nonlan_id': Detail,
    '/nonlan_create': NonlanCreate,
    '/user-create': UserCreate,
    '/user-login': UserLogin,
    '/nonlan-modify/:nonlan_id': NonlanModify,
    '/mypage/:username': MyPage,
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
<Router {routes}/>

