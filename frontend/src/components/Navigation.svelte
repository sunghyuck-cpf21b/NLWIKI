<script>
    import { link } from 'svelte-spa-router'
    import { page, now_page, T_page, access_token, username, is_login } from "../lib/store"
    import * as myurl from "../lib/myurl"

    const nav_height = 65

</script>

<!-- 네비게이션바 -->
<nav style='height: {nav_height}px'>

    <div class='logo_box'>
        
        <a class='home_logo' use:link href={myurl.home_url} on:click={()=>{$page=0; $now_page=1; $T_page=0;}}>
            <img src='https://nlwk.nlwiki.com/media/logo_1.png' alt='' style='width: {50*(nav_height-5)/42.3}px; height: {nav_height-5}px;'>
            <span>NLWK</span>
        </a>
        
    </div>
    
    <!--
    <a class='create_btn' use:link href="/nonlan_create">논란 작성</a>
    -->

    <div class='button_box'>
        <ul>
            {#if $is_login}
            <li>
                <a use:link href={myurl.mypage_url+$username}>마이페이지</a>
            </li>
            <li>
                <a use:link href={myurl.userlogin_url} on:click={()=>{
                    $access_token = ''
                    $username = ''
                    $is_login = false
                }}>로그아웃 ({$username})</a>
            </li>
            {:else}
            <li>
                <a use:link href={myurl.usercreate_url}>회원가입</a>
            </li>
            <li>
                <a use:link href={myurl.userlogin_url}>로그인</a>
            </li>
            {/if}
        </ul>
    </div>
    
</nav>


<style>
    nav {
        border: 1px solid #000000;
        min-width: 1200px;
        width: 100%;
        margin: 0;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: center;
    }
    ul {
        margin: 0 auto;
    }
    li {
        list-style-type: none;
        display: inline;
        margin: 0 10px 0;
    }

    .home_logo {
        font-size: 30px;
        font-weight: 600;
        display: flex;
        align-items: center;
    }
    .logo_box {
        height: 100%;
        display: flex;
        align-items: center;

    }
    .button_box {
        display: flex;
        align-items: center;
        height: 100%;
        margin: 0 10px 0;

    }
    a {
        text-decoration: none;
        color: #000000;
        margin: 0 auto;
    }
</style>
