<script>
    import { link } from 'svelte-spa-router'
    import { page, access_token, username, is_login } from "../lib/store"
</script>

<!-- 네비게이션바 -->
<nav>
    <div>
        <a class='home_logo' use:link href="/" on:click={()=>{$page=0}}>NLWK</a>
        <!--
        <a class='create_btn' use:link href="/nonlan_create">논란 작성</a>
        -->
        <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation">
        <span class="navbar-toggler-icon" />
    </button>
        <div>
            <ul>
                {#if $is_login}
                <li>
                    <a use:link href='/mypage/{$username}'>마이페이지</a>
                </li>
                <li>
                    <a use:link href='/user-login' on:click={()=>{
                        $access_token = ''
                        $username = ''
                        $is_login = false
                    }}>로그아웃 ({$username})</a>
                </li>
                {:else}
                <li>
                    <a use:link href='/user-create'>회원가입</a>
                </li>
                <li>
                    <a use:link href='/user-login'>로그인</a>
                </li>
                {/if}
            </ul>
        </div>
    </div>
</nav>


<style>
    nav {
        border: 1px solid #000000;
        min-width: 900px;
        width: 100%;
        margin: 0;
    }
    nav > div {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        align-items: baseline;
        margin: 3px 10px;
    }
    nav li {
        list-style-type: none;
        display: inline;
    }
    li a {
        margin: auto 10px;
    }
    .home_logo {
        font-size: 30px;
        font-weight: 600;
    }
    a {
        text-decoration: none;
        color: #000000;
    }
</style>
